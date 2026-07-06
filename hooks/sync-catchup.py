#!/usr/bin/env python3
"""Sync catchup — finds and syncs all sessions not yet sent to AgentCore Memory and KB."""

import json
import os
import sqlite3
import sys
import subprocess
import time

DB_PATH = os.path.expanduser("~/.local/share/kiro-cli/data.sqlite3")
MEMORY_STATE_PATH = os.path.expanduser("~/.kiro/sessions/memory-sync-state.json")
KB_STATE_PATH = os.path.expanduser("~/.kiro/sessions/kb-sync-state.json")
MIN_MESSAGES = 8

SYNC_MEMORY_SCRIPT = os.path.expanduser("~/.kiro/hooks/sync-session-to-memory.py")
SYNC_KB_SCRIPT = "/home/nizar/workspace/PROC/xxxxuseful-scripts/kiro-kb-sync.py"


def load_state(path):
    if os.path.exists(path):
        try:
            return json.loads(open(path).read())
        except:
            return {}
    return {}


def get_unsyncted_sessions():
    """Find sessions that need syncing (modified since last sync, >= 8 messages)."""
    memory_state = load_state(MEMORY_STATE_PATH)
    kb_state = load_state(KB_STATE_PATH)

    db = sqlite3.connect(DB_PATH)
    rows = db.execute('SELECT key, conversation_id, value, updated_at FROM conversations_v2 ORDER BY updated_at DESC').fetchall()
    db.close()

    # Deduplicate by conversation_id
    seen = set()
    unique = []
    for row in rows:
        if row[1] not in seen:
            seen.add(row[1])
            unique.append(row)

    needs_memory_sync = []
    needs_kb_sync = []

    for cwd, sid, value, updated_ms in unique:
        # Check message count
        try:
            d = json.loads(value)
            history = d.get('history', [])
            msg_count = len(history) * 2  # Each turn has user + assistant
        except:
            continue

        if msg_count < MIN_MESSAGES:
            continue

        # Check if memory sync needed
        mem_info = memory_state.get(sid, {})
        mem_sent = mem_info.get('messages_sent', 0)
        if mem_sent < msg_count:
            needs_memory_sync.append(sid)

        # Check if KB sync needed
        kb_info = kb_state.get(sid, {})
        if kb_info.get('updated_ms') != updated_ms:
            needs_kb_sync.append(sid)

    return needs_memory_sync, needs_kb_sync


def main():
    needs_memory, needs_kb = get_unsyncted_sessions()

    if not needs_memory and not needs_kb:
        sys.exit(0)  # Nothing to do

    # Sync to AgentCore Memory (limit to 10 per catchup to avoid long runs)
    for sid in needs_memory[:10]:
        try:
            subprocess.Popen(
                [sys.executable, SYNC_MEMORY_SCRIPT, sid],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.5)
        except:
            pass

    # Sync to KB (limit to 10 per catchup)
    for sid in needs_kb[:10]:
        try:
            subprocess.Popen(
                [sys.executable, SYNC_KB_SCRIPT, "one", sid],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(0.5)
        except:
            pass


if __name__ == "__main__":
    main()

    # Also update the session catalog
    try:
        subprocess.Popen(
            [sys.executable, "/home/nizar/workspace/PROC/xxxxuseful-scripts/session-catalog.py", "update"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass
