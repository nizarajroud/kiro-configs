#!/bin/bash
# Stop hook: sends ALL new messages from the current session to AgentCore Memory.
# Tracks what was already sent to avoid duplicates.
EVENT=$(cat)

# Log for debugging
echo "$(date) | STOP HOOK TRIGGERED" >> /tmp/kiro-hook-debug.log
echo "$EVENT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'session_id={d.get(\"session_id\",\"NONE\")}')" >> /tmp/kiro-hook-debug.log 2>&1

# Extract session ID from the event
SESSION_ID=$(echo "$EVENT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null)
[ -z "$SESSION_ID" ] && exit 0

# Run the sync script in background (non-blocking)
python3 ~/.kiro/hooks/sync-session-to-memory.py "$SESSION_ID" &>/dev/null &
