#!/usr/bin/env python3
"""MCP Wrapper: Unified idea-to-issue pipeline.

Two prompts:
- idea: auto-detect repo from cwd (fallback: IDEAS)
- backlog: always targets nizarajroud/IDEAS
"""
import json
import subprocess
import re
import sys

OWNER = "nizarajroud"
FALLBACK_REPO = "IDEAS"

PROMPT_TEMPLATE = """Crée une issue GitHub avec ces paramètres EXACTS. Ne pose AUCUNE question. Exécute directement.

owner: {owner}
repo: {repo}
title: {idea}
labels: [{label}]
body: (laisser vide)

Utilise l'outil create_issue avec owner="{owner}", repo="{repo}", title="{idea}", labels=["{label}"].
Ne modifie PAS le repo. Ne demande PAS de confirmation. Exécute immédiatement."""

LABELS_IDEAS = "projet, optimisation, expérimentation, évolution, portail, infra"
LABELS_DEFAULT = "feature, enhancement, bug, design"


def detect_repo():
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            m = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$", url)
            if m:
                return m.group(1), m.group(2)
    except Exception:
        pass
    return OWNER, FALLBACK_REPO


def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"prompts": {"listChanged": False}, "tools": {"listChanged": False}},
            "serverInfo": {"name": "idea", "version": "2.0.0"}
        }}

    if method == "notifications/initialized":
        return None

    if method == "prompts/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "prompts": [
                {
                    "name": "idea",
                    "description": "Crée une issue dans le repo courant (ou IDEAS si pas dans un repo Git)",
                    "arguments": [{"name": "idea", "description": "L'idée à transformer", "required": True}]
                },
                {
                    "name": "backlog",
                    "description": "Crée une issue dans le backlog centralisé (nizarajroud/IDEAS), peu importe le cwd",
                    "arguments": [{"name": "idea", "description": "L'idée à noter", "required": True}]
                }
            ]
        }}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": []}}

    if method == "prompts/get":
        name = request.get("params", {}).get("name", "")
        args = request.get("params", {}).get("arguments", {})
        idea = args.get("idea", "")

        if name == "backlog":
            owner, repo = OWNER, FALLBACK_REPO
            label = "projet"
        else:
            owner, repo = detect_repo()
            label = "projet" if repo == FALLBACK_REPO else "feature"

        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "messages": [{"role": "user", "content": {"type": "text", "text": PROMPT_TEMPLATE.format(
                idea=idea, owner=owner, repo=repo, label=label
            )}}]
        }}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = handle_request(request)
        if response:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
