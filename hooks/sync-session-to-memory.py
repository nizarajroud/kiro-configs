#!/usr/bin/env python3
"""Sync a Kiro CLI session to AgentCore Memory — sends only NEW messages (delta tracking)."""

import json
import os
import sqlite3
import sys
import time

sys.path.insert(0, '/home/nizar/HomeWspce/sample-amazon-bedrock-agentcore-memory-mcp-server/venv/lib/python3.13/site-packages')

from bedrock_agentcore.memory.session import MemorySessionManager
from bedrock_agentcore.memory.constants import ConversationalMessage, MessageRole

# Config
DB_PATH = os.path.expanduser("~/.local/share/kiro-cli/data.sqlite3")
STATE_PATH = os.path.expanduser("~/.kiro/sessions/memory-sync-state.json")
MEMORY_ID = "kiro_sessions_memory-gyjyxdCmPK"
REGION = "ca-central-1"
PROFILE = "csna-operations-sso-828"
ACTOR_ID = os.environ.get("USER", "nizar")

os.environ['AWS_PROFILE'] = PROFILE
os.environ['AWS_REGION'] = REGION


def load_state():
    if os.path.exists(STATE_PATH):
        return json.loads(open(STATE_PATH).read())
    return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    open(STATE_PATH, 'w').write(json.dumps(state))


def extract_all_messages(value_json):
    """Extract ALL user+assistant messages from a session."""
    try:
        d = json.loads(value_json)
    except:
        return None, None, None, None

    cm = d.get('context_manager', {})
    agent = cm.get('current_profile', 'unknown') if isinstance(cm, dict) else 'unknown'
    history = d.get('history', [])

    messages = []
    for turn in history:
        # User message
        user = turn.get('user', {})
        content = user.get('content', {})
        user_text = ''
        if isinstance(content, dict):
            user_text = content.get('Prompt', {}).get('prompt', '')
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get('type') == 'text':
                    user_text = c.get('text', '')
                    break

        # Assistant message
        assistant = turn.get('assistant', {})
        a_content = assistant.get('content', [])
        a_text = ''
        if isinstance(a_content, list):
            for c in a_content:
                if isinstance(c, dict) and c.get('type') == 'text':
                    a_text = c.get('text', '')
                    break

        if user_text:
            messages.append(('USER', user_text))
        if a_text:
            messages.append(('ASSISTANT', a_text))

    return messages, agent, len(history), d.get('updated_at', '')


def main():
    if len(sys.argv) < 2:
        print("Usage: sync-session-to-memory.py <session_id>", file=sys.stderr)
        sys.exit(1)

    session_id = sys.argv[1]

    # Read session from SQLite
    db = sqlite3.connect(DB_PATH)
    row = db.execute(
        "SELECT key, value, updated_at FROM conversations_v2 WHERE conversation_id=? ORDER BY updated_at DESC LIMIT 1",
        (session_id,)
    ).fetchone()
    db.close()

    if not row:
        sys.exit(0)

    cwd, value, updated_ms = row
    messages, agent, turn_count, _ = extract_all_messages(value)

    if not messages or len(messages) < 8:
        sys.exit(0)  # Skip sessions with fewer than 8 messages (noise)

    folder = os.path.basename(cwd) if cwd else 'unknown'

    # Load sync state — check how many messages were already sent
    state = load_state()
    session_state = state.get(session_id, {})
    already_sent = session_state.get('messages_sent', 0)

    # Only send new messages (delta)
    new_messages = messages[already_sent:]
    if not new_messages:
        sys.exit(0)  # Nothing new to send

    # Connect to AgentCore Memory
    session_manager = MemorySessionManager(
        memory_id=MEMORY_ID,
        region_name=REGION
    )

    # Use a deterministic session ID based on the kiro session
    memory_session_id = f"kiro_{session_id[:8]}_{folder}_{agent}"
    # Clean invalid chars
    memory_session_id = ''.join(c if c.isalnum() or c in '-_' else '_' for c in memory_session_id)

    session = session_manager.create_memory_session(
        actor_id=ACTOR_ID,
        session_id=memory_session_id
    )

    # Send messages in batches of 10
    BATCH_SIZE = 10
    sent_count = 0

    for i in range(0, len(new_messages), BATCH_SIZE):
        batch = new_messages[i:i + BATCH_SIZE]
        turns = []
        for role, text in batch:
            # Prefix with folder/agent for cascade search
            if role == 'USER':
                prefixed_text = f"[{folder}/{agent}] {text[:2000]}"
                turns.append(ConversationalMessage(prefixed_text, MessageRole.USER))
            else:
                turns.append(ConversationalMessage(text[:2000], MessageRole.ASSISTANT))

        try:
            session.add_turns(messages=turns)
            sent_count += len(batch)
        except Exception as e:
            # Log error but don't crash
            print(f"Error sending batch: {e}", file=sys.stderr)
            if 'Throttling' in str(e):
                time.sleep(2)
            break

    # Update state
    state[session_id] = {
        'messages_sent': already_sent + sent_count,
        'last_sync': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'folder': folder,
        'agent': agent
    }
    save_state(state)


if __name__ == "__main__":
    main()
