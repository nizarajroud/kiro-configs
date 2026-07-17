#!/usr/bin/env python3
"""Sync catchup — optimized version.

Key optimizations:
1. Skip if last run was < 1 hour ago (flag file)
2. Use only updated_at from SQLite (no JSON parsing) for delta detection
3. Only parse JSON for sessions that actually need syncing
4. Sequential subprocess calls (not parallel) to avoid resource saturation
"""

import json
import os
import sqlite3
import sys
import subprocess
import time

DB_PATH = os.path.expanduser("~/.local/share/kiro-cli/data.sqlite3")
MEMORY_STATE_PATH = os.path.expanduser("~/.kiro/sessions/memory-sync-state.json")
KB_STATE_PATH = os.path.expanduser("~/.kiro/sessions/kb-sync-state.json")
IMPORT_STATE_PATH = os.path.expanduser("~/.kiro/sessions/memory-import-state.json")
LAST_RUN_PATH = os.path.expanduser("~/.kiro/sessions/.catchup-last-run")
MIN_MESSAGES = 8
MAX_PER_RUN = 5
COOLDOWN_SECONDS = 3600  # 1 hour

SYNC_MEMORY_SCRIPT = os.path.expanduser("~/.kiro/hooks/sync-session-to-memory.py")
SYNC_KB_SCRIPT = "/home/nizar/workspace/PROC/xxxxuseful-scripts/kiro-kb-sync.py"
CATALOG_SCRIPT = "/home/nizar/workspace/PROC/xxxxuseful-scripts/session-catalog.py"


def should_skip():
    """Skip if last run was less than COOLDOWN_SECONDS ago."""
    if os.path.exists(LAST_RUN_PATH):
        last_run = os.path.getmtime(LAST_RUN_PATH)
        if time.time() - last_run < COOLDOWN_SECONDS:
            return True
    return False


def touch_last_run():
    """Mark current run time."""
    os.makedirs(os.path.dirname(LAST_RUN_PATH), exist_ok=True)
    with open(LAST_RUN_PATH, 'w') as f:
        f.write(str(int(time.time())))


def load_state(path):
    if os.path.exists(path):
        try:
            return json.loads(open(path).read())
        except:
            return {}
    return {}


def get_unsynced_sessions():
    """Find sessions needing sync using ONLY updated_at (no JSON parsing).
    
    Strategy: compare updated_at in SQLite vs state files.
    Only sessions where updated_at differs from state need attention.
    """
    kb_state = load_state(KB_STATE_PATH)
    import_state = load_state(IMPORT_STATE_PATH)

    db = sqlite3.connect(DB_PATH)
    # Only fetch sid + updated_at (lightweight query, no value column)
    rows = db.execute(
        'SELECT conversation_id, updated_at FROM conversations_v2 ORDER BY updated_at DESC'
    ).fetchall()
    db.close()

    # Deduplicate
    seen = set()
    unique = []
    for sid, updated_ms in rows:
        if sid not in seen:
            seen.add(sid)
            unique.append((sid, updated_ms))

    needs_kb_sync = []
    needs_memory_sync = []

    for sid, updated_ms in unique:
        # KB: check if updated_ms matches
        kb_info = kb_state.get(sid, {})
        if kb_info.get('updated_ms') != updated_ms:
            needs_kb_sync.append(sid)

        # Memory: check if updated_ms matches
        mem_info = import_state.get(sid, {})
        if mem_info.get('updated_ms') != updated_ms:
            needs_memory_sync.append(sid)

    return needs_memory_sync, needs_kb_sync


def validate_session(sid):
    """Check if session has enough messages (only for sessions that need sync)."""
    db = sqlite3.connect(DB_PATH)
    row = db.execute(
        'SELECT value FROM conversations_v2 WHERE conversation_id=? LIMIT 1', (sid,)
    ).fetchone()
    db.close()
    if not row:
        return False
    try:
        d = json.loads(row[0])
        return len(d.get('history', [])) >= MIN_MESSAGES // 2
    except:
        return False


def main():
    # Cooldown check
    if should_skip():
        sys.exit(0)

    touch_last_run()

    needs_memory, needs_kb = get_unsynced_sessions()

    if not needs_memory and not needs_kb:
        # Still run catalog update (lightweight)
        subprocess.Popen(
            [sys.executable, CATALOG_SCRIPT, "update"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        sys.exit(0)

    # Sync KB (limit per run, validate msg count before syncing)
    synced_kb = 0
    for sid in needs_kb:
        if synced_kb >= MAX_PER_RUN:
            break
        if not validate_session(sid):
            continue
        try:
            subprocess.run(
                [sys.executable, SYNC_KB_SCRIPT, "one", sid],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=30
            )
            synced_kb += 1
        except:
            pass

    # Sync Memory (limit per run)
    synced_mem = 0
    for sid in needs_memory:
        if synced_mem >= MAX_PER_RUN:
            break
        if not validate_session(sid):
            continue
        try:
            subprocess.run(
                [sys.executable, SYNC_MEMORY_SCRIPT, sid],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=30
            )
            synced_mem += 1
        except:
            pass

    # Update catalog
    subprocess.Popen(
        [sys.executable, CATALOG_SCRIPT, "update"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


if __name__ == "__main__":
    main()
