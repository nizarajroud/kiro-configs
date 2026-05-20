import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

env = os.environ.copy()
env["OPENAI_API_KEY"] = env.get("BEDROCK_GATEWAY_API_KEY", "")
env["OPENAI_BASE_URL"] = f"http://localhost:{env.get('BEDROCK_GATEWAY_PORT', '8766')}/api/v1"
env["OPENAI_MODEL"] = "amazon.nova-pro-v1:0"
env["VISION_PROVIDER"] = "openai"
env["LOG_LEVEL"] = "ERROR"

venv_python = "/home/nizar/HomeWspce/mcp-image-recognition/.venv/bin/python"
server_module = "image_recognition_server.server"
src_dir = "/home/nizar/HomeWspce/mcp-image-recognition/src"

os.execve(venv_python, [venv_python, "-m", server_module], {**env, "PYTHONPATH": src_dir})
