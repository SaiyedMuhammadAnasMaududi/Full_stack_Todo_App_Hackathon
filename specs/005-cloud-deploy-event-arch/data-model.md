# Data Model: Phase V Event-Driven Architecture

## Existing Entities (Unchanged)

### Task
Per `backend/models.py`. Fields: id, title, description, completed, user_id, created_at, updated_at, priority, tags, due_at, reminder_at, recurrence_rule, is_recurring, parent_task_id, completed_at.

## New Entities

### TaskEvent
Published to Kafka via Dapr PubSub.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| event_type | string | Yes | task.created, task.updated, task.deleted, task.completed |
| task_id | string (UUID) | Yes | Task identifier |
| user_id | string | Yes | Task owner |
| task_data | object | Yes | Full task payload at time of event |
| timestamp | string (ISO-8601) | Yes | Event creation time |
| correlation_id | string (UUID) | Yes | Idempotency key |

### AuditEntry
Persisted by Audit Service.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string (UUID) | Yes | Audit record ID |
| event_type | string | Yes | From TaskEvent |
| task_id | string | Yes | From TaskEvent |
| user_id | string | Yes | From TaskEvent |
| timestamp | string | Yes | From TaskEvent |
| snapshot | object | Yes | task_data at event time |

### DaprJob (Reminder)
Managed by Dapr Jobs API.

| Field | Type | Description |
|-------|------|-------------|
| name | string | `reminder-{task_id}` |
| schedule | string | One-time trigger at reminder_at |
| data | object | {task_id, user_id, title} |

## Kafka Topics

| Topic | Producers | Consumers |
|-------|-----------|-----------|
| task-events | Backend | Recurring Service, Audit Service |
| reminders | Backend | Notification Service |
| task-updates | Backend | WebSocket Service |

## State Transitions

```
Task Created → event(task.created) → Kafka
Task Updated → event(task.updated) → Kafka
Task Completed → event(task.completed) → Kafka → Recurring Service creates next
Task Deleted → event(task.deleted) → Kafka
Reminder Time → Dapr Job fires → Notification Service
```
