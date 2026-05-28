#!/usr/bin/env python3
"""Wrapper for @fangjunjie/ssh-mcp-server that reads ~/.ssh/config and generates a JSON config."""
import json
import os
import re
import tempfile

SSH_CONFIG = os.path.expanduser("~/.ssh/config")

def parse_ssh_config(path):
    """Parse ~/.ssh/config into a list of host configs for ssh-mcp-server."""
    configs = []
    current = None

    with open(path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if not line:
                continue
            if line.lower().startswith("host "):
                if current and current.get("host"):
                    configs.append(current)
                patterns = line[5:].strip()
                # Skip wildcard-only entries
                if "*" in patterns or "?" in patterns:
                    current = None
                    continue
                current = {"name": patterns.split()[0]}
            elif current is not None:
                m = re.match(r"(\S+)\s+(.*)", line)
                if m:
                    key, val = m.group(1).lower(), m.group(2).strip()
                    if key == "hostname":
                        current["host"] = val
                    elif key == "user":
                        current["username"] = val
                    elif key == "port":
                        current["port"] = int(val)
                    elif key == "identityfile":
                        current["privateKey"] = os.path.expanduser(val)

    if current and current.get("host"):
        configs.append(current)

    # Ensure required fields have defaults
    for c in configs:
        c.setdefault("port", 22)
        c.setdefault("username", os.environ.get("USER", "root"))
        # Use SSH agent if no privateKey specified
        if "privateKey" not in c:
            c["agent"] = os.environ.get("SSH_AUTH_SOCK", "")

    return configs

configs = parse_ssh_config(SSH_CONFIG)

# Write temp JSON config
tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", prefix="ssh-mcp-", delete=False)
json.dump(configs, tmp)
tmp.close()

os.execvp("npx", ["npx", "-y", "@fangjunjie/ssh-mcp-server", "--config-file", tmp.name])
