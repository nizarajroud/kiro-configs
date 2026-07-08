#!/usr/bin/env python3
"""Wrapper for graphistry-mcp server — loads credentials from .env"""
import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/HomeWspce/kiro-configs/.env")

os.environ.setdefault("GRAPHISTRY_USERNAME", os.environ.get("GRAPHISTRY_USERNAME", ""))
os.environ.setdefault("GRAPHISTRY_PASSWORD", os.environ.get("GRAPHISTRY_PASSWORD", ""))
os.environ.setdefault("LOG_LEVEL", "INFO")

server_dir = "/home/nizar/HomeWspce/graphistry-mcp/src"
os.environ["PYTHONPATH"] = server_dir
sys.path.insert(0, server_dir)

os.execvp("python3", ["python3", "-m", "graphistry_mcp_server.server"])
