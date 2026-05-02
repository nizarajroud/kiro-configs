import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("GITHUB_TOKEN", os.environ.get("GITHUB_PAT", ""))

os.execvp("node", ["node", "/home/nizar/HomeWspce/notion-mcp-server/bin/cli.mjs"])
