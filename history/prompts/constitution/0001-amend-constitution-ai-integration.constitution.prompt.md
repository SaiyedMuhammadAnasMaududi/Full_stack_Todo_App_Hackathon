---
id: 0001
title: amend-constitution-ai-integration
stage: constitution
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Sonnet 4.5
command: /sp.constitution
labels: ["constitution", "ai-integration", "security", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution
Project Name

Secure Multi-User Todo Application with AI Chatbot (Agentic + MCP)

Purpose

Define non-negotiable system rules governing architecture, security, data ownership,
AI behavior, and integration boundaries for a full-stack Todo application enhanced
with an AI-powered conversational interface.

This Constitution ensures that:

Existing REST-based task management remains stable

AI integration is additive, not destructive

All user data remains isolated, secure, and auditable

Agentic behavior is controlled, deterministic, and tool-driven

All specifications, plans, tasks, prompts, and generated code must comply with this Constitution.

System Overview

The system consists of four cooperating layers:

Frontend

Next.js (App Router)

Standard UI for task management

ChatKit-based UI for AI chatbot

Backend

Python FastAPI

REST APIs for task management

Chat API endpoint for AI interaction

Stateless request handling

AI Layer

OpenAI Agents SDK

Cohere model as the LLM provider

Agent reasoning + tool invocation only

MCP Layer

Official MCP SDK

Task operations exposed strictly as tools

Stateless tools with database persistence

Core Architectural Principles (Non-Negotiable)
1. Statelessness

No server-side session memory is allowed

No in-memory conversation state may persist between requests

All conversational state must be stored in the database

Any server instance must be able to handle any request independently

2. Single Source of Truth

Database is the only source of truth for:

Tasks

Conversations

Messages

AI agents must never infer or assume state without database reads

Frontend state must always reflect backend responses

3. Authentication & Identity

Better Auth is the only authentication provider

JWT tokens issued by Better Auth are mandatory for:

REST task APIs

Chat API

Backend must:

Verify JWT signature

Validate expiration

Extract user identity from token

Backend must never trust user_id from request payload alone

4. User Isolation (Hard Rule)

Every task, conversation, and message is owned by exactly one user

All queries must be filtered by authenticated user ID

Cross-user access is strictly forbidden

AI agents must never access or reference another user's data

REST API Stability Rule

Existing REST endpoints must not change:

URLs

HTTP methods

Request/response semantics

The AI chatbot must integrate without modifying or breaking:

Task CRUD behavior

Authorization logic

Database schema (except additive tables for chat)

AI & Agent Rules (Critical)
1. Agent Capabilities

The AI agent:

Can reason over natural language

Can decide which MCP tools to call

Can chain multiple tools in a single turn

Can explain and confirm actions in natural language

The AI agent:

Cannot directly access the database

Cannot call REST APIs directly

Cannot fabricate tool results

Cannot modify data without a tool call

2. Tool-Only Action Rule

All state changes must occur via MCP tools.

If an action changes tasks:

An MCP tool must be invoked

The tool must persist the change

The agent must confirm the action

No exceptions.

3. MCP Tool Contract Integrity

MCP tools must be:

Stateless

Deterministic

Idempotent where possible

MCP tools must validate:

User ownership

Input correctness

MCP tools are the only bridge between AI and the database

Conversational Architecture Rules

Chat endpoint:

POST /api/{user_id}/chat

Each request must:

Load conversation history from DB

Append new user message

Run agent with MCP tools

Persist assistant response

Return response + tool calls

Server must retain no runtime memory

Model & AI Provider Rules

OpenAI Agents SDK must be used for:

Agent definition

Tool registration

Agent execution

Cohere API key must be used as the LLM provider

Model credentials must:

Be read from environment variables

Never be hardcoded

Agent logic must be provider-agnostic where possible

Environment Variables (Mandatory Governance)

All secrets must be supplied via environment variables only:

BETTER_AUTH_SECRET

DATABASE_URL

COHERE_API_KEY

OPENAI_DOMAIN_KEY (frontend ChatKit)

No secret may appear in:

Source code

Logs

Responses

Client-side bundles (except explicitly public keys)

Error Handling & UX Rules

Errors must be:

Gracefully handled

User-safe

Non-leaking (no stack traces)

AI must:

Explain failures politely

Never blame the system

Never expose internal implementation details

Out of Scope (System-Wide)

The system will not include:

Password handling in backend

Role-based permissions

Cross-user collaboration

Real-time streaming chat

Long-term memory beyond stored conversations

AI fine-tuning

Vendor/product comparisons

Compliance Requirement

Any specification, plan, task breakdown, agent prompt, or generated code
that violates this Constitution is invalid and must be corrected before implementation.

This Constitution is the highest authority in the project.

## Response snapshot

Updated the project constitution to incorporate AI Chatbot and MCP specifications while maintaining all security and architectural requirements. The constitution now includes expanded principles for statelessness, single source of truth, authentication, user isolation, and detailed rules for AI and MCP integration.

## Outcome

- ✅ Impact: Updated project constitution to version 2.0.0 with comprehensive AI integration rules and expanded architectural principles
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated with new AI/MCP specifications
- 🔁 Next prompts: none
- 🧠 Reflection: The constitution now properly governs AI behavior and MCP integration while preserving existing security requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
