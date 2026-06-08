import os
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("PERPLEXITY_API_KEY", os.environ.get("PERPLEXITY_API_KEY", ""))

os.execvp("npx", ["npx", "-yq", "@perplexity-ai/mcp-server"])
