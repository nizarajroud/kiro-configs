import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("NAPKIN_API_KEY", os.environ.get("NAPKIN_API_KEY", ""))

os.execvp("npx", ["npx", "-y", "napkin-ai-mcp"])
