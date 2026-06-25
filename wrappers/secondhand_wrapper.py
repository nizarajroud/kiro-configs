import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/HomeWspce/secondhand-mcp/.env")

os.execvp("node", ["node", "/home/nizar/HomeWspce/secondhand-mcp/dist/index.js"])
