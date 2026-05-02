import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("N8N_BASE_URL", "http://localhost:5678")
os.environ.setdefault("N8N_API_KEY", os.environ.get("N8N_API_KEY", ""))

os.execvp("npx", ["npx", "-y", "n8n-mcp-server"])
