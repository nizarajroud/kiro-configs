import os
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("FASTMCP_LOG_LEVEL", "ERROR")

os.execvp("uvx", ["uvx", "awslabs.eks-mcp-server@latest", "--allow-sensitive-data-access"])
