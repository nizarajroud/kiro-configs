---
inclusion: always
---
# Personal Knowledge Hub — Product Overview

## Purpose

This workspace is the **master data warehouse of my entire personal life**. It serves as the single entry point for an AI agent to answer any question about my personal affairs by intelligently querying the right data sources in real time.

## Target User

Me (Nizar) — via Kiro CLI, Telegram bot, or any future interface.

## Core Objective

When I ask a question about my personal life, the agent must:
1. Understand the intent and classify the domain
2. Route to the correct source(s) — NOT maintain a static index
3. Query sources live (they are dynamic and change constantly)
4. Synthesize a response with source citations
5. Flag contradictions between sources

## What This Project Is NOT

- NOT a copy/mirror of data from other systems
- NOT a static index that needs manual sync
- NOT limited to local files — it orchestrates live queries to external sources
- NOT a code project — it is a knowledge orchestration layer

## Domains of Life Covered

- Déménagement (relocation project)
- Famille (children, education, schools, clubs, health)
- Finances (accounts, expenses, investments, budget)
- Administration (papers, insurance, taxes, immigration)
- Abonnements (telecom, cloud, sport)
- Identité (personal documents, IDs)
- Any future personal project

## Key Design Decisions

1. **Query-first, not index-first** — sources are queried live via MCP
2. **Each source self-indexes** — no centralized duplication
3. **Steering files define routing logic** — not data
4. **Extensible** — adding a new source = adding a MCP connector
5. **NotebookLM + Notion are primary sources of truth**
