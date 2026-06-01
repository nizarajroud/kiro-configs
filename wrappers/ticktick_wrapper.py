import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.execvp("/home/nizar/.local/bin/tick-mcp", ["tick-mcp", "serve"])
