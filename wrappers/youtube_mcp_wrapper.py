import os
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

# Primary + optional fallback keys (the server rotates on quota exhaustion)
os.environ.setdefault("YOUTUBE_API_KEY", os.environ.get("YOUTUBE_API_KEY", ""))
os.environ.setdefault("YOUTUBE_API_KEY2", os.environ.get("YOUTUBE_API_KEY2", ""))
os.environ.setdefault("YOUTUBE_API_KEY3", os.environ.get("YOUTUBE_API_KEY3", ""))
os.environ.setdefault("YOUTUBE_TRANSCRIPT_LANG", os.environ.get("YOUTUBE_TRANSCRIPT_LANG", "en"))

os.execvp("npx", ["npx", "-y", "zubeid-youtube-mcp-server"])
