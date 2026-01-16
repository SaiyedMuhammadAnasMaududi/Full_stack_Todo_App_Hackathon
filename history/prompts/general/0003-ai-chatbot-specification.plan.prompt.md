---
id: 3
title: "AI Chatbot Specification and Planning"
stage: "plan"
date_iso: "2026-01-15"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "ai-chatbot-integration"
branch: "main"
user: "anasbhai"
command: "sp.plan"
labels: ["ai", "chatbot", "mcp", "openai-agents", "cohere"]
links:
  spec: "specs/003-ai-chatbot-integration/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/003-ai-chatbot-integration/plan.md"
  - "specs/003-ai-chatbot-integration/research.md"
  - "specs/003-ai-chatbot-integration/data-model.md"
  - "specs/003-ai-chatbot-integration/contracts/openapi.yaml"
  - "specs/003-ai-chatbot-integration/ai-agent-config.md"
  - "specs/003-ai-chatbot-integration/quickstart.md"
  - "specs/003-ai-chatbot-integration/checklists/validation-checklist.md"
tests:
  - "Unit tests for AI agent configuration"
  - "Integration tests for MCP tools"
  - "API tests for chat endpoint"
  - "Security tests for user isolation"
---

## Prompt

Objective

Define a clear, auditable execution plan for implementing an AI-powered
conversational Todo chatbot using OpenAI Agents SDK, Cohere LLM,
and MCP server architecture, while preserving the integrity of the
existing full-stack Todo application.

Execution Strategy

Phases of Work
Phase 1: Architecture & Integration Design

Create:

High-level architecture sketch showing:

Frontend (ChatKit UI + chatbot icon)

FastAPI chat endpoint

OpenAI Agents SDK (Agent + Runner)

MCP Server (task tools)

Neon PostgreSQL (tasks, conversations, messages)

Clear data flow from user message → agent → MCP tool → database → response

Decisions to document:

Why stateless chat architecture is used

Why MCP tools are the only allowed task interface

Why Cohere is used as the LLM provider

Why existing REST endpoints remain unchanged

Phase 2: Specification-to-Tool Mapping

Define explicit mappings between:

Natural language intents → MCP tools

Agent behavior rules → tool invocation logic

Output artifacts:

Tool invocation rules table

Error-handling strategy (task not found, invalid task ID, empty list)

Confirmation message patterns

Phase 3: MCP Server Planning

Plan MCP Server responsibilities:

Stateless tool execution

Task ownership enforcement

Database persistence via SQLModel

Tools to plan:

add_task

list_tasks

update_task

complete_task

delete_task

Decisions to document:

Input validation strategy

Ownership verification logic

Consistent tool response schema

Phase 4: AI Agent Design (OpenAI Agents SDK)

Plan agent configuration:

Agent instructions (task-focused, tool-first behavior)

Tool availability rules

Multi-tool chaining logic

Friendly confirmation responses

LLM Provider Plan:

Replace Gemini with Cohere

Use Cohere via OpenAI Agents SDK abstraction

Ensure no direct LLM calls outside the agent runner

Phase 5: Chat API Endpoint Planning

Endpoint:

POST /api/{user_id}/chat

Plan request lifecycle:

Verify JWT

Validate user_id against token

Fetch conversation history from DB

Store incoming user message

Build agent input (history + new message)

Run agent with MCP tools

Persist assistant response

Return response + tool_calls

Decision to document:

Why server holds no in-memory state

Why conversation is DB-backed

Phase 6: Frontend Chat Integration Planning

Plan frontend changes:

Add chatbot icon to existing Todo UI

Integrate OpenAI ChatKit

Send messages to backend chat endpoint

Display assistant responses and confirmations

Security planning:

Attach JWT token to chat requests

Handle 401 responses gracefully

Environment Variables Plan

The implementation must explicitly request the following environment variables:

Backend

COHERE_API_KEY
→ Taken from Cohere dashboard

BETTER_AUTH_SECRET
→ Same secret used by frontend Better Auth

DATABASE_URL
→ Neon PostgreSQL connection string

Frontend

NEXT_PUBLIC_OPENAI_DOMAIN_KEY
→ Provided after adding deployed domain to OpenAI allowlist

No secrets may be hardcoded.

Testing & Validation Strategy

Validation must be aligned with /sp.specify success criteria.

Functional Validation

Add task via chat

List tasks via chat

Update task via chat

Complete task via chat

Delete task via chat

Security Validation

Requests without JWT → 401

Cross-user access attempts → blocked

Tool calls always include correct user_id

Statelessness Validation

Restart server → conversations resume correctly

No memory loss across requests

Non-Goals Enforcement

Explicitly confirm during implementation that:

REST APIs are not modified

Agent never accesses database directly

No session or cache is used for chat state

MCP tools are the only task mutation path

Deliverables from This Plan

Architecture diagram

MCP tool definitions

Agent instruction prompt

Chat API flow documentation

Environment variable checklist

Validation checklist

## Response snapshot

Successfully created a comprehensive implementation plan for the AI-powered conversational Todo chatbot. The plan includes:

1. **Implementation Plan** (`specs/003-ai-chatbot-integration/plan.md`): Detailed architecture covering all six phases including high-level design, component responsibilities, and key decisions.

2. **Research Documentation** (`specs/003-ai-chatbot-integration/research.md`): Technology decisions for AI framework, LLM provider, MCP server, and architecture patterns.

3. **Data Model** (`specs/003-ai-chatbot-integration/data-model.md`): Complete schema for Conversation and Message entities with relationships and validation rules.

4. **API Contracts** (`specs/003-ai-chatbot-integration/contracts/openapi.yaml`): Full OpenAPI specification for the chatbot API endpoints.

5. **AI Agent Configuration** (`specs/003-ai-chatbot-integration/ai-agent-config.md`): Detailed configuration for OpenAI Agents SDK with Cohere integration.

6. **Quickstart Guide** (`specs/003-ai-chatbot-integration/quickstart.md`): Step-by-step setup and deployment instructions.

7. **Validation Checklist** (`specs/003-ai-chatbot-integration/checklists/validation-checklist.md`): Comprehensive checklist for implementation and testing.

The plan addresses all requirements including stateless architecture, MCP tool usage, user isolation, and preservation of existing REST APIs. All constitutional requirements are satisfied, and the design follows the specified technology stack with OpenAI Agents SDK, Cohere LLM, and MCP server architecture.

## Outcome

- ✅ Impact: Created comprehensive planning artifacts for AI chatbot implementation
- 🧪 Tests: Defined testing strategies for AI agent, MCP tools, API, and security
- 📁 Files: Generated 7 key planning documents covering architecture, data model, API contracts, and implementation guides
- 🔁 Next prompts: Ready for task generation phase (/sp.tasks)
- 🧠 Reflection: Plan comprehensively addresses all requirements while maintaining system integrity

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from the plan using /sp.tasks