---
id: 1
title: amend-constitution-todo-app
stage: constitution
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude Sonnet 4.5
command: sp.constitution
labels: [constitution,spec-driven-development,todo-application]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
## Project
Full-Stack Multi-User Todo Application using Spec-Driven Development (Spec-Kit Plus)

## Purpose
Define the non-negotiable principles, standards, constraints, and success criteria
governing the design, development, and implementation of a secure, scalable,
full-stack Todo web application for hackathon submission.

This constitution acts as the highest authority for all specifications, plans,
and implementation decisions.

---

## Core Principles

1. **Spec-Driven First**
   - No implementation begins without an approved specification.
   - Code must strictly conform to defined specs.

2. **User Isolation & Security**
   - Every user must only access their own data.
   - Authentication and authorization are enforced at every API boundary.

3. **Single Source of Truth**
   - Backend is the authoritative source for task data.
   - Frontend never assumes state without API confirmation.

4. **Simplicity with Completeness**
   - Only required features are implemented.
   - All required features must be implemented fully and correctly.

5. **Reproducibility**
   - The application must be deployable using documented steps.
   - Environment-based configuration is mandatory.

---

## Functional Requirements (Mandatory)

The application **must implement all 5 Basic Level Todo features**:

1. **Add Task**
   - Create a new todo item for the authenticated user.

2. **Delete Task**
   - Remove an existing task owned by the authenticated user.

3. **Update Task**
   - Modify task title, description, or other editable fields.

4. **View Task List**
   - Display all tasks belonging to the authenticated user.

5. **Mark as Complete**
   - Toggle the completion status of a task.

All features must be accessible via REST API and usable through the frontend UI.

---

## API Standards

### RESTful Endpoints (Required)

| Method | Endpoint                                   | Description                     |
|------|--------------------------------------------|---------------------------------|
| GET  | /api/{user_id}/tasks                       | List all user tasks             |
| POST | /api/{user_id}/tasks                       | Create a new task               |
| GET  | /api/{user_id}/tasks/{id}                  | Retrieve task details           |
| PUT  | /api/{user_id}/tasks/{id}                  | Update an existing task         |
| DELETE | /api/{user_id}/tasks/{id}                | Delete a task                   |
| PATCH | /api/{user_id}/tasks/{id}/complete        | Toggle completion status        |

---

## Authentication & Authorization

### Authentication Provider
- **Better Auth** (Next.js frontend)

### Authorization Mechanism
- **JWT (JSON Web Tokens)**

### Mandatory JWT Rules
- Every API request **must** include:
Authorization: Bearer <JWT_TOKEN>

kotlin
Copy code
- Requests without a valid JWT must return:
401 Unauthorized

diff
Copy code

### JWT Verification
- FastAPI backend must:
- Verify token signature
- Validate expiration
- Decode user identity (user_id, email)

### Shared Secret
- JWT signing and verification must use the same secret:
BETTER_AUTH_SECRET

yaml
Copy code
- Stored as environment variables in both frontend and backend.

---

## Backend Security Rules (Non-Negotiable)

- Task ownership **must be enforced** on every operation.
- URL `user_id` **must match** the authenticated JWT user ID.
- Backend must never trust frontend-provided user data.
- All database queries must be filtered by authenticated user ID.

---

## Technology Stack (Fixed)

| Layer        | Technology                         |
|-------------|------------------------------------|
| Frontend    | Next.js 16+ (App Router)            |
| Backend     | Python FastAPI                     |
| ORM         | SQLModel                           |
| Database    | Neon Serverless PostgreSQL         |
| Auth        | Better Auth + JWT                  |
| Spec System | Claude Code + Spec-Kit Plus        |

No substitutions are allowed.

---

## Data Storage Rules

- All task data must be stored in Neon PostgreSQL.
- No in-memory or local-only persistence is allowed.
- Each task record must be associated with a user ID.

---

## Frontend Standards

- Responsive UI (mobile + desktop)
- Frontend must:
- Attach JWT token to every API request
- Never store sensitive secrets
- UI must reflect backend state accurately.

---

## Constraints

- Must be a fully working web application.
- Must use REST APIs (no direct DB access from frontend).
- Stateless backend authentication only (JWT-based).
- No shared sessions between frontend and backend.

---

## Success Criteria

The project is considered **successful** if and only if:

- All 5 required Todo features work correctly.
- All API endpoints require valid JWT authentication.
- Users can only see and modify their own tasks.
- Backend enforces ownership and authorization.
- Application runs without security bypasses.
- Implementation strictly follows all specifications.

---

## Enforcement

Any feature, behavior, or code that violates this constitution
is considered invalid and must be revised to comply.

This document overrides all lower-level specifications and plans.
```

## Response snapshot

The constitution for the Full-Stack Multi-User Todo Application has been successfully created at `.specify/memory/constitution.md`. The document includes all the required principles, functional requirements, API standards, technology stack, authentication standards, data storage rules, frontend standards, constraints, and success criteria as specified in the user's input. The constitution version is 1.0.0, with ratification and last amended dates set to 2026-01-01-06. The document serves as the highest authority for all specifications, plans, and implementation decisions for the project.

## Outcome

- ✅ Impact: New constitution document created with all specified requirements
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Continue with spec, plan, and task creation for the todo application
- 🧠 Reflection: The constitution provides clear guidelines and constraints for the todo application development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating the feature specification based on this constitution