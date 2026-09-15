"""FastAPI web wrapper around kiro-cli acp.

Phase 1 MVP:
- Serves a single-page chat UI (static/index.html)
- One WebSocket per browser connection
- Each connection spawns its own `kiro-cli acp` subprocess, does the ACP
  handshake, creates a session (cwd configurable), sets an agent (mode),
  and relays user prompts to streaming assistant chunks.

Reuses the validated ACP layer from src/kiro_acp_chat_client/:
  process_manager.py (subprocess + JSON-RPC read/write)
  acp_client.py      (ACP protocol methods)
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Make the reusable ACP layer importable
_SRC = Path(__file__).parent / "src"
sys.path.insert(0, str(_SRC))

from kiro_acp_chat_client.acp_client import ACPClient  # noqa: E402
from kiro_acp_chat_client.process_manager import (  # noqa: E402
    ProcessManager,
    ProcessStartError,
    ProcessTerminatedError,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("web-interface")

APP_DIR = Path(__file__).parent
STATIC_DIR = APP_DIR / "static"

# Default working directory for ACP sessions (where kiro loads .kiro/ config from)
DEFAULT_CWD = os.environ.get("KIRO_WEB_CWD", str(Path.home() / "HomeWspce" / "kiro-configs"))
DEFAULT_AGENT = os.environ.get("KIRO_WEB_AGENT", "exp2")

# Hook scripts — mirror qq's pre/post-session behavior exactly
_HOOKS = {
    "catchup": str(Path.home() / ".kiro/hooks/sync-catchup.py"),
    "memory": str(Path.home() / ".kiro/hooks/sync-session-to-memory.py"),
    "kb_sync": "/home/nizar/workspace/PROC/xxxxuseful-scripts/kiro-kb-sync.py",
    "catalog": "/home/nizar/workspace/PROC/xxxxuseful-scripts/session-catalog.py",
}


def _run_bg(*args: str) -> None:
    """Launch a detached background process (fire-and-forget), like qq's `&`."""
    import subprocess

    try:
        subprocess.Popen(  # noqa: S603
            ["python3", *args],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("bg hook failed (%s): %s", args, e)


def post_session_sync(session_id: str) -> None:
    """Post-session hooks — identical to qq's _qq_resume tail.

    Runs in background (non-blocking): AgentCore Memory + Knowledge Base + topic catalog.
    """
    if not session_id:
        return
    logger.info("post-session sync for %s", session_id)
    _run_bg(_HOOKS["memory"], session_id)
    _run_bg(_HOOKS["kb_sync"], "one", session_id)
    _run_bg(_HOOKS["catalog"], "enrich-one", session_id)

app = FastAPI(title="Kiro Web Interface")


@app.on_event("startup")
async def _startup_catchup() -> None:
    """Pre-flight catchup sync for missed sessions — mirrors qq's startup hook."""
    _run_bg(_HOOKS["catchup"])
    logger.info("startup: sync-catchup launched")


# Path to the CLI session DB (used by the DELETE endpoint). Listing logic itself
# lives in the shared session-query.py script (single source of truth with qq).
_DB_PATH = str(Path.home() / ".local/share/kiro-cli/data.sqlite3")


# Shared session-listing logic — single source of truth used by BOTH qq and the web.
# Located next to the qq scripts so any future change to qq's -r logic propagates here.
_SESSION_QUERY = "/home/nizar/workspace/PROC/xxxxuseful-scripts/session-query.py"


def _agent_for_session(session_id: str) -> str:
    """Return the agent of a session, via the shared session-query.py script."""
    import subprocess

    try:
        out = subprocess.run(  # noqa: S603
            ["python3", _SESSION_QUERY, "agent", session_id],
            capture_output=True, text=True, timeout=15,
        )
        return out.stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def list_recent_sessions() -> list[dict]:
    """Return last-24h sessions via the shared session-query.py (same as qq -r)."""
    import subprocess

    try:
        out = subprocess.run(  # noqa: S603
            ["python3", _SESSION_QUERY, "recent", "--json"],
            capture_output=True, text=True, timeout=20,
        )
        data = json.loads(out.stdout or "{}")
        return data.get("sessions", [])
    except Exception as e:  # noqa: BLE001
        logger.warning("session list error: %s", e)
        return []


class ACPSession:
    """Owns one kiro-cli acp subprocess for a single WebSocket connection."""

    def __init__(self, cwd: str, agent: str) -> None:
        self.cwd = cwd
        self.agent = agent
        self.pm = ProcessManager()
        self.acp = ACPClient(self.pm)
        self.session_id: str = ""
        self.modes: list[dict] = []
        self.models: list[dict] = []

    async def start(self) -> dict:
        """Spawn kiro-cli acp, handshake, create session, set the agent."""
        await self.pm.start(timeout=25.0)
        await self.acp.initialize()
        result = await self.acp.create_session(self.cwd)
        self.session_id = result.get("sessionId", "")

        modes = result.get("modes", {}) or {}
        models = result.get("models", {}) or {}
        self.modes = modes.get("availableModes", []) if isinstance(modes, dict) else []
        self.models = models.get("availableModels", []) if isinstance(models, dict) else []

        # Set the requested agent if it exists
        if any(m.get("id") == self.agent for m in self.modes):
            await self.acp.set_mode(self.session_id, self.agent)
        else:
            logger.warning("Agent %r not found; using session default", self.agent)

        return result

    async def load(self, session_id: str, ws: WebSocket) -> dict:
        """Resume an existing session and replay its history to the websocket.

        session/load makes the agent replay the conversation as session/update
        notifications (user_message_chunk / agent_message_chunk / tool_call),
        followed by the final response matching the request id. We coalesce
        consecutive chunks of the same role into whole messages and forward
        each completed message to the browser as a 'history' event.
        """
        await self.pm.start(timeout=25.0)
        await self.acp.initialize()
        self.session_id = session_id
        await self.acp.load_session(session_id, self.cwd)
        req_id = self.acp._last_request_id

        cur_role: str | None = None
        cur_text: list[str] = []

        async def flush() -> None:
            nonlocal cur_role, cur_text
            if cur_role and cur_text:
                await ws.send_json(
                    {"type": "history", "role": cur_role, "text": "".join(cur_text)}
                )
            cur_role, cur_text = None, []

        result: dict = {}
        while True:
            msg = await self.acp.read_update()
            # Final response to session/load → replay done
            if "id" in msg and msg.get("id") == req_id and "method" not in msg:
                await flush()
                result = msg.get("result") or {}
                break
            # Agent request during replay (rare) — ignore/skip
            if "id" in msg and "method" in msg:
                continue
            if msg.get("method") == "session/update":
                update = msg.get("params", {}).get("update", {})
                utype = update.get("sessionUpdate", "")
                if utype in ("user_message_chunk", "agent_message_chunk"):
                    role = "user" if utype == "user_message_chunk" else "assistant"
                    content = update.get("content", {})
                    if content.get("type") == "text":
                        # Flush on role change (user<->assistant)
                        if cur_role and cur_role != role:
                            await flush()
                        cur_role = role
                        cur_text.append(content.get("text", ""))
                elif utype == "tool_call":
                    # A tool call ends the current text segment. Flush it, emit the
                    # tool note, so the NEXT text becomes a new bubble AFTER the note.
                    # This preserves chronological order exactly like live streaming/CLI.
                    await flush()
                    await ws.send_json(
                        {"type": "history_tool", "title": update.get("title", "tool")}
                    )

        # Parse modes/models from the load result
        modes = result.get("modes", {}) or {}
        models = result.get("models", {}) or {}
        self.modes = modes.get("availableModes", []) if isinstance(modes, dict) else []
        self.models = models.get("availableModels", []) if isinstance(models, dict) else []
        # Resolve the session's real agent from the CLI DB (like qq does),
        # since load's currentModeId is the ACP default, not the session's agent.
        real_agent = _agent_for_session(session_id)
        if real_agent and any(m.get("id") == real_agent for m in self.modes):
            self.agent = real_agent
            await self.acp.set_mode(self.session_id, real_agent)
        return result

    async def stream_prompt(self, text: str, ws: WebSocket) -> None:
        """Send a prompt and forward streaming chunks to the websocket."""
        await self.acp.send_prompt(self.session_id, text)
        while True:
            msg = await self.acp.read_update()

            # Agent request (e.g. permission) — auto-allow in MVP
            if "id" in msg and "method" in msg:
                if msg.get("method") == "session/request_permission":
                    params = msg.get("params", {})
                    opts = params.get("options", [])
                    chosen = None
                    for o in opts:
                        oid = str(o.get("optionId", "")).lower()
                        if "allow" in oid or "yes" in oid:
                            chosen = o.get("optionId")
                            break
                    if not chosen and opts:
                        chosen = opts[0].get("optionId")
                    await self.acp.respond_to_request(
                        msg["id"], {"outcome": {"outcome": "selected", "optionId": chosen}}
                    )
                    title = params.get("toolCall", {}).get("title", "action")
                    await ws.send_json({"type": "tool", "title": title})
                continue

            # Final response (id, no method) → turn complete
            if "id" in msg and "method" not in msg:
                await ws.send_json({"type": "done"})
                return

            # Streaming notification
            if msg.get("method") == "session/update":
                update = msg.get("params", {}).get("update", {})
                utype = update.get("sessionUpdate", "")
                if utype == "agent_message_chunk":
                    content = update.get("content", {})
                    if content.get("type") == "text":
                        await ws.send_json({"type": "chunk", "text": content.get("text", "")})
                elif utype == "tool_call":
                    await ws.send_json({"type": "tool", "title": update.get("title", "tool")})

    async def shutdown(self) -> None:
        await self.pm.shutdown()


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/api/sessions")
async def api_sessions() -> dict:
    """List recent sessions (last 24h) — mirrors `qq -r`."""
    return {"sessions": list_recent_sessions()}


# Root of AI-generated artifacts (diagrams, images, etc.)
_AIGEN_ROOT = Path("/mnt/c/Users/nizar/Documents/AI-GENERATED").resolve()


@app.get("/ai-generated/{path:path}")
async def serve_ai_generated(path: str):
    """Serve a file from the AI-GENERATED folder (read-only, no path traversal).

    Used to display generated diagrams/images inline in the chat.
    """
    from fastapi import HTTPException

    # Resolve and ensure the target stays inside _AIGEN_ROOT (anti path-traversal)
    target = (_AIGEN_ROOT / path).resolve()
    if not str(target).startswith(str(_AIGEN_ROOT)):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(str(target))


@app.delete("/api/sessions/{session_id}")
async def api_delete_session(session_id: str) -> dict:
    """Delete a session from the CLI SQLite DB (all rows for this conversation_id)."""
    import sqlite3

    try:
        db = sqlite3.connect(_DB_PATH)
        cur = db.execute(
            "DELETE FROM conversations_v2 WHERE conversation_id=?", (session_id,)
        )
        db.commit()
        deleted = cur.rowcount
        db.close()
        logger.info("Deleted session %s (%d rows)", session_id, deleted)
        return {"ok": True, "deleted": deleted}
    except Exception as e:  # noqa: BLE001
        logger.warning("delete session error: %s", e)
        return {"ok": False, "error": str(e)}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    session: ACPSession | None = None
    synced = False  # True once post-session hooks have run (explicit stop)
    try:
        # First message from client can carry cwd/agent/session_id
        init_msg = await ws.receive_json()
        cwd = init_msg.get("cwd") or DEFAULT_CWD
        agent = init_msg.get("agent") or DEFAULT_AGENT
        resume_id = init_msg.get("session_id")

        if resume_id:
            # Resume an existing session: load + replay history
            await ws.send_json(
                {"type": "status", "text": f"Reprise de la session {resume_id[:8]}…"}
            )
            session = ACPSession(cwd=cwd, agent=agent)
            await session.load(resume_id, ws)
            await ws.send_json(
                {
                    "type": "ready",
                    "session_id": session.session_id,
                    "agent": session.agent,
                    "cwd": cwd,
                    "resumed": True,
                    "modes": [m.get("id") for m in session.modes],
                }
            )
        else:
            await ws.send_json(
                {"type": "status", "text": f"Démarrage de kiro-cli acp (agent: {agent})…"}
            )
            session = ACPSession(cwd=cwd, agent=agent)
            await session.start()
            await ws.send_json(
                {
                    "type": "ready",
                    "session_id": session.session_id,
                    "agent": agent,
                    "cwd": cwd,
                    "resumed": False,
                    "modes": [m.get("id") for m in session.modes],
                }
            )

        # Main loop: receive prompts, stream responses
        while True:
            data = await ws.receive_json()
            if data.get("type") == "prompt":
                text = (data.get("text") or "").strip()
                if not text:
                    continue
                try:
                    await session.stream_prompt(text, ws)
                except ProcessTerminatedError as e:
                    await ws.send_json({"type": "error", "text": str(e)})
                    break
            elif data.get("type") == "stop":
                # Explicit "Arrêter session": run post-session hooks now, confirm, then stop.
                post_session_sync(session.session_id)
                synced = True
                await ws.send_json(
                    {"type": "stopped", "session_id": session.session_id}
                )
                break
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except ProcessStartError as e:
        await ws.send_json({"type": "error", "text": f"Impossible de démarrer kiro-cli: {e}"})
    except Exception as e:  # noqa: BLE001
        logger.exception("WS error")
        try:
            await ws.send_json({"type": "error", "text": str(e)})
        except Exception:  # noqa: BLE001, S110
            pass
    finally:
        if session is not None:
            # Post-session sync (Memory + KB + topic catalog) — like qq.
            # Skip if already done via an explicit "stop" to avoid double-sync.
            if not synced:
                post_session_sync(session.session_id)
            await session.shutdown()


# Serve static assets (index.html, JS, CSS)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
