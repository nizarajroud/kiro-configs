import os
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("AIRTABLE_API_KEY", os.environ.get("AIRTABLE_API_KEY", ""))

os.execvp("npx", ["npx", "-y", "airtable-mcp-server"])
