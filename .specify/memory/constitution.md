<!-- Sync Impact Report:
Version change: 3.0.0 → 4.0.0
Modified principles: Core Architectural Principles expanded with event-driven and Dapr requirements, added Cloud-Native deployment with Oracle-specific requirements
Added sections: Event Architecture, Dapr Constitution, Oracle Cloud Deployment, CI/CD Pipeline requirements
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Cloud Native AI Todo Chatbot - Phase V Constitution

## Core Architectural Principles (Non-Negotiable)

### Spec First Development
No implementation may begin until: `/sp.specify` is approved, `/sp.plan` is approved, and tasks are generated. All development must follow the Spec-Driven Development methodology with Claude Code agents. This principle ensures systematic and well-planned development.

### Agent-Driven Execution
Every subsystem must be owned by an agent: Backend Agent, Frontend Agent, Kafka/Event Agent, Dapr Agent, Kubernetes Agent, Cloud Agent, CI/CD Agent. No agent may operate outside its domain. Manual coding is forbidden - all implementation must be executed via Claude Code agents.

### Cloud-Native By Default
The system must follow: microservices architecture, event-driven communication, stateless services, declarative infrastructure, immutable containers. This principle ensures scalable and maintainable architecture patterns.

### Infrastructure Abstraction
Application code MUST NOT directly depend on: Kafka clients, database drivers, secret stores, service URLs. All infrastructure access must go through Dapr. This creates proper abstraction layers and reduces coupling to specific implementations.

### Event-Driven Architecture
All task operations must be published to Kafka via Dapr PubSub. No synchronous CRUD operations for reminders, recurring tasks, auditing, or real-time updates. This ensures loose coupling and asynchronous processing capabilities.

## System Overview

The system consists of seven cooperating layers:

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

### Event Layer
- Apache Kafka/Redpanda for messaging
- Dapr PubSub integration
- Task events, reminders, and updates topics
- Event-driven microservices communication

### Dapr Layer
- Dapr sidecar in every pod
- PubSub, State Management, Service Invocation, Jobs API, Secrets building blocks
- Infrastructure abstraction layer
- Event-driven processing capabilities

### Infrastructure Layer
- Docker Desktop for containerization
- Minikube for local Kubernetes cluster
- Oracle Kubernetes Engine (OKE) for production
- Helm for deployment management
- Oracle Cloud Infrastructure (OCI) for managed services

## REST API Stability Rule
Existing REST endpoints must not change: URLs, HTTP methods, Request/response semantics. The AI chatbot must integrate without modifying or breaking: Task CRUD behavior, Authorization logic, Database schema (except additive tables for chat). This stability must be maintained across containerized deployments.

## Functional Requirements (Mandatory)
The application must implement all 5 Basic Level Todo features plus advanced features:

1. **Add Task** - Create a new todo item for the authenticated user.
2. **Delete Task** - Remove an existing task owned by the authenticated user.
3. **Update Task** - Modify task title, description, or other editable fields.
4. **View Task List** - Display all tasks belonging to the authenticated user.
5. **Mark as Complete** - Toggle the completion status of a task.
6. **AI Chatbot** - Conversational interface that can interact with tasks via MCP tools.
7. **Recurring Tasks** - Automated creation of recurring task instances.
8. **Due Dates** - Date-based task scheduling and reminders.
9. **Reminders** - Timely notifications for upcoming tasks.
10. **Priorities** - Task priority levels for sorting and organization.
11. **Tags** - Categorization and filtering of tasks.
12. **Search** - Text-based search across all tasks.
13. **Filter** - Filtering by various criteria (status, priority, tags).
14. **Sort** - Sorting by various criteria (date, priority, title).

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
| Messaging | Apache Kafka / Redpanda |
| Orchestration | Dapr Runtime |
| Kubernetes | Minikube (local), Oracle Kubernetes Engine (OKE) |
| Cloud | Oracle Cloud Infrastructure (OCI) |
| Packaging | Helm Charts |
| AI DevOps | kubectl-ai + Kagent |
| Protocol | MCP |
| Spec System | Claude Code + Spec-Kit Plus |

No substitutions are allowed. All operations must follow the Agentic Dev Stack: Spec → Plan → Tasks → Claude Code Execution.

## Event Architecture (Mandatory)
Kafka is the system backbone with topics: task-events, reminders, task-updates. Rules: 1. Chat API publishes ALL task operations to Kafka via Dapr PubSub. 2. Notification Service consumes "reminders". 3. Recurring Task Service consumes "task-events". 4. Audit Service consumes "task-events". 5. WebSocket Service consumes "task-updates". No direct REST between these services. Event schemas must include: event_type, task_id, task_data, user_id, timestamp. Kafka may be: Strimzi (local) or Redpanda Cloud (production). Kafka clients are forbidden inside application code - only Dapr PubSub is allowed.

## Dapr Constitution
Every pod MUST run with Dapr sidecar. Dapr building blocks required: 1. Pub/Sub 2. State Management 3. Service Invocation 4. Jobs API 5. Secrets. Usage: Kafka via pubsub.kafka, PostgreSQL via state.postgresql, Reminders via Dapr Jobs API, Credentials via secretstores.kubernetes, Frontend → Backend via service invocation. Direct DB access is forbidden. Direct Kafka access is forbidden. Cron polling is forbidden. All reminders MUST use Dapr Jobs API. All recurring tasks MUST be event-driven.

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

## Oracle Cloud Infrastructure (OCI) Deployment Requirements
Production deployment MUST use:
- Oracle Kubernetes Engine (OKE)
- Oracle Cloud Infrastructure (OCI) managed services
- Oracle Streaming (managed Kafka alternative)
- Oracle Autonomous Database (alternative to Neon PostgreSQL)
- Oracle Container Registry (OCR) for Docker images
- OCI Load Balancer for traffic distribution
- OCI DNS for domain management
- OCI Vault for secret management
- OCI Logging for centralized logging
- OCI Monitoring for metrics and alarms

## Event-Driven Architecture Requirements
All services MUST implement:
- Event publishing via Dapr PubSub to Kafka
- Event consumption via Dapr PubSub from Kafka
- Proper event schema definition and validation
- Event-driven processing patterns
- Saga patterns for distributed transactions
- Circuit breakers for fault tolerance
- Retry mechanisms with exponential backoff
- Dead letter queues for failed events
- Idempotency for event processing

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

## CI/CD Pipeline Constitution
GitHub Actions pipeline is mandatory. Pipeline stages: 1. Lint 2. Build 3. Dockerize 4. Push Images 5. Helm Deploy. Manual deployment is forbidden. Secrets must use GitHub Secrets → Kubernetes/Dapr. Pipeline must support: Docker image building, Image tagging and versioning, Image pushing to registry, Helm chart packaging, Helm deployment to clusters, Environment promotion, Automated testing, Security scanning, Performance testing.

## Security Requirements
- No secrets in code
- No credentials in YAML
- No plaintext environment variables
- Use only Kubernetes Secrets and Dapr Secrets API
- Enable mTLS between Dapr services
- Configure proper RBAC permissions
- Implement network policies
- Enable Pod Security Standards
- Configure security scanning for images
- Enable audit logging
- Encrypt data in transit and at rest
- Implement access controls and authentication

## Observability Requirements
Must configure:
- Centralized logging via OCI Logging or Fluentd/Elasticsearch
- Metrics collection via Prometheus/Grafana or OCI Monitoring
- Distributed tracing via Jaeger/Zipkin
- Pod health monitoring via liveness/readiness probes
- Application performance monitoring
- Business metrics and KPIs
- Alerting and notification systems
- Log aggregation and analysis
- Performance dashboards
- Audit trails for compliance

## Constraints
Must be a fully working web application. Must use REST APIs (no direct DB access from frontend). Must use MCP tools for AI actions (no direct DB access from AI). Stateless backend authentication only (JWT-based). No shared sessions between frontend and backend. Must run in containerized Kubernetes environment. No manual operations allowed during deployment. All event-driven communication must go through Dapr. No direct Kafka or database access from application code.

## Out of Scope (System-Wide)
The system will not include: Password handling in backend, Role-based permissions, Cross-user collaboration, Real-time streaming chat, Long-term memory beyond stored conversations, AI fine-tuning, Vendor/product comparisons, Manual kubectl commands, Direct cluster manipulation, AWS or Azure services (Oracle only).

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
- Event-driven architecture implemented correctly.
- Dapr integration working properly.
- Kafka/Redpanda messaging functional.
- Recurring tasks working via events.
- Reminders working via Dapr Jobs API.
- Due dates and scheduling functional.
- Priority, tags, search, filter, sort features working.
- Containers built successfully.
- Helm charts deployed successfully.
- Minikube running successfully locally.
- OKE cluster running successfully in OCI.
- Frontend accessible from Kubernetes service.
- Backend responding from Kubernetes service.
- Chatbot functional in containerized environment.
- MCP tools working in Kubernetes deployment.
- kubectl-ai managing cluster successfully.
- Kagent reporting health successfully.
- Phase III functionality preserved in containerized deployment.

## Learning Objectives
This phase must demonstrate:
- Event-driven microservices
- Dapr abstraction
- Kafka orchestration
- Cloud Kubernetes deployment (Oracle OKE)
- CI/CD automation
- Distributed system design
- Oracle Cloud Infrastructure integration
- Microservices communication patterns

## Governance
Any feature, behavior, or code that violates this constitution is considered invalid and must be revised to comply. This document overrides all lower-level specifications and plans. All operations must follow the Agentic Dev Stack: Spec → Plan → Tasks → Claude Code Execution.

**Version**: 4.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-02-06