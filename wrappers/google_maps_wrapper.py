#!/usr/bin/env python3
"""Wrapper for Google Maps Grounding Lite remote MCP via mcp-remote."""
import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/HomeWspce/kiro-configs/.env")

api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
if not api_key:
    print("ERROR: GOOGLE_MAPS_API_KEY not set in .env", file=sys.stderr)
    sys.exit(1)

os.execvp("npx", [
    "npx", "mcp-remote",
    "https://mapstools.googleapis.com/mcp",
    "--header", f"X-Goog-Api-Key:{api_key}"
])
