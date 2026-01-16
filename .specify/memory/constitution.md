<!-- Sync Impact Report:
Version change: 1.0.0 → 2.0.0
Modified principles: Backend Security Rules → Core Architectural Principles (expanded with statelessness and user isolation)
Added sections: AI Layer, MCP Layer, AI & Agent Rules, Converstaional Architecture Rules, Model & AI Provider Rules
Removed sections: Original functional requirements (replaced with expanded scope)
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Secure Multi-User Todo Application with AI Chatbot Constitution

## Core Architectural Principles (Non-Negotiable)

### Statelessness
No server-side session memory is allowed. No in-memory conversation state may persist between requests. All conversational state must be stored in the database. Any server instance must be able to handle any request independently.

### Single Source of Truth
Database is the only source of truth for: tasks, conversations, messages. AI agents must never infer or assume state without database reads. Frontend state must always reflect backend responses.

### Authentication & Identity
Better Auth is the only authentication provider. JWT tokens issued by Better Auth are mandatory for: REST task APIs, Chat API. Backend must: verify JWT signature, validate expiration, extract user identity from token. Backend must never trust user_id from request payload alone.

### User Isolation (Hard Rule)
Every task, conversation, and message is owned by exactly one user. All queries must be filtered by authenticated user ID. Cross-user access is strictly forbidden. AI agents must never access or reference another user's data.

## System Overview

The system consists of four cooperating layers:

### Frontend
- Next.js (App Router)
- Standard UI for task management
- ChatKit-based UI for AI chatbot

### Backend
- Python FastAPI
- REST APIs for task management
- Chat API endpoint for AI interaction
- Stateless request handling

### AI Layer
- OpenAI Agents SDK
- Cohere model as the LLM provider
- Agent reasoning + tool invocation only

### MCP Layer
- Official MCP SDK
- Task operations exposed strictly as tools
- Stateless tools with database persistence

## REST API Stability Rule
Existing REST endpoints must not change: URLs, HTTP methods, Request/response semantics. The AI chatbot must integrate without modifying or breaking: Task CRUD behavior, Authorization logic, Database schema (except additive tables for chat).

## Functional Requirements (Mandatory)
The application must implement all 5 Basic Level Todo features plus AI chatbot integration:

1. **Add Task** - Create a new todo item for the authenticated user.
2. **Delete Task** - Remove an existing task owned by the authenticated user.
3. **Update Task** - Modify task title, description, or other editable fields.
4. **View Task List** - Display all tasks belonging to the authenticated user.
5. **Mark as Complete** - Toggle the completion status of a task.
6. **AI Chatbot** - Conversational interface that can interact with tasks via MCP tools.

All features must be accessible via REST API and usable through the frontend UI.

## API Standards
### RESTful Endpoints (Required)
| Method | Endpoint | Description |
|------|--------------------------------------------|---------------------------------|
| GET | /api/{user_id}/tasks | List all user tasks |
| POST | /api/{user_id}/tasks | Create a new task |
| GET | /api/{user_id}/tasks/{id} | Retrieve task details |
| PUT | /api/{user_id}/tasks/{id} | Update an existing task |
| DELETE | /api/{user_id}/tasks/{id} | Delete a task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion status |
| POST | /api/{user_id}/chat | Chat with AI assistant |

## Technology Stack (Fixed)
| Layer | Technology |
|-------------|------------------------------------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | Better Auth + JWT |
| AI Layer | OpenAI Agents SDK + Cohere |
| MCP Layer | Official MCP SDK |
| Spec System | Claude Code + Spec-Kit Plus |

No substitutions are allowed.

## AI & Agent Rules (Critical)

### Agent Capabilities
The AI agent: Can reason over natural language, Can decide which MCP tools to call, Can chain multiple tools in a single turn, Can explain and confirm actions in natural language. The AI agent: Cannot directly access the database, Cannot call REST APIs directly, Cannot fabricate tool results, Cannot modify data without a tool call.

### Tool-Only Action Rule
All state changes must occur via MCP tools. If an action changes tasks: An MCP tool must be invoked, The tool must persist the change, The agent must confirm the action. No exceptions.

### MCP Tool Contract Integrity
MCP tools must be: Stateless, Deterministic, Idempotent where possible. MCP tools must validate: User ownership, Input correctness. MCP tools are the only bridge between AI and the database.

## Conversational Architecture Rules
Chat endpoint: POST /api/{user_id}/chat. Each request must: Load conversation history from DB, Append new user message, Run agent with MCP tools, Persist assistant response, Return response + tool calls. Server must retain no runtime memory.

## Model & AI Provider Rules
OpenAI Agents SDK must be used for: Agent definition, Tool registration, Agent execution. Cohere API key must be used as the LLM provider. Model credentials must: Be read from environment variables, Never be hardcoded. Agent logic must be provider-agnostic where possible.

## Authentication & Authorization
### JWT Verification
FastAPI backend must verify token signature, validate expiration, and decode user identity (user_id, email).

### Shared Secret
JWT signing and verification must use the same secret: BETTER_AUTH_SECRET, stored as environment variables in both frontend and backend.

## Data Storage Rules
All task data must be stored in Neon PostgreSQL. No in-memory or local-only persistence is allowed. Each task record must be associated with a user ID. All conversation and message data must also be stored in the database with proper user isolation.

## Frontend Standards
Responsive UI (mobile + desktop). Frontend must attach JWT token to every API request, never store sensitive secrets, and UI must reflect backend state accurately. Chat interface must support natural language interaction with AI assistant.

## Environment Variables (Mandatory Governance)
All secrets must be supplied via environment variables only: BETTER_AUTH_SECRET, DATABASE_URL, COHERE_API_KEY, OPENAI_DOMAIN_KEY (frontend ChatKit). No secret may appear in: Source code, Logs, Responses, Client-side bundles (except explicitly public keys).

## Error Handling & UX Rules
Errors must be: Gracefully handled, User-safe, Non-leaking (no stack traces). AI must: Explain failures politely, Never blame the system, Never expose internal implementation details.

## Constraints
Must be a fully working web application. Must use REST APIs (no direct DB access from frontend). Must use MCP tools for AI actions (no direct DB access from AI). Stateless backend authentication only (JWT-based). No shared sessions between frontend and backend.

## Out of Scope (System-Wide)
The system will not include: Password handling in backend, Role-based permissions, Cross-user collaboration, Real-time streaming chat, Long-term memory beyond stored conversations, AI fine-tuning, Vendor/product comparisons.

## Success Criteria
The project is considered successful if and only if:
- All 5 required Todo features work correctly.
- All API endpoints require valid JWT authentication.
- Users can only see and modify their own tasks.
- Backend enforces ownership and authorization.
- AI chatbot can interact with tasks via MCP tools.
- Conversations are properly stored and retrieved.
- Application runs without security bypasses.
- Implementation strictly follows all specifications.

## Governance
Any feature, behavior, or code that violates this constitution is considered invalid and must be revised to comply. This document overrides all lower-level specifications and plans.

**Version**: 2.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-15