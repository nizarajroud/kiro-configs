#!/usr/bin/env python3
"""MCP Wrapper: Product Owner Idea-to-Issue pipeline.

Exposes a single MCP prompt 'idea' that accepts multi-line text
and instructs the agent to create a GitHub issue, update steering, and update Notion.
"""
import json
import sys

PROMPT_TEMPLATE = """Agis comme un Product Owner. Transforme cette idée en User Story et exécute les actions suivantes :

IDÉE : {idea}

ACTIONS À EXÉCUTER :
1. Crée une issue GitHub sur nizarajroud/MY-PERSONAL-PORTFOLIO avec :
   - Titre clair et concis
   - Description au format "En tant que [visiteur/recruteur], je veux [action], afin de [bénéfice]"
   - Critères d'acceptation (3-5 items en checklist)
   - Labels appropriés (feature, enhancement, bug, design, etc.)
2. Mets à jour le steering file du projet si accessible (.kiro/steering.md)
3. Mets à jour ou crée la page Notion "MY-PERSONAL-PORTFOLIO" avec la User Story dans le backlog
4. Confirme avec le numéro de l'issue et le lien Notion

Contexte : Portail personnel Cloud Architect (expériences, certifications, CV, projets)."""


def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"prompts": {"listChanged": False}},
            "serverInfo": {"name": "idea-prompt", "version": "1.0.0"}
        }}

    if method == "notifications/initialized":
        return None

    if method == "prompts/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "prompts": [{
                "name": "idea",
                "description": "Transforme une idée en User Story → GitHub Issue + Notion + Steering",
                "arguments": [{"name": "idea", "description": "L'idée à transformer (mot, phrase, ou paragraphe)", "required": True}]
            }]
        }}

    if method == "prompts/get":
        args = request.get("params", {}).get("arguments", {})
        idea = args.get("idea", "")
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "messages": [{"role": "user", "content": {"type": "text", "text": PROMPT_TEMPLATE.format(idea=idea)}}]
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
