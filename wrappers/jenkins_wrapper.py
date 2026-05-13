import os
import sys
from dotenv import load_dotenv

load_dotenv("/home/nizar/.kiro/.env")

url = os.environ.get("CSBEN_JENKINS_URL", "")
user = os.environ.get("CSBEN_JENKINS_USER", "")
token = os.environ.get("CSBEN_JENKINS_TOKEN", "")

os.execvp("mcp-jenkins", [
    "mcp-jenkins",
    "--jenkins-url", url,
    "--jenkins-username", user,
    "--jenkins-password", token,
    "--read-only"
])
