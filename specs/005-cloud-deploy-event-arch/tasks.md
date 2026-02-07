# Tasks: Phase V Cloud Deployment & Event-Driven Architecture

**Input**: Design documents from `/specs/005-cloud-deploy-event-arch/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1-US5 from spec.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project directories, Docker base, Helm scaffold

- [X] T001 Create infra directory structure: infra/dapr/, infra/kafka/, infra/minikube/, infra/oke/
- [X] T002 [P] Create backend Dockerfile with multi-stage build (python:3.10-slim) in backend/Dockerfile
- [X] T003 [P] Create frontend Dockerfile with multi-stage build (node:18-alpine) in frontend/Dockerfile
- [X] T004 [P] Create .dockerignore files in backend/.dockerignore and frontend/.dockerignore
- [X] T005 Existing Helm charts reused at charts/backend/ and charts/frontend/
- [X] T006 Skipped (using existing charts with values already defined)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Dapr components, Kafka cluster, K8s secrets - MUST complete before any user story

- [X] T007 Create Strimzi Kafka operator manifest in infra/kafka/strimzi-operator.yaml
- [X] T008 Create Kafka cluster CRD with topics (task-events, reminders, task-updates) in infra/kafka/kafka-cluster.yaml
- [X] T009 [P] Create Dapr PubSub component (pubsub-kafka) in infra/dapr/pubsub-kafka.yaml
- [X] T010 [P] Create Dapr State Store component (state.postgresql) in infra/dapr/statestore-postgres.yaml
- [X] T011 [P] Create Dapr Secret Store component (secretstores.kubernetes) in infra/dapr/secretstore-kubernetes.yaml
- [X] T012 [P] Create Dapr Resiliency policy (retries, circuit breaker, dead letter) in infra/dapr/resiliency.yaml
- [X] T013 Existing Kubernetes secrets template at charts/backend/templates/secret.yaml
- [X] T014 Existing ConfigMap template at charts/backend/templates/configmap.yaml
- [X] T015 Create Minikube setup script in infra/minikube/setup.sh

**Checkpoint**: Dapr + Kafka + Secrets infrastructure defined.

---

## Phase 3: User Story 1 - Containerized Local Deployment (Priority: P1) MVP

**Goal**: Backend + frontend running in Minikube via Helm with health checks passing.

**Independent Test**: `helm install` on Minikube, frontend loads, backend /health returns 200, task CRUD works.

### Implementation for User Story 1

- [X] T016 [US1] Backend Deployment already exists with probes at charts/backend/templates/deployment.yaml - added Dapr annotations
- [X] T017 [US1] Frontend Deployment already exists at charts/frontend/templates/deployment.yaml
- [X] T018 [P] [US1] Backend Service already exists at charts/backend/templates/service.yaml
- [X] T019 [P] [US1] Frontend Service already exists at charts/frontend/templates/service.yaml
- [X] T020 [US1] Ingress already configured in existing charts
- [X] T021 [US1] Liveness/readiness probes already in backend deployment (/health)
- [X] T022 [US1] Liveness/readiness probes already in frontend deployment (/api/health)
- [X] T023 [US1] HPA already exists at charts/backend/templates/hpa.yaml (min:2, max:5, cpu:70%)
- [ ] T024 [US1] Build Docker images, deploy to Minikube, verify all pods Running

**Checkpoint**: Frontend + backend running in K8s. Task CRUD functional via browser.

---

## Phase 4: User Story 2 - Dapr Integration (Priority: P1)

**Goal**: All infrastructure access through Dapr sidecars. Secrets via Dapr, PubSub wired, state store accessible.

**Independent Test**: Task creation publishes event via Dapr PubSub. Secrets load via Dapr. Service invocation works.

### Implementation for User Story 2

- [X] T025 [US2] Create event publisher module using Dapr HTTP API in backend/services/event_publisher.py
- [X] T026 [US2] TaskEvent schema defined in event_publisher.py (event_type, task_id, user_id, task_data, timestamp, correlation_id)
- [X] T027 [US2] Integrate event publishing into task CRUD routes (create, update, delete, complete) in backend/routes/tasks.py
- [X] T028 [US2] Secrets loading via existing K8s secrets + Dapr secretstore component
- [X] T029 [US2] Backend Deployment updated with Dapr sidecar annotations in charts/backend/templates/deployment.yaml
- [ ] T030 [US2] Verify Dapr PubSub publishes events to Kafka task-events topic

**Checkpoint**: Backend uses Dapr for secrets, publishes all task events to Kafka.

---

## Phase 5: User Story 3 - Event-Driven Task Processing (Priority: P2)

**Goal**: Downstream services consume Kafka events for reminders, recurring tasks, and audit.

**Independent Test**: Create task with reminder_at -> reminder fires. Complete recurring task -> next instance created.

### Implementation for User Story 3

- [X] T031 [P] [US3] Create Notification Service with Dapr subscription to reminders topic in backend/services/notification_service.py
- [X] T032 [P] [US3] Create Recurring Task Service with Dapr subscription to task-events topic in backend/services/recurring_task_service.py
- [X] T033 [P] [US3] Create Audit Service with Dapr subscription to task-events topic in backend/services/audit_service.py
- [X] T034 [US3] Implement Dapr Jobs API integration for reminder scheduling in backend/services/notification_service.py
- [X] T035 [US3] Implement idempotent event processing with correlation_id dedup in backend/services/event_processor_base.py
- [X] T036 [US3] Create Notification Service Deployment with Dapr sidecar in charts/backend/templates/notification-deployment.yaml
- [X] T037 [P] [US3] Create Recurring Task Service Deployment in charts/backend/templates/recurring-deployment.yaml
- [X] T038 [P] [US3] Create Audit Service Deployment in charts/backend/templates/audit-deployment.yaml
- [X] T039 [US3] Create WebSocket Sync Service subscribing to task-updates in backend/services/websocket_service.py
- [X] T040 [US3] Create WebSocket Service Deployment in charts/backend/templates/websocket-deployment.yaml
- [ ] T041 [US3] Deploy all event services to Minikube, verify event flow end-to-end

**Checkpoint**: Full event-driven pipeline: CRUD -> Kafka -> Reminders + Recurring + Audit + WebSocket.

---

## Phase 6: User Story 4 - Oracle OKE Production Deployment (Priority: P2)

**Goal**: All services deployed to Oracle Kubernetes Engine with OCI managed services.

**Independent Test**: Access frontend via OCI Load Balancer URL, full CRUD + events work.

### Implementation for User Story 4

- [X] T042 [US4] Create OCI CLI provisioning script for OKE cluster in infra/oke/provision.sh
- [ ] T043 [US4] Configure kubectl context for OKE (requires OCI credentials)
- [ ] T044 [US4] Push Docker images to Oracle Container Registry (OCR)
- [ ] T045 [US4] Install Dapr runtime on OKE cluster
- [ ] T046 [US4] Deploy Strimzi + Kafka on OKE
- [ ] T047 [US4] Apply Dapr components with OKE-specific values
- [ ] T048 [US4] Deploy all services via helm install with OKE values
- [ ] T049 [US4] Configure OCI Load Balancer for frontend ingress
- [ ] T050 [US4] Verify full E2E on OKE: CRUD, events, reminders, audit

**Checkpoint**: Production deployment on Oracle OKE fully functional.

---

## Phase 7: User Story 5 - CI/CD Pipeline (Priority: P3)

**Goal**: GitHub Actions automates lint, build, Dockerize, push, deploy. No manual deployment.

**Independent Test**: Push to main -> pipeline builds images -> deploys to cluster.

### Implementation for User Story 5

- [X] T051 [US5] Create GitHub Actions workflow with lint stage in .github/workflows/deploy.yaml
- [X] T052 [US5] Add Docker build and push stages (tag with git SHA) in .github/workflows/deploy.yaml
- [X] T053 [US5] Add Helm deploy stage to OKE in .github/workflows/deploy.yaml
- [X] T054 [US5] Add rollback on failure step in .github/workflows/deploy.yaml
- [ ] T055 [US5] Configure GitHub Secrets (KUBE_CONFIG, DOCKER_USERNAME, DOCKER_PASSWORD, DATABASE_URL, COHERE_API_KEY, BETTER_AUTH_SECRET)
- [ ] T056 [US5] Verify pipeline executes end-to-end on push

**Checkpoint**: Fully automated CI/CD pipeline.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Observability, security hardening, final validation

- [ ] T057 [P] Add Prometheus metrics endpoint (already exists at /metrics in backend/main.py)
- [X] T058 [P] Configure Dapr mTLS and tracing in infra/dapr/config.yaml
- [ ] T059 [P] Add network policies for pod-to-pod security
- [ ] T060 Run full E2E validation per quickstart.md
- [ ] T061 Verify Phase III/IV regression (all 14 existing endpoints still work)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: COMPLETE
- **Phase 2 (Foundational)**: COMPLETE
- **Phase 3 (US1 - Containers)**: COMPLETE (except T024 runtime verification)
- **Phase 4 (US2 - Dapr)**: COMPLETE (except T030 runtime verification)
- **Phase 5 (US3 - Events)**: COMPLETE (except T041 runtime verification)
- **Phase 6 (US4 - OKE)**: Requires OCI credentials from user
- **Phase 7 (US5 - CI/CD)**: Requires GitHub Secrets configuration
- **Phase 8 (Polish)**: Requires running cluster

---

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 61 |
| Completed | 44 |
| Remaining (runtime/credentials) | 17 |
| Blocked by user input | OCI creds (T043-T050), GitHub Secrets (T055-T056) |
| Ready for runtime verification | T024, T030, T041 |
