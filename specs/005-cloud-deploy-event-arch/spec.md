# Feature Specification: Cloud Deployment & Event-Driven Architecture (Phase V)

**Feature Branch**: `005-cloud-deploy-event-arch`
**Created**: 2026-02-07
**Status**: Draft
**Input**: Phase V Cloud Deployment with Event-Driven Architecture using Dapr, Kafka, Oracle OKE, Minikube, Helm, and CI/CD

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Containerized Local Deployment (Priority: P1)

Developer builds Docker images for frontend and backend, deploys to Minikube via Helm charts, and accesses the full Todo application from Kubernetes services.

**Why this priority**: Without containerization and local K8s, no other Phase V work can proceed. This is the foundation.

**Independent Test**: Run `helm install` on Minikube, verify frontend loads at NodePort, backend health check returns 200, task CRUD works end-to-end.

**Acceptance Scenarios**:

1. **Given** Docker images are built, **When** `helm install todo-app ./charts` runs on Minikube, **Then** frontend and backend pods reach Running state with health checks passing.
2. **Given** app is deployed to Minikube, **When** user navigates to frontend URL, **Then** login, task CRUD, and AI chat work identically to non-containerized version.
3. **Given** backend pod is running, **When** `/health` is called, **Then** returns `{"status": "healthy"}` with 200 status.

---

### User Story 2 - Dapr Integration for Infrastructure Abstraction (Priority: P1)

Backend services communicate through Dapr sidecars instead of direct DB/Kafka/service calls. Dapr PubSub publishes task events, State Store manages state, Service Invocation handles inter-service calls, and Secrets API manages credentials.

**Why this priority**: Dapr is the mandatory abstraction layer per constitution. All event-driven features depend on it.

**Independent Test**: Deploy with Dapr enabled, verify task creation publishes event via Dapr PubSub, state is accessible via Dapr State API, secrets load via Dapr Secrets API.

**Acceptance Scenarios**:

1. **Given** Dapr sidecar is running alongside backend, **When** a task is created, **Then** a `task-created` event is published to Kafka via Dapr PubSub.
2. **Given** Dapr Secrets component is configured, **When** backend starts, **Then** DATABASE_URL and BETTER_AUTH_SECRET are loaded via Dapr Secrets API.
3. **Given** Dapr Service Invocation is configured, **When** frontend calls backend, **Then** the call routes through Dapr service invocation.

---

### User Story 3 - Event-Driven Task Processing (Priority: P2)

Task operations (create, update, delete, complete) publish events to Kafka topics via Dapr PubSub. Downstream services (reminders, recurring tasks, audit) consume events asynchronously.

**Why this priority**: Core event-driven architecture that enables reminders, recurring tasks, and audit trail without synchronous coupling.

**Independent Test**: Create a task, verify event appears on `task-events` topic, verify reminder service schedules reminder via Dapr Jobs API, verify audit service logs the event.

**Acceptance Scenarios**:

1. **Given** a task with `reminder_at` is created, **When** the event is consumed by Reminder Service, **Then** a Dapr Job is scheduled for the reminder time.
2. **Given** a recurring task is completed, **When** the event is consumed by Recurring Task Service, **Then** the next instance is automatically created.
3. **Given** any task operation occurs, **When** the event is consumed by Audit Service, **Then** an audit record is persisted with event_type, task_id, user_id, timestamp.

---

### User Story 4 - Oracle Cloud (OKE) Production Deployment (Priority: P2)

Application is deployed to Oracle Kubernetes Engine with OCI managed services: OCI Load Balancer, Oracle Container Registry, OCI Vault for secrets, OCI Monitoring/Logging.

**Why this priority**: Production deployment target. Demonstrates cloud-native capabilities.

**Independent Test**: Deploy Helm charts to OKE cluster, verify frontend is accessible via OCI Load Balancer, backend serves API requests, Kafka messaging works.

**Acceptance Scenarios**:

1. **Given** Helm charts are packaged, **When** deployed to OKE, **Then** all pods reach Running state with Dapr sidecars injected.
2. **Given** OCI Load Balancer is configured, **When** user accesses the public URL, **Then** frontend loads and connects to backend API.
3. **Given** OCI Vault is configured, **When** backend starts in OKE, **Then** secrets are mounted from OCI Vault via Dapr Secrets.

---

### User Story 5 - CI/CD Pipeline Automation (Priority: P3)

GitHub Actions pipeline automates: lint, build, Dockerize, push images, Helm deploy. No manual deployment allowed.

**Why this priority**: Automation ensures reproducible deployments. Required by constitution but depends on Stories 1-4.

**Independent Test**: Push code to main branch, verify pipeline runs all stages, images are pushed to registry, Helm deployment succeeds.

**Acceptance Scenarios**:

1. **Given** code is pushed to main, **When** GitHub Actions triggers, **Then** lint, build, Docker build, push, and Helm deploy stages all pass.
2. **Given** pipeline completes, **When** checking the cluster, **Then** new image version is running in pods.
3. **Given** a deployment fails, **When** pipeline detects failure, **Then** it rolls back to previous version and notifies via GitHub status.

---

### Edge Cases

- What happens when Dapr sidecar is unavailable? Backend must fail gracefully with appropriate error messages.
- How does the system handle Kafka broker downtime? Dapr retry policies with exponential backoff; events are not lost.
- What if OKE node pool runs out of resources? HPA must scale pods, and alerts must fire via OCI Monitoring.
- How does migration work from SQLite (local) to Neon PostgreSQL (prod)? Environment variable switches DATABASE_URL; schema auto-migrates on startup.
- What if a recurring task event is processed twice? Idempotent event processing ensures no duplicate tasks.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST containerize frontend (Next.js) and backend (FastAPI) as production-grade Docker images with health checks.
- **FR-002**: System MUST deploy to Minikube locally via Helm charts with Dapr sidecar injection.
- **FR-003**: System MUST publish all task CRUD events to Kafka via Dapr PubSub (topics: task-events, reminders, task-updates).
- **FR-004**: System MUST consume task events for: Reminder scheduling (Dapr Jobs API), Recurring task creation, Audit logging.
- **FR-005**: System MUST use Dapr Secrets API for all credential management (DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY).
- **FR-006**: System MUST use Dapr State Management for any state storage needs beyond the primary database.
- **FR-007**: System MUST use Dapr Service Invocation for inter-service communication.
- **FR-008**: System MUST deploy to Oracle Kubernetes Engine (OKE) with OCI managed services.
- **FR-009**: System MUST implement CI/CD via GitHub Actions (lint, build, Dockerize, push, Helm deploy).
- **FR-010**: System MUST preserve all Phase III/IV functionality (task CRUD, AI chatbot, MCP tools, advanced features) in containerized deployment.
- **FR-011**: System MUST implement event schemas with: event_type, task_id, task_data, user_id, timestamp.
- **FR-012**: System MUST implement idempotent event processing with deduplication.
- **FR-013**: System MUST configure HPA for backend pods (min: 2, max: 10, target CPU: 70%).
- **FR-014**: System MUST implement liveness and readiness probes for all services.
- **FR-015**: System MUST implement circuit breakers and retry policies via Dapr resiliency.

### Key Entities

- **TaskEvent**: Event published to Kafka (event_type, task_id, task_data, user_id, timestamp, correlation_id)
- **DaprComponent**: Configuration for PubSub (Kafka), State (PostgreSQL), Secrets (K8s/OCI Vault), Jobs
- **HelmRelease**: Deployment unit with values for each environment (local/minikube, production/OKE)
- **Pipeline**: GitHub Actions workflow with stages (lint, build, docker, push, deploy)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Frontend and backend Docker images build in under 5 minutes each.
- **SC-002**: Helm install on Minikube succeeds with all pods Running within 3 minutes.
- **SC-003**: Task CRUD operations publish events to Kafka within 100ms via Dapr PubSub.
- **SC-004**: Reminder service schedules Dapr Jobs within 500ms of event consumption.
- **SC-005**: Recurring task creation happens within 1 second of triggering event.
- **SC-006**: OKE deployment via Helm succeeds with zero downtime.
- **SC-007**: CI/CD pipeline completes full cycle (lint to deploy) in under 15 minutes.
- **SC-008**: All Phase III/IV features pass regression testing in containerized environment.
- **SC-009**: System handles 100 concurrent users with p95 latency under 500ms.
- **SC-010**: Zero secrets exposed in code, logs, or container images.
