---
inclusion: always
---
# Data Principles

## Principle 1: Data is Dynamic

All sources change at any time without notification. The agent MUST:
- Query sources in real time for every request
- Never assume data is the same as a previous session
- Never rely on cached or memorized answers from past conversations

## Principle 2: No Duplication

Data lives in ONE authoritative location. We do not copy it elsewhere.

| ❌ Wrong | ✅ Right |
|----------|---------|
| Copy Notion page content into a local .md file | Query Notion live |
| Export NotebookLM answers into a local index | Query NotebookLM live |
| Store Gmail search results locally | Query Gmail live |
| Maintain a "last known state" cache | Always query fresh |

**Exception**: The `domains/` folder contains data that has NO other home (e.g., steering files for the déménagement project that don't exist in Notion or NotebookLM).

## Principle 3: Source Citation is Mandatory

Every piece of information returned to the user MUST include:
- Which source it came from
- Enough context to verify (page name, email date, notebook name)

This is non-negotiable. An answer without a source citation is incomplete.

## Principle 4: Contradictions are Valuable

When sources disagree, this is INFORMATION, not an error. The agent must:
1. Present both versions clearly
2. Indicate which is more recent
3. Suggest which might be outdated
4. Ask the user to confirm the truth
5. Optionally suggest updating the stale source

## Principle 5: Extensibility Over Completeness

It is better to have a system that can easily add new sources than to try to cover everything from day one.

**Adding a new source requires only:**
1. A working MCP server
2. An entry in `sources-registry.md`
3. A routing rule in `query-routing.md`

No infrastructure changes, no database migrations, no reindexing.

## Principle 6: Privacy and Sensitivity

- Sensitive data (passwords, financial details, legal documents) stays in local files or NotebookLM (private notebooks)
- The agent never exposes raw sensitive data in responses — it references by key, not by value
- No source data is transmitted to third-party services beyond the MCP connections already configured

## Principle 7: Freshness Over Completeness

If a source is temporarily unavailable:
- Inform the user that source X could not be reached
- Provide partial results from available sources
- NEVER fabricate or guess information to fill the gap
- Suggest retrying later for the missing source

## Principle 8: Timezone is Always Montreal (America/Toronto)

All dates and times displayed to the user or interpreted from sources MUST use the **America/Toronto** timezone (Eastern Time, Montréal/Québec). This applies to:
- Displaying task due dates and event times
- Interpreting timestamps from TickTick, Gmail, Google Calendar, etc.
- Converting UTC or other timezone data before presenting to the user
- The current time reference is always the local machine time (ET)

Never display raw UTC times to the user. Always convert to Eastern Time (ET).

## Principle 9: The Agent Learns Routing, Not Data

The steering files teach the agent HOW to find information, not WHAT the information is. If the agent needs to "remember" a fact, it should be stored in one of the sources (NotebookLM, Notion, etc.), not in a steering file.

| Belongs in steering files | Belongs in data sources |
|--------------------------|------------------------|
| "For school questions, check NotebookLM first" | "Léa is enrolled at École X" |
| "Financial data is in the Excel file" | "Monthly rent is $1,500" |
| "Use Gmail for confirmation dates" | "The appointment is March 15" |
