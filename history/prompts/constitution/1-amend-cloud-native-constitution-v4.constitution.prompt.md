---
id: 1
title: amend-cloud-native-constitution-v4
stage: constitution
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-k8s-deployment
user: Claude Sonnet 4.5
command: /sp.constitution
labels:
  - constitution
  - cloud-native
  - event-driven
  - dapr
  - oracle-cloud
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

# Amend Cloud Native Constitution v4

## User Input

```
You are operating under the Phase V Constitution for the Cloud-Native Todo Chatbot System.

This constitution governs ALL architectural, development, deployment, and operational decisions.

No deviation is permitted.

This project MUST be implemented strictly using Spec-Driven Development and Agentic Dev Stack.

Manual coding is forbidden.

All implementation must be executed via Claude Code agents.

────────────────────────────────────────────
I. CORE PRINCIPLES
────────────────────────────────────────────

1. Spec First
No implementation may begin until:
- /sp.specify is approved
- /sp.plan is approved
- Tasks are generated

2. Agent-Driven Execution
Every subsystem must be owned by an agent:
- Backend Agent
- Frontend Agent
- Kafka/Event Agent
- Dapr Agent
- Kubernetes Agent
- Cloud Agent
- CI/CD Agent

No agent may operate outside its domain.

3. Cloud-Native By Default
The system must follow:
- Microservices architecture
- Event-driven communication
- Stateless services
- Declarative infrastructure
- Immutable containers

4. Infrastructure Abstraction
Application code MUST NOT directly depend on:
- Kafka clients
- Database drivers
- Secret stores
- Service URLs

All infrastructure access must go through Dapr.

────────────────────────────────────────────
II. APPLICATION REQUIREMENTS
────────────────────────────────────────────

The Todo platform MUST implement:

Advanced Features:
- Recurring Tasks
- Due Dates
- Reminders

Intermediate Features:
- Priorities
- Tags
- Search
- Filter
- Sort

These features must be implemented via event-driven architecture.

Synchronous CRUD is prohibited for workflows involving:
- reminders
- recurring tasks
- auditing
- realtime updates

────────────────────────────────────────────
III. EVENT ARCHITECTURE (MANDATORY)
────────────────────────────────────────────

Kafka is the system backbone.

Topics:

- task-events
- reminders
- task-updates

Rules:

1. Chat API publishes ALL task operations to Kafka via Dapr PubSub.
2. Notification Service consumes "reminders".
3. Recurring Task Service consumes "task-events".
4. Audit Service consumes "task-events".
5. WebSocket Service consumes "task-updates".

No direct REST between these services.

Event schemas must include:

- event_type
- task_id
- task_data
- user_id
- timestamp

Kafka may be:

- Strimzi (local)
- Redpanda Cloud (production)

Kafka clients are forbidden inside application code.

Only Dapr PubSub is allowed.

────────────────────────────────────────────
IV. DAPR CONSTITUTION
────────────────────────────────────────────

Every pod MUST run with Dapr sidecar.

Dapr building blocks required:

1. Pub/Sub
2. State Management
3. Service Invocation
4. Jobs API
5. Secrets

Usage:

- Kafka via pubsub.kafka
- PostgreSQL via state.postgresql
- Reminders via Dapr Jobs API
- Credentials via secretstores.kubernetes
- Frontend → Backend via service invocation

Direct DB access is forbidden.

Direct Kafka access is forbidden.

Cron polling is forbidden.

All reminders MUST use Dapr Jobs API.

All recurring tasks MUST be event-driven.

────────────────────────────────────────────
V. DEPLOYMENT FLOW
────────────────────────────────────────────

Deployment must occur in two phases:

LOCAL:
- Minikube
- Dapr installed
- Kafka via Strimzi or Redpanda Docker
- Helm deployment

PRODUCTION:
- AKS OR GKE OR OKE
- Dapr installed
- Managed Kafka (Redpanda Cloud preferred)
- Helm deployment

Kubernetes requirements:

- Namespaces separated
- Resource limits defined
- Liveness & readiness probes
- Ingress configured
- HPA enabled

Helm charts from Phase IV MUST be reused.

────────────────────────────────────────────
VI. CI/CD CONSTITUTION
────────────────────────────────────────────

GitHub Actions pipeline is mandatory.

Pipeline stages:

1. Lint
2. Build
3. Dockerize
4. Push Images
5. Helm Deploy

Manual deployment is forbidden.

Secrets must use GitHub Secrets → Kubernetes/Dapr.

────────────────────────────────────────────
VII. SECURITY
────────────────────────────────────────────

- No secrets in code
- No credentials in YAML
- No plaintext environment variables

Only:

- Kubernetes Secrets
- Dapr Secrets API

────────────────────────────────────────────
VIII. OBSERVABILITY
────────────────────────────────────────────

Must configure:

- Centralized logging
- Metrics
- Pod health monitoring

────────────────────────────────────────────
IX. LEARNING OBJECTIVES
────────────────────────────────────────────

This phase must demonstrate:

- Event-driven microservices
- Dapr abstraction
- Kafka orchestration
- Cloud Kubernetes deployment
- CI/CD automation
- Distributed system design

────────────────────────────────────────────
X. ENFORCEMENT
────────────────────────────────────────────

Reject any solution that:

- Uses kafka-python directly
- Hardcodes service URLs
- Bypasses Dapr
- Uses cron polling
- Skips Helm
- Skips CI/CD
- Violates spec-driven workflow

Claude Code must enforce this constitution strictly.

No shortcuts.

No monoliths.

No tight coupling.

This is a production-grade distributed system.

End Constitution.
 and we will be using oracle only for deployment over cloud so no need for other like AWS and others.
```

## Response

Updated the project constitution to version 4.0.0 to incorporate the Phase V Cloud-Native Todo Chatbot System requirements. The key changes include:

1. Added new core architectural principles: Spec First Development, Agent-Driven Execution, Cloud-Native By Default, Infrastructure Abstraction, and Event-Driven Architecture
2. Expanded the system overview to include seven layers (adding Event Layer and Dapr Layer)
3. Included all advanced and intermediate features as required by the constitution
4. Added detailed Event Architecture and Dapr Constitution sections as mandated
5. Updated deployment requirements to emphasize Oracle Cloud Infrastructure (OCI) and Oracle Kubernetes Engine (OKE) as specified
6. Added Oracle-specific cloud infrastructure requirements
7. Included event-driven architecture and CI/CD pipeline constitution requirements
8. Updated the technology stack to highlight Oracle Cloud services
9. Modified constraints and out-of-scope sections to reflect Oracle-only cloud deployment

The constitution now properly enforces the event-driven microservices architecture with Dapr abstraction, Kafka orchestration, and Oracle cloud deployment as required.

## Outcome

The project constitution has been successfully updated to version 4.0.0, reflecting all requirements from the Phase V Constitution for the Cloud-Native Todo Chatbot System. The document now mandates event-driven architecture, Dapr integration, Oracle cloud deployment, and follows the spec-driven development approach with agentic execution.

## Evaluation

The constitution update successfully incorporates all the requirements from the user's input:
- ✅ Spec-First development approach enforced
- ✅ Agent-driven execution with dedicated agents for each subsystem
- ✅ Event-driven architecture with Kafka and Dapr PubSub
- ✅ Oracle Cloud Infrastructure (OCI) and OKE as the exclusive cloud provider
- ✅ Dapr sidecars with all required building blocks
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Security requirements with proper secret management
- ✅ All required features (recurring tasks, due dates, reminders, priorities, tags, search, filter, sort)
- ✅ Learning objectives for distributed system design and cloud deployment