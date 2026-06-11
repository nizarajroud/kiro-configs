---
name: ssh-mcp-server
description: SSH remote server management — execute commands, upload/download files via SSH config hosts.
---
# SSH MCP Server

- **Status**: installed
- **JSON key**: `ssh-mcp-server`
- **Location**: settings/mcp.json
- **Wrapper**: none
- **Command**: `python3 /home/nizar/HomeWspce/kiro-configs/wrappers/ssh_mcp_wrapper.py`
- **Source**: Community package
- **Verdict**: adopted

## Tools

| Tool | Description |
|------|-------------|
| `listservers` | List configured SSH servers |
| `executecommand` | Run command on remote server |
| `upload` | Upload file to remote |
| `download` | Download file from remote |

## Auth

- SSH keys configured in `~/.ssh/config`
- Supports bastion hosts, SOCKS proxy, 2FA

## Limitations

- Default timeout: 30s per command
- Connection name defaults to 'default' if not specified
- Requires SSH key access (no interactive password prompts)
