#!/usr/bin/env python3
"""Fast wrapper for mcp-gsuite. Uses local venv (no uvx), patches schemas."""

import sys
import os
import json
import subprocess
import threading

VENV_PYTHON = "/home/nizar/.gmail-mcp/.venv/bin/python"
GAUTH_FILE = "/home/nizar/.gmail-mcp/.gauth.json"
ACCOUNTS_FILE = "/home/nizar/.gmail-mcp/.accounts.json"
CREDENTIALS_DIR = "/home/nizar/.gmail-mcp/credentials"

RENAMES = {"__user_id__": "user_id", "__calendar_id__": "calendar_id"}

def fix_tool_params(tools_result):
    for tool in tools_result.get("tools", []):
        schema = tool.get("inputSchema", {})
        props = schema.get("properties", {})
        required = schema.get("required", [])
        for old_name, new_name in RENAMES.items():
            if old_name in props:
                props[new_name] = props.pop(old_name)
            for i, r in enumerate(required):
                if r == old_name:
                    required[i] = new_name
        for prop_val in props.values():
            if isinstance(prop_val, dict):
                prop_val.pop("required", None)
    return tools_result

def fix_tool_call_params(params):
    if "arguments" in params:
        args = params["arguments"]
        for new_name, old_name in [(v, k) for k, v in RENAMES.items()]:
            if new_name in args:
                args[old_name] = args.pop(new_name)
    return params

def main():
    # Auto-patch mcp-gsuite source bugs (only if needed, uses marker file)
    import glob
    marker = "/home/nizar/.gmail-mcp/.patched"
    if not os.path.exists(marker):
        for f in glob.glob("/home/nizar/.gmail-mcp/.venv/**/mcp_gsuite/tools_gmail.py", recursive=True):
            with open(f, "r") as fh:
                content = fh.read()
            if '"required": False' in content:
                content = content.replace('"required": False', '')
            if 'gmail_service.get_email_by_id(args["original_message_id"])' in content:
                content = content.replace(
                    'gmail_service.get_email_by_id(args["original_message_id"])',
                    'gmail_service.get_email_by_id_with_attachments(args["original_message_id"])[0]')
            with open(f, "w") as fh:
                fh.write(content)
        for f in glob.glob("/home/nizar/.gmail-mcp/.venv/**/mcp_gsuite/gmail.py", recursive=True):
            with open(f, "r") as fh:
                content = fh.read()
            if 'message["payload"]["parts"]' in content:
                with open(f, "w") as fh:
                    fh.write(content.replace('message["payload"]["parts"]', 'message["payload"].get("parts", [])'))
        open(marker, "w").close()
    proc = subprocess.Popen(
        ["/home/nizar/.gmail-mcp/.venv/bin/mcp-gsuite",
         "--gauth-file", GAUTH_FILE,
         "--accounts-file", ACCOUNTS_FILE,
         "--credentials-dir", CREDENTIALS_DIR],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
    )

    def read_responses():
        for line in proc.stdout:
            if not line.strip():
                continue
            try:
                msg = json.loads(line)
                if "result" in msg and "tools" in msg.get("result", {}):
                    msg["result"] = fix_tool_params(msg["result"])
                sys.stdout.write(json.dumps(msg) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                sys.stdout.write(line.decode() if isinstance(line, bytes) else line)
                sys.stdout.flush()

    reader = threading.Thread(target=read_responses, daemon=True)
    reader.start()

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
            if msg.get("method") == "tools/call":
                msg["params"] = fix_tool_call_params(msg.get("params", {}))
            proc.stdin.write((json.dumps(msg) + "\n").encode())
            proc.stdin.flush()
        except json.JSONDecodeError:
            proc.stdin.write(line.encode() if isinstance(line, str) else line)
            proc.stdin.flush()

    proc.wait()

if __name__ == "__main__":
    main()
