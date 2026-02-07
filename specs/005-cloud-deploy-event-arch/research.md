# Research: Phase V Cloud Deployment & Event-Driven Architecture

**Date**: 2026-02-07

## R-1: Kafka Operator Choice

**Decision**: Strimzi Kafka Operator
**Rationale**: Kubernetes-native CRDs, free/open-source, supports single-node for dev, multi-broker for prod. Mature ecosystem.
**Alternatives**: Redpanda Cloud (managed but costly), Confluent Operator (enterprise license), bare Kafka (no K8s integration).

## R-2: Dapr Jobs API for Reminders

**Decision**: Dapr Jobs API (stable since Dapr 1.13+)
**Rationale**: Schedule one-time or recurring jobs via HTTP/gRPC. No cron polling needed. Constitution mandates this over cron.
**Pattern**: Backend publishes reminder event → Notification Service creates Dapr Job with trigger time → Job fires callback to Notification Service → Service sends notification.

## R-3: Dapr PubSub Configuration

**Decision**: Dapr PubSub component with Kafka backend
**Pattern**: Application publishes via `POST /v1.0/publish/pubsub-kafka/task-events`. Consumers subscribe via `/dapr/subscribe` endpoint returning topic subscriptions.
**Topics**: task-events (CRUD), reminders (scheduled), task-updates (real-time sync).

## R-4: Dapr State Store

**Decision**: state.postgresql pointing to Neon PostgreSQL
**Rationale**: Reuses existing database. Dapr handles connection pooling and retries.
**Alternative rejected**: Redis (adds infra), etcd (operational complexity).

## R-5: Docker Image Strategy

**Decision**: Multi-stage builds
- Backend: `python:3.10-slim` base, pip install, copy app, uvicorn entrypoint
- Frontend: `node:18-alpine` build stage, `nginx:alpine` serve stage
**Image targets**: < 200MB backend, < 100MB frontend

## R-6: Helm Chart Structure

**Decision**: Single umbrella chart
**Structure**: One Chart.yaml, templates per service, values.yaml for local, values-oke.yaml for production.
**Dapr annotations**: `dapr.io/enabled: "true"`, `dapr.io/app-id`, `dapr.io/app-port`.

## R-7: Oracle OKE Setup

**Decision**: OCI CLI provisioning
**Steps**: Create VCN → Create subnet → Create OKE cluster → Create node pool → Download kubeconfig.
**Registry**: Oracle Container Registry (OCR) for Docker images.

## R-8: CI/CD Pipeline

**Decision**: GitHub Actions
**Stages**: lint (ruff/eslint) → test → docker build → push to registry → helm upgrade --install
**Secrets**: ORACLE_KUBECONFIG, OCR_TOKEN, DATABASE_URL, COHERE_API_KEY stored in GitHub Secrets.

## R-9: Event Schema

**Decision**: JSON schema with mandatory fields
```json
{
  "event_type": "task.created|task.updated|task.deleted|task.completed",
  "task_id": "uuid",
  "user_id": "string",
  "task_data": {},
  "timestamp": "ISO-8601",
  "correlation_id": "uuid"
}
```
**Idempotency**: correlation_id tracked in state store, duplicate events skipped.

## R-10: Resiliency

**Decision**: Dapr resiliency policies
- Retry: 3 attempts, exponential backoff (1s, 2s, 4s)
- Circuit breaker: trip after 5 consecutive failures, 30s timeout
- Dead letter: failed events routed to `dead-letter-task-events` topic
