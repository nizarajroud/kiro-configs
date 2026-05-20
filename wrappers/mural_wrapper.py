#!/usr/bin/env python3
"""MURAL MCP Server — exposes MURAL API tools via MCP (stdio transport).
Auto-authenticates via browser on first run if no token exists."""

import json
import os
import time
import urllib.parse
import urllib.request
import urllib.error
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from mcp.server.fastmcp import FastMCP

ENV_FILE = Path(__file__).parent.parent / ".env"
TOKEN_FILE = Path(__file__).parent.parent / "credentials" / "mural_token.json"
API_BASE = "https://app.mural.co/api/public/v1"

mcp = FastMCP("mural")

# --- Env loading ---

def _load_env():
    env = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                line = line.removeprefix("export ")
                k, v = line.split("=", 1)
                env[k] = v
    return env

# --- OAuth auth (first run only) ---

def _authenticate():
    env = _load_env()
    client_id = env["MURAL_CLIENT_ID"]
    client_secret = env["MURAL_CLIENT_SECRET"]
    redirect_uri = env["MURAL_REDIRECT_URI"]
    scopes = "murals:read murals:write rooms:read workspaces:read"

    auth_url = (
        "https://app.mural.co/api/public/v1/authorization/oauth2/?"
        + urllib.parse.urlencode({
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scopes,
            "state": "mcp_auth",
            "response_type": "code",
        })
    )

    import sys
    print("No MURAL token found. Opening browser for authentication...", file=sys.stderr)
    webbrowser.open(auth_url)

    code_holder = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            code = query.get("code", [None])[0]
            if code:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"MURAL auth successful! You can close this tab.")
                code_holder["code"] = code
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: no code received")

        def log_message(self, format, *args):
            pass

    port = int(redirect_uri.split(":")[-1].split("/")[0])
    print(f"Waiting for OAuth callback on port {port}...", file=sys.stderr)
    HTTPServer(("localhost", port), Handler).handle_request()

    # Exchange code for token
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code_holder["code"],
        "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/authorization/oauth2/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as resp:
        token_data = json.loads(resp.read())

    token_data["client_id"] = client_id
    token_data["client_secret"] = client_secret
    token_data["expires_at"] = time.time() + token_data.get("expires_in", 900)
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)
    print("Token saved. MURAL MCP server starting...", file=sys.stderr)

# --- Token management ---

def _load_token():
    with open(TOKEN_FILE) as f:
        return json.load(f)

def _save_token(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def _get_access_token():
    data = _load_token()
    if time.time() >= data.get("expires_at", 0) - 60:
        body = urllib.parse.urlencode({
            "client_id": data["client_id"],
            "client_secret": data["client_secret"],
            "refresh_token": data["refresh_token"],
            "grant_type": "refresh_token",
        }).encode()
        req = urllib.request.Request(
            f"{API_BASE}/authorization/oauth2/token",
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req) as resp:
            new_data = json.loads(resp.read())
        data["access_token"] = new_data["access_token"]
        data["expires_at"] = time.time() + new_data.get("expires_in", 900)
        if "refresh_token" in new_data:
            data["refresh_token"] = new_data["refresh_token"]
        _save_token(data)
    return data["access_token"]

# --- API helpers ---

def _api_get(path):
    token = _get_access_token()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def _api_post(path, payload):
    token = _get_access_token()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def _api_patch(path, payload):
    token = _get_access_token()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/json"},
        method="PATCH",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def _api_delete(path):
    token = _get_access_token()
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        method="DELETE",
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status

# --- MCP Tools ---

@mcp.tool()
def list_workspaces() -> str:
    """List all MURAL workspaces accessible to the authenticated user."""
    return json.dumps(_api_get("/workspaces"), indent=2)

@mcp.tool()
def list_rooms(workspace_id: str) -> str:
    """List all rooms in a workspace."""
    return json.dumps(_api_get(f"/workspaces/{workspace_id}/rooms"), indent=2)

@mcp.tool()
def list_murals(room_id: str = None, workspace_id: str = None) -> str:
    """List murals. Provide room_id or workspace_id."""
    if room_id:
        return json.dumps(_api_get(f"/rooms/{room_id}/murals"), indent=2)
    elif workspace_id:
        return json.dumps(_api_get(f"/workspaces/{workspace_id}/murals"), indent=2)
    return "Error: provide room_id or workspace_id"

@mcp.tool()
def get_mural_widgets(mural_id: str) -> str:
    """Get all widgets (sticky notes, shapes, text, images) from a mural. Handles pagination automatically."""
    all_widgets = []
    next_token = None
    while True:
        path = f"/murals/{mural_id}/widgets"
        if next_token:
            path += f"?next={next_token}"
        result = _api_get(path)
        all_widgets.extend(result.get("value", result.get("data", [])))
        next_token = result.get("next")
        if not next_token:
            break
    return json.dumps({"count": len(all_widgets), "widgets": all_widgets}, indent=2)

@mcp.tool()
def search_mural(mural_id: str, query: str) -> str:
    """Search for widgets containing specific text in a mural. Case-insensitive."""
    all_widgets = []
    next_token = None
    while True:
        path = f"/murals/{mural_id}/widgets"
        if next_token:
            path += f"?next={next_token}"
        result = _api_get(path)
        all_widgets.extend(result.get("value", result.get("data", [])))
        next_token = result.get("next")
        if not next_token:
            break
    q = query.lower()
    matches = [w for w in all_widgets if q in json.dumps(w).lower()]
    return json.dumps({"query": query, "matches": len(matches), "widgets": matches}, indent=2)

@mcp.tool()
def create_sticky_note(mural_id: str, text: str, x: float = 0, y: float = 0, color: str = "yellow") -> str:
    """Create a sticky note. Colors: yellow, blue, green, pink, purple, gray."""
    colors = {"yellow": "#FFFF00", "blue": "#4FC3F7", "green": "#81C784", "pink": "#F48FB1", "purple": "#CE93D8", "gray": "#BDBDBD"}
    payload = {"type": "sticky_note", "x": x, "y": y, "text": text, "style": {"backgroundColor": colors.get(color, color)}}
    return json.dumps(_api_post(f"/murals/{mural_id}/widgets/sticky-note", payload), indent=2)

@mcp.tool()
def update_sticky_note(mural_id: str, widget_id: str, text: str) -> str:
    """Update the text of an existing sticky note."""
    return json.dumps(_api_patch(f"/murals/{mural_id}/widgets/sticky-note/{widget_id}", {"text": text}), indent=2)

@mcp.tool()
def delete_widget(mural_id: str, widget_id: str) -> str:
    """Delete a widget from a mural."""
    return f"Deleted (status {_api_delete(f'/murals/{mural_id}/widgets/{widget_id}')})"

@mcp.tool()
def create_mural(room_id: str, title: str) -> str:
    """Create a new mural in a room."""
    return json.dumps(_api_post(f"/rooms/{room_id}/murals", {"title": title}), indent=2)

# --- Main ---

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--auth":
        _authenticate()
    elif not TOKEN_FILE.exists():
        print("ERROR: No MURAL token found. Run:", file=sys.stderr)
        print(f"  python3 {__file__} --auth", file=sys.stderr)
        sys.exit(1)
    else:
        mcp.run(transport="stdio")
