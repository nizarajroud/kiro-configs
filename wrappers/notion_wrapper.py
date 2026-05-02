import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")
os.environ.setdefault("NOTION_TOKEN", os.environ.get("NOTION_PERSONAL_PAT", ""))
os.environ.setdefault("GITHUB_TOKEN", os.environ.get("GITHUB_PERSONAL_PAT", ""))

os.execvp("node", ["node", "/home/nizar/HomeWspce/notion-mcp-server/bin/cli.mjs"])
