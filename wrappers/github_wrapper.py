import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("GITHUB_PERSONAL_ACCESS_TOKEN", os.environ.get("GITHUB_PAT"))

os.execvp("npx", ["npx", "-y", "@modelcontextprotocol/server-github"])
