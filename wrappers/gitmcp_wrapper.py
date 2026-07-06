#!/usr/bin/env python3
"""
GitMCP Wrapper — Proxies GitMCP remote server via mcp-remote (SSE→stdio).
Reads GITMCP_REPO from .env to dynamically target any GitHub repository.

Usage in exp2.json:
  "git-mcp": {
    "command": "python3",
    "args": ["/home/nizar/HomeWspce/kiro-configs/wrappers/gitmcp_wrapper.py"]
  }

Set GITMCP_REPO in .env:
  export GITMCP_REPO="aws-samples/landing-zone-accelerator-on-aws-for-cccs-medium"
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/HomeWspce/kiro-configs/.env")

repo = os.environ.get("GITMCP_REPO", "aws-samples/landing-zone-accelerator-on-aws-for-cccs-medium")
url = f"https://gitmcp.io/{repo}"

# Use npx mcp-remote to proxy SSE remote server to stdio
os.execvp("npx", ["npx", "--yes", "mcp-remote", url])
