import os
import boto3
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("bedrock-agent-multi-project")

# Default project — stored in ~/.smartingest_default_project (single source of truth)
# or via the switch_default_project tool
DEFAULT_PROJECT_FILE = os.path.expanduser("~/.smartingest_default_project")


def _get_default_project() -> str:
    """Read default project from file (single source of truth)."""
    if os.path.exists(DEFAULT_PROJECT_FILE):
        with open(DEFAULT_PROJECT_FILE, "r") as f:
            return f.read().strip()
    return ""


def _set_default_project(name: str):
    """Persist default project to file."""
    with open(DEFAULT_PROJECT_FILE, "w") as f:
        f.write(name)


def _discover_projects() -> dict:
    """Discover active SmartIngest agents via AWS API (tag-based)."""
    region = os.getenv("AWS_REGION", "ca-central-1")
    client = boto3.client("bedrock-agent", region_name=region)

    projects = {}
    paginator = client.get_paginator("list_agents")

    for page in paginator.paginate():
        for agent in page.get("agentSummaries", []):
            agent_name = agent.get("agentName", "")
            agent_id = agent.get("agentId", "")
            status = agent.get("agentStatus", "")

            # Only include SmartIngest agents that are PREPARED
            if not agent_name.endswith("-agent"):
                continue
            if status != "PREPARED":
                continue

            # Extract environment name: "ctx2-agent" → "ctx2"
            env_name = agent_name.replace("-agent", "")

            # Get alias (prefer 'live', fallback to TSTALIASID)
            alias_id = "TSTALIASID"
            try:
                aliases_resp = client.list_agent_aliases(agentId=agent_id)
                for alias in aliases_resp.get("agentAliasSummaries", []):
                    if alias.get("agentAliasName") == "live":
                        alias_id = alias.get("agentAliasId", "TSTALIASID")
                        break
            except Exception:
                pass

            projects[env_name] = {
                "agent_id": agent_id,
                "alias_id": alias_id,
                "description": f"SmartIngest environment: {env_name}",
            }

    return projects


# Discover projects at startup
PROJECTS = _discover_projects()


@mcp.tool()
def list_projects() -> str:
    """List available SmartIngest projects and their descriptions."""
    if not PROJECTS:
        return "No active SmartIngest projects found. Are any environments deployed?"

    default = _get_default_project()
    result = []
    for name, config in sorted(PROJECTS.items()):
        marker = " ⭐ (default)" if name == default else ""
        result.append(f"- **{name}**: {config['description']} [Agent: {config['agent_id']}]{marker}")

    return "\n".join(result)


@mcp.tool()
def query_project(question: str, project: str | None = None, session_id: str | None = None) -> str:
    """Query a SmartIngest project's knowledge base via its Bedrock Agent.

    Args:
        question: The question to ask about the project documents.
        project: Project name (e.g., 'ctx2', 'bixi'). Defaults to the default project.
        session_id: Optional session ID for conversation continuity.
    """
    # Resolve project
    project_name = project or _get_default_project()

    if not project_name:
        available = ", ".join(sorted(PROJECTS.keys()))
        return f"❌ No default project set. Specify one: {available}\nUse switch_default_project() to set a default."

    if project_name not in PROJECTS:
        available = ", ".join(sorted(PROJECTS.keys()))
        return f"❌ Project '{project_name}' not found. Available: {available}"

    config = PROJECTS[project_name]

    if not session_id:
        session_id = f"kiro-{project_name}-{os.urandom(4).hex()}"

    # Create client with extended timeout
    region = os.getenv("AWS_REGION", "ca-central-1")
    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=region,
        config=boto3.session.Config(read_timeout=180),
    )

    # Invoke with versioned alias + streaming
    response = client.invoke_agent(
        agentId=config["agent_id"],
        agentAliasId=config["alias_id"],
        sessionId=session_id,
        inputText=question,
        streamingConfigurations={"streamFinalResponse": True},
    )

    # Collect streamed response
    completion = ""
    for event in response.get("completion", []):
        if "chunk" in event:
            chunk = event["chunk"]
            if "bytes" in chunk:
                completion += chunk["bytes"].decode()

    return completion


@mcp.tool()
def switch_default_project(name: str) -> str:
    """Switch the default SmartIngest project for queries.

    Args:
        name: Project name to set as default (e.g., 'ctx2', 'bixi').
    """
    if name not in PROJECTS:
        available = ", ".join(sorted(PROJECTS.keys()))
        return f"❌ Project '{name}' not found. Available: {available}"

    _set_default_project(name)
    return f"✅ Default project switched to: **{name}** (Agent: {PROJECTS[name]['agent_id']})"


if __name__ == "__main__":
    mcp.run()
