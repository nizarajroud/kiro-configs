import os
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

os.environ.setdefault("JIRA_PERSONAL_TOKEN", os.environ.get("JIRA_PERSONAL_TOKEN", ""))
os.environ.setdefault("CONFLUENCE_PERSONAL_TOKEN", os.environ.get("CONFLUENCE_PERSONAL_TOKEN", ""))

os.execvp("uvx", ["uvx", "mcp-atlassian"])
