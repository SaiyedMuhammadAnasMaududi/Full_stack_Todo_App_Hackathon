# Implementation Plan: Phase V Cloud Deployment & Event-Driven Architecture

**Branch**: `005-cloud-deploy-event-arch` | **Date**: 2026-02-07 | **Spec**: specs/005-cloud-deploy-event-arch/spec.md
**Input**: Feature specification from `/specs/005-cloud-deploy-event-arch/spec.md`

## Summary

Deploy the AI Todo Chatbot to Kubernetes (Minikube local, Oracle OKE production) with Dapr sidecar injection for infrastructure abstraction. Implement event-driven architecture using Kafka via Dapr PubSub for task events, reminders, recurring tasks, and audit. Automate via GitHub Actions CI/CD pipeline.

## Technical Context

**Language/Version**: Python 3.10+ (backend), Node.js 18+ / Next.js 14 (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Dapr SDK, Strimzi Kafka, Helm 3, Docker
**Storage**: Neon PostgreSQL (via Dapr state.postgresql), Kafka (via Dapr pubsub.kafka)
**Testing**: curl/httpie for API, kubectl for infra, dapr CLI for components
**Target Platform**: Kubernetes (Minikube local, Oracle OKE production)
**Project Type**: Web application (microservices)
**Performance Goals**: p95 < 500ms, 100 concurrent users, event publish < 100ms
**Constraints**: No direct Kafka/DB access from app code (Dapr only), no manual kubectl
**Scale/Scope**: 6 pods (frontend, backend, notification, recurring, audit, websocket) + Kafka + Dapr

## Constitution Check

| Gate | Status | Notes |
|------|--------|-------|
| Spec approved | PASS | spec.md created |
| No direct DB access | PASS | Dapr state.postgresql |
| No direct Kafka access | PASS | Dapr pubsub.kafka |
| Dapr sidecar mandatory | PASS | All pods annotated |
| No manual coding | PASS | Claude Code agents |
| No hardcoded secrets | PASS | Dapr secretstores.kubernetes |
| Event-driven for reminders/recurring/audit | PASS | Kafka topics via Dapr |
| Helm charts for deployment | PASS | charts/ directory |
| CI/CD mandatory | PASS | GitHub Actions |

## Project Structure

### Documentation

```text
specs/005-cloud-deploy-event-arch/
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── event-schemas.yaml
│   └── dapr-components.yaml
└── tasks.md
```

### Source Code

```text
backend/
├── main.py                    # Existing FastAPI app
├── services/
│   ├── event_publisher.py     # Dapr PubSub event publishing
│   ├── notification.py        # Reminder consumer service
│   ├── recurring.py           # Recurring task consumer
│   └── audit.py               # Audit log consumer
├── Dockerfile                 # Production Docker image

frontend/
├── Dockerfile                 # Production Docker image

infra/
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-oke.yaml
│       └── templates/
│           ├── backend-deployment.yaml
│           ├── frontend-deployment.yaml
│           ├── notification-deployment.yaml
│           ├── recurring-deployment.yaml
│           ├── audit-deployment.yaml
│           ├── websocket-deployment.yaml
│           ├── services.yaml
│           ├── configmap.yaml
│           ├── secrets.yaml
│           ├── hpa.yaml
│           └── ingress.yaml
├── dapr/
│   ├── pubsub-kafka.yaml
│   ├── statestore-postgres.yaml
│   ├── secretstore-kubernetes.yaml
│   └── resiliency.yaml
├── kafka/
│   ├── strimzi-operator.yaml
│   └── kafka-cluster.yaml
└── minikube/
    └── setup.sh

.github/workflows/
└── deploy.yaml                # CI/CD pipeline
```

**Structure Decision**: Web application with microservices. Backend services split into event consumers. Infrastructure as code in `infra/` directory.

## Architecture Decisions

### AD-1: Strimzi for Kafka
- **Chosen**: Strimzi Kafka Operator
- **Rationale**: Free, Kubernetes-native, CRD-based management, battle-tested
- **Alternative rejected**: Redpanda Cloud (cost, external dependency)

### AD-2: Dapr Jobs API for Reminders
- **Chosen**: Dapr Jobs API
- **Rationale**: Exact timing, no DB polling, Dapr-native
- **Alternative rejected**: Cron polling (constitution forbids)

### AD-3: Kubernetes Secrets Store
- **Chosen**: secretstores.kubernetes
- **Rationale**: Simple, Oracle-compatible, no extra infra
- **Alternative rejected**: OCI Vault (adds complexity for MVP)

### AD-4: Single Helm Chart
- **Chosen**: One umbrella chart with subcharts per service
- **Rationale**: Atomic deployment, shared values, environment overrides
- **Alternative rejected**: Per-service charts (deployment coordination overhead)

## Delivery Phases

### Phase 1: Dockerization (P1)
1. Create backend Dockerfile (multi-stage, Python 3.10-slim)
2. Create frontend Dockerfile (multi-stage, Node 18-alpine)
3. Build and test images locally
4. Health check endpoints verified in containers

### Phase 2: Minikube + Dapr + Kafka (P1)
1. Minikube cluster init with sufficient resources
2. Install Dapr runtime (`dapr init -k`)
3. Deploy Strimzi operator + Kafka cluster CRD
4. Create Kafka topics (task-events, reminders, task-updates)
5. Apply Dapr components (pubsub, statestore, secretstore)
6. Deploy backend/frontend via Helm with Dapr annotations

### Phase 3: Event Services (P2)
1. Implement event publisher in backend (publish on CRUD operations)
2. Implement Notification Service (consume reminders, schedule Dapr Jobs)
3. Implement Recurring Task Service (consume task-events, create next instance)
4. Implement Audit Service (consume task-events, persist audit log)
5. Event schema validation and idempotency (correlation_id dedup)

### Phase 4: Oracle OKE (P2)
1. Provision OKE cluster via OCI CLI
2. Configure kubectl context
3. Install Dapr + Strimzi on OKE
4. Push Docker images to Oracle Container Registry
5. Deploy via Helm with values-oke.yaml overrides

### Phase 5: CI/CD (P3)
1. GitHub Actions workflow: lint → build → docker → push → helm deploy
2. Image tagging with git SHA
3. Rollback on deployment failure
4. Secrets via GitHub Secrets → K8s Secrets

### Phase 6: Observability (P3)
1. Prometheus metrics endpoint
2. Dapr dashboard
3. Pod liveness/readiness probes
4. Centralized logging

### Phase 7: Validation
- Full E2E: task CRUD → events → reminders → recurring → audit
- Secrets via Dapr verified
- HPA scaling verified
- Cloud deployment verified

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dapr Jobs API instability | Missed reminders | Fallback to scheduled consumer polling |
| Strimzi resource overhead on Minikube | OOM/slow | Reduce Kafka replicas to 1 for local |
| Oracle OKE provisioning delays | Blocked Phase 4 | Minikube as primary validation target |

## Complexity Tracking

No constitution violations detected. All gates pass.
