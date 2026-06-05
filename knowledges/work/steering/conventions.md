---
inclusion: always
---
# Work Context — Conventions

## Git

- Branch naming: `feature/<ticket>-<description>`, `fix/<ticket>-<description>`
- Commit messages: conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`)
- Never push directly to main/master without PR
- PR titles: concise, under 70 characters

## Documentation

- Architecture decisions → Confluence
- Diagrams → AWS diagram generator or Mermaid, stored in Notion or Confluence
- Meeting notes → Notion

## Code

- Follow existing project conventions before introducing new patterns
- Read existing code before writing new code
- Verify API signatures with context7 before using external libraries
- Infrastructure changes require explicit user confirmation

## AWS Profiles

- `csna-operations-sso-828` — primary profile for CSBEN operations
- Always specify region explicitly for cross-region operations
