---
id: 3
title: plan-frontend-auth-todo-app
stage: plan
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: frontend-auth-todo
branch: 001-frontend-auth-todo
user: claude
command: /sp.plan
labels:
  - planning
  - authentication
  - todo-app
  - frontend
  - nextjs
  - jwt
links:
  spec: ../specs/001-frontend-auth-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-frontend-auth-todo/plan.md
  - specs/001-frontend-auth-todo/research.md
  - specs/001-frontend-auth-todo/data-model.md
  - specs/001-frontend-auth-todo/quickstart.md
  - specs/001-frontend-auth-todo/contracts/todo-api.yaml
tests: []
---

# Plan Frontend Authentication and Todo Application

## User Prompt

```

## Create

### Architecture Sketch

- **Frontend Layer**: Next.js 16+ (App Router)
  - Pages:
    - `/login` → User signin
    - `/signup` → User signup
    - `/tasks` → Main Todo dashboard (list, add, update, delete, complete)
  - Components:
    - `TaskList` → Displays tasks for authenticated user
    - `TaskItem` → Single task with actions (edit, delete, toggle complete)
    - `TaskForm` → Add/Edit task form
    - `Header` → Navigation + Signout
    - `AuthGuard` → Protects routes from unauthenticated access

- **API Client**
  - Centralized file to handle REST API requests
  - Automatically attaches JWT token to `Authorization: Bearer <token>` header

- **State Management**
  - Use React state or Context for task list
  - Keep UI in sync with backend responses
  - No backend logic in frontend

- **Responsive Design**
  - Mobile-first layout
  - Flexbox / CSS Grid
  - Optional Tailwind CSS or plain CSS modules

---

### Section Structure

1. **Authentication**
   - Pages: `/login`, `/signup`
   - Features:
     - Signin / Signup forms
     - JWT token retrieval and storage (localStorage/sessionStorage)
     - Redirect to `/tasks` on success

2. **Todo Dashboard**
   - Protected by `AuthGuard`
   - Features:
     - View task list (GET `/api/{user_id}/tasks`)
     - Add task (POST `/api/{user_id}/tasks`)
     - Update task (PUT `/api/{user_id}/tasks/{id}`)
     - Delete task (DELETE `/api/{user_id}/tasks/{id}`)
     - Toggle completion (PATCH `/api/{user_id}/tasks/{id}/complete`)

3. **Error Handling**
   - Display messages for failed API requests (401, 404, 500)
   - Graceful fallback for empty task list

---

### Research Approach

- Research **Better Auth Next.js integration** concurrently while building pages
- Verify **JWT token handling and route protection**
- Check **Next.js 16+ App Router best practices** for dynamic pages
- Explore **responsive UI patterns** for task management

---

### Quality Validation

- Ensure **all 5 Todo features** function correctly for a single user
- JWT token **must be included** in all API requests
- UI must **accurately reflect backend state**
- Test **mobile and desktop layouts**
- Confirm **unauthenticated users cannot access `/tasks`**

---

## Decisions Needing Documentation

| Decision | Options | Trade-offs |
|----------|--------|------------|
| **Authentication Storage** | localStorage, sessionStorage, or React Context | localStorage persists across tabs, sessionStorage expires on close; Context is volatile on refresh |
| **Task State Management** | React state, Context, or Redux | Simple React state enough for hackathon; Redux adds complexity |
| **Styling Framework** | Tailwind CSS, CSS Modules, or plain CSS | Tailwind = faster and responsive; CSS Modules = lightweight; plain CSS = manual responsiveness |
| **JWT Retrieval & Usage** | Store in client, attach manually, or use wrapper API | Wrapper API simplifies requests; manual approach gives full control |

---

## Testing Strategy

- **Authentication**
  - Attempt login/signup with valid/invalid credentials
  - Ensure JWT token is issued and stored correctly
  - Verify protected routes redirect unauthenticated users

- **Todo Features**
  - Add a task → Verify task appears in UI and backend
  - Update a task → Verify task changes persist
  - Delete a task → Verify task removed
  - Mark complete → Verify status toggled and synced
  - Ensure tasks **only belong to the logged-in user**

- **Responsive Layout**
  - Test at mobile widths (320px, 375px, 480px)
  - Test at tablet widths (768px, 1024px)
  - Test at desktop widths (1280px+)

- **API Error Handling**
  - Test unauthorized request → Should show 401 error
  - Test invalid endpoint → Should show proper error message

---

## Technical Details

- **Use research-concurrent approach**
  - Research Better Auth and Next.js while building components
- **Environment Variables**
  - `BETTER_AUTH_SECRET` → Required for JWT verification
  - Should be obtained from the backend / project environment setup
  - Frontend reads it via `.env.local` or Next.js environment variables
- **Phased Development**
  1. **Foundation**
     - Set up Next.js 16+ project
     - Configure routing & layout
     - Install Better Auth library
  2. **Authentication**
     - Build signup/signin pages
     - Retrieve and store JWT token
     - Protect `/tasks` route with `AuthGuard`
  3. **Todo Features**
     - Build `TaskList` and `TaskItem` components
     - Implement Add/Update/Delete/Complete actions
     - Connect all actions to REST API with JWT token
  4. **UI/UX**
     - Make frontend responsive
     - Error handling, empty states, feedback messages
  5. **Validation**
     - Test all acceptance criteria
     - Verify JWT token is included in API calls
     - Ensure tasks belong to logged-in user only

- **Documentation**
  - Comment code where JWT handling or API calls occur
  - Maintain `.env.local.example` to show required environment variables

---
```

## Response Summary

Successfully completed the planning phase for the frontend authentication and todo application. Created comprehensive documentation including:

1. Implementation plan (plan.md) - detailing architecture, tech stack, and structure
2. Research summary (research.md) - covering technology decisions and approaches
3. Data model (data-model.md) - defining frontend data structures
4. Quickstart guide (quickstart.md) - providing setup and development instructions
5. API contracts (contracts/todo-api.yaml) - specifying API endpoints and schemas

The plan ensures compliance with the project constitution and covers all required functionality: user authentication with Better Auth, JWT-based authorization, and all 5 required todo features (Add, Delete, Update, View, Mark Complete). The design includes responsive UI, proper error handling, and security measures as specified in the requirements.

## Outcome

Planning phase complete with all required artifacts generated. The implementation is ready to proceed to the task breakdown phase with /sp.tasks. The frontend application will be built using Next.js 16+ with App Router, Better Auth for authentication, and JWT tokens for API authorization.