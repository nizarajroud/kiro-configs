#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/HomeWspce/kiro-configs/.env")

os.environ.setdefault("ATLASSIAN_BITBUCKET_USERNAME", os.environ.get("BITBUCKET_USERNAME", ""))
os.environ.setdefault("ATLASSIAN_BITBUCKET_APP_PASSWORD", os.environ.get("BITBUCKET_APP_PASSWORD", ""))

os.execvp("npx", ["npx", "-y", "@aashari/mcp-server-atlassian-bitbucket"])
