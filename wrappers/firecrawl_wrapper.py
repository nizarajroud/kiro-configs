import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/HomeWspce/kiro-configs/.env")

os.execvp("npx", ["npx", "-y", "firecrawl-mcp"])
