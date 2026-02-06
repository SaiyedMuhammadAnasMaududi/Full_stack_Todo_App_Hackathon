<!-- Sync Impact Report:
Version change: 2.0.0 → 3.0.0
Modified principles: Core Architectural Principles expanded with cloud-native requirements, added Containerization and Kubernetes principles
Added sections: Cloud-Native Deployment, Containerization Requirements, Kubernetes Requirements, AI DevOps Requirements, Agentic DevOps Workflows, Technology Stack additions for cloud-native deployment
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Cloud Native AI Todo Chatbot - Phase IV Constitution

## Core Architectural Principles (Non-Negotiable)

### Statelessness
No server-side session memory is allowed. No in-memory conversation state may persist between requests. All conversational state must be stored in the database. Any server instance must be able to handle any request independently. This principle must be maintained in containerized environments.

### Single Source of Truth
Database is the only source of truth for: tasks, conversations, messages. AI agents must never infer or assume state without database reads. Frontend state must always reflect backend responses. This principle must be preserved across containerized deployments.

### Authentication & Identity
Better Auth is the only authentication provider. JWT tokens issued by Better Auth are mandatory for: REST task APIs, Chat API. Backend must: verify JWT signature, validate expiration, extract user identity from token. Backend must never trust user_id from request payload alone. This must work consistently across containerized services.

### User Isolation (Hard Rule)
Every task, conversation, and message is owned by exactly one user. All queries must be filtered by authenticated user ID. Cross-user access is strictly forbidden. AI agents must never access or reference another user's data. This must be enforced consistently across all containerized services.

### Cloud-Native Scalability
The system must be designed to scale horizontally across multiple container instances. No shared state between containers. All state must be externalized to databases or shared storage. Services must be resilient to container restarts and scaling events.

### Containerization Integrity
All services must run in containers. No direct installation of application code on hosts. All dependencies must be packaged within containers. External configuration via environment variables or ConfigMaps/Secrets only. This ensures consistent deployments across environments.

## System Overview

The system consists of five cooperating layers:

### Frontend
- Next.js (App Router)
- Standard UI for task management
- ChatKit-based UI for AI chatbot
- Containerized in Docker with production-ready build

### Backend
- Python FastAPI
- REST APIs for task management
- Chat API endpoint for AI interaction
- Stateless request handling
- Containerized in Docker with production-ready configuration

### AI Layer
- OpenAI Agents SDK
- Cohere model as the LLM provider
- Agent reasoning + tool invocation only
- Containerized with proper resource allocation

### MCP Layer
- Official MCP SDK
- Task operations exposed strictly as tools
- Stateless tools with database persistence
- Containerized service for MCP operations

### Infrastructure Layer
- Docker Desktop for containerization
- Minikube for local Kubernetes cluster
- Helm for deployment management
- kubectl-ai and Kagent for AI-assisted operations

## REST API Stability Rule
Existing REST endpoints must not change: URLs, HTTP methods, Request/response semantics. The AI chatbot must integrate without modifying or breaking: Task CRUD behavior, Authorization logic, Database schema (except additive tables for chat). This stability must be maintained across containerized deployments.

## Functional Requirements (Mandatory)
The application must implement all 5 Basic Level Todo features plus AI chatbot integration:

1. **Add Task** - Create a new todo item for the authenticated user.
2. **Delete Task** - Remove an existing task owned by the authenticated user.
3. **Update Task** - Modify task title, description, or other editable fields.
4. **View Task List** - Display all tasks belonging to the authenticated user.
5. **Mark as Complete** - Toggle the completion status of a task.
6. **AI Chatbot** - Conversational interface that can interact with tasks via MCP tools.

All features must be accessible via REST API and usable through the frontend UI, accessible from containerized services.

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
| Containerization | Docker Desktop |
| Docker AI | Gordon (Docker AI Agent) |
| Kubernetes | Minikube |
| Packaging | Helm Charts |
| AI DevOps | kubectl-ai + Kagent |
| Protocol | MCP |
| Spec System | Claude Code + Spec-Kit Plus |

No substitutions are allowed. All operations must follow the Agentic Dev Stack: Spec → Plan → Tasks → Claude Code Execution.

## AI & Agent Rules (Critical)

### Agent Capabilities
The AI agent: Can reason over natural language, Can decide which MCP tools to call, Can chain multiple tools in a single turn, Can explain and confirm actions in natural language. The AI agent: Cannot directly access the database, Cannot call REST APIs directly, Cannot fabricate tool results, Cannot modify data without a tool call.

### Tool-Only Action Rule
All state changes must occur via MCP tools. If an action changes tasks: An MCP tool must be invoked, The tool must persist the change, The agent must confirm the action. No exceptions. This rule must be preserved in containerized environments.

### MCP Tool Contract Integrity
MCP tools must be: Stateless, Deterministic, Idempotent where possible. MCP tools must validate: User ownership, Input correctness. MCP tools are the only bridge between AI and the database. Tools must be accessible from containerized services.

## Conversational Architecture Rules
Chat endpoint: POST /api/{user_id}/chat. Each request must: Load conversation history from DB, Append new user message, Run agent with MCP tools, Persist assistant response, Return response + tool calls. Server must retain no runtime memory. This architecture must work in containerized environments.

## Model & AI Provider Rules
OpenAI Agents SDK must be used for: Agent definition, Tool registration, Agent execution. Cohere API key must be used as the LLM provider. Model credentials must: Be read from environment variables, Never be hardcoded. Agent logic must be provider-agnostic where possible. Credentials must be securely managed in Kubernetes Secrets.

## Authentication & Authorization
### JWT Verification
FastAPI backend must verify token signature, validate expiration, and decode user identity (user_id, email). This must work consistently across containerized services.

### Shared Secret
JWT signing and verification must use the same secret: BETTER_AUTH_SECRET, stored as environment variables in both frontend and backend, and as Kubernetes Secrets in the cluster.

## Data Storage Rules
All task data must be stored in Neon PostgreSQL. No in-memory or local-only persistence is allowed. Each task record must be associated with a user ID. All conversation and message data must also be stored in the database with proper user isolation. Database connectivity must work reliably from containerized services.

## Containerization Requirements
Frontend and backend MUST:
- Be containerized via Gordon or Claude Code
- Use production-grade images
- Include health checks
- Externalize secrets
- Support environment variables
- Avoid hardcoded credentials
- Be optimized for minimal image size
- Include proper logging mechanisms
- Support graceful shutdown
- Be compatible with Kubernetes deployment

## Kubernetes Deployment Requirements
Helm Charts MUST include:
- Deployments
- Services
- ConfigMaps
- Secrets
- Resource limits
- Replica configuration
- Health checks (liveness and readiness probes)
- Horizontal Pod Autoscaling (HPA) configurations
- Network policies (if required)
- Persistent volumes (if needed for any stateful components)

## Frontend Standards
Responsive UI (mobile + desktop). Frontend must attach JWT token to every API request, never store sensitive secrets, and UI must reflect backend state accurately. Chat interface must support natural language interaction with AI assistant. Frontend must be served through containerized web server with proper caching headers.

## Environment Variables (Mandatory Governance)
All secrets must be supplied via environment variables only: BETTER_AUTH_SECRET, DATABASE_URL, COHERE_API_KEY, OPENAI_DOMAIN_KEY (frontend ChatKit). No secret may appear in: Source code, Logs, Responses, Client-side bundles (except explicitly public keys). In Kubernetes, secrets must be stored in Kubernetes Secrets and mounted as environment variables or volume mounts.

## Error Handling & UX Rules
Errors must be: Gracefully handled, User-safe, Non-leaking (no stack traces). AI must: Explain failures politely, Never blame the system, Never expose internal implementation details. Containerized services must have proper error logging and monitoring.

## Agentic DevOps Requirements
### Absolute Rules
❌ No manual coding
❌ No handwritten Dockerfiles
❌ No handwritten Helm YAML
❌ No manual kubectl commands
❌ No direct cluster manipulation

All operations MUST be performed using:

- Claude Code
- Docker AI Agent (Gordon)
- kubectl-ai
- Kagent

### AI DevOps Enforcement

#### kubectl-ai
Used for:
- Deployment
- Scaling
- Debugging

#### Kagent
Used for:
- Cluster health
- Resource optimization

Manual kubectl forbidden.

## Constraints
Must be a fully working web application. Must use REST APIs (no direct DB access from frontend). Must use MCP tools for AI actions (no direct DB access from AI). Stateless backend authentication only (JWT-based). No shared sessions between frontend and backend. Must run in containerized Kubernetes environment. No manual operations allowed during deployment.

## Out of Scope (System-Wide)
The system will not include: Password handling in backend, Role-based permissions, Cross-user collaboration, Real-time streaming chat, Long-term memory beyond stored conversations, AI fine-tuning, Vendor/product comparisons, Manual kubectl commands, Direct cluster manipulation.

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
- Containers built successfully.
- Helm charts deployed successfully.
- Minikube running successfully.
- Frontend accessible from Kubernetes service.
- Backend responding from Kubernetes service.
- Chatbot functional in containerized environment.
- MCP tools working in Kubernetes deployment.
- kubectl-ai managing cluster successfully.
- Kagent reporting health successfully.
- Phase III functionality preserved in containerized deployment.

## Governance
Any feature, behavior, or code that violates this constitution is considered invalid and must be revised to comply. This document overrides all lower-level specifications and plans. All operations must follow the Agentic Dev Stack: Spec → Plan → Tasks → Claude Code Execution.

**Version**: 3.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-02-05