<!-- Sync Impact Report:
Version change: N/A → 1.0.0
Modified principles: N/A (new constitution)
Added sections: Core Principles (6), Technology Stack & Data Storage, Authentication & Authorization Standards, Functional Requirements, API Standards, Frontend Standards, Constraints, Success Criteria
Removed sections: N/A
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Full-Stack Multi-User Todo Application Constitution

## Core Principles

### Spec-Driven First
No implementation begins without an approved specification. Code must strictly conform to defined specs.

### User Isolation & Security
Every user must only access their own data. Authentication and authorization are enforced at every API boundary.

### Single Source of Truth
Backend is the authoritative source for task data. Frontend never assumes state without API confirmation.

### Simplicity with Completeness
Only required features are implemented. All required features must be implemented fully and correctly.

### Reproducibility
The application must be deployable using documented steps. Environment-based configuration is mandatory.

### Backend Security Rules
Task ownership must be enforced on every operation. URL user_id must match the authenticated JWT user ID. Backend must never trust frontend-provided user data. All database queries must be filtered by authenticated user ID.

## Functional Requirements (Mandatory)
The application must implement all 5 Basic Level Todo features:

1. **Add Task** - Create a new todo item for the authenticated user.
2. **Delete Task** - Remove an existing task owned by the authenticated user.
3. **Update Task** - Modify task title, description, or other editable fields.
4. **View Task List** - Display all tasks belonging to the authenticated user.
5. **Mark as Complete** - Toggle the completion status of a task.

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

## Technology Stack (Fixed)
| Layer | Technology |
|-------------|------------------------------------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Auth | Better Auth + JWT |
| Spec System | Claude Code + Spec-Kit Plus |

No substitutions are allowed.

## Authentication & Authorization
### JWT Verification
FastAPI backend must verify token signature, validate expiration, and decode user identity (user_id, email).

### Shared Secret
JWT signing and verification must use the same secret: BETTER_AUTH_SECRET, stored as environment variables in both frontend and backend.

## Data Storage Rules
All task data must be stored in Neon PostgreSQL. No in-memory or local-only persistence is allowed. Each task record must be associated with a user ID.

## Frontend Standards
Responsive UI (mobile + desktop). Frontend must attach JWT token to every API request, never store sensitive secrets, and UI must reflect backend state accurately.

## Constraints
Must be a fully working web application. Must use REST APIs (no direct DB access from frontend). Stateless backend authentication only (JWT-based). No shared sessions between frontend and backend.

## Success Criteria
The project is considered successful if and only if:
- All 5 required Todo features work correctly.
- All API endpoints require valid JWT authentication.
- Users can only see and modify their own tasks.
- Backend enforces ownership and authorization.
- Application runs without security bypasses.
- Implementation strictly follows all specifications.

## Governance
Any feature, behavior, or code that violates this constitution is considered invalid and must be revised to comply. This document overrides all lower-level specifications and plans.

**Version**: 1.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-06