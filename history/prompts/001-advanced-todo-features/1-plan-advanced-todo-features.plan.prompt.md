---
id: 1
title: plan-advanced-todo-features
stage: plan
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-advanced-todo-features
branch: main
user: Claude Sonnet 4.5
command: /sp.plan
labels:
  - planning
  - architecture
  - todo-features
  - advanced-features
  - backend
  - frontend
  - mcp-tools
  - ai-integration
links:
  spec: specs/001-advanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-advanced-todo-features/plan.md
tests_yaml: []
---

# Plan Advanced Todo Features

## User Input

```
/sp.plan

Project: Phase V – Part A – Advanced + Intermediate Todo Features

Execution Mode: Claude Code (Fully Agentic)
Manual Coding: Forbidden

────────────────────────────────────────
PLAN OVERVIEW
────────────────────────────────────────

Implement Advanced and Intermediate Todo features across:

- Database
- Backend APIs
- Chat Agent MCP tools
- Frontend UI

Infrastructure is excluded.

Implementation must proceed in strict dependency order.

────────────────────────────────────────
PHASE 1 — DATABASE EVOLUTION
────────────────────────────────────────

1. Extend Task model:
   - priority
   - tags
   - due_at
   - reminder_at
   - recurrence_rule
   - is_recurring
   - parent_task_id
   - completed_at

2. Create new tables:
   - RecurringTaskTemplate
   - TaskAudit

3. Generate migration files.

4. Apply migrations.

5. Validate schema integrity.

Deliverables:
- Updated SQLModel classes
- Migration scripts
- Verified database state

────────────────────────────────────────
PHASE 2 — BACKEND DOMAIN LOGIC
────────────────────────────────────────

1. Implement recurring task engine:
   - Detect completion
   - Generate next instance using RRULE
   - Preserve parent-child relationship

2. Implement reminder metadata storage.

3. Implement priority and tagging logic.

4. Add TaskAudit event recording on:
   - create
   - update
   - complete
   - delete

Deliverables:
- Recurrence service
- Reminder handling
- Audit hooks

────────────────────────────────────────
PHASE 3 — REST API EXPANSION
────────────────────────────────────────

Create endpoints:

- POST /tasks/search
- POST /tasks/filter
- POST /tasks/sort
- PATCH /tasks/{id}/complete
- PATCH /tasks/{id}/update

Add request validation.

Ensure backward compatibility.

Deliverables:
- Controllers
- Schemas
- OpenAPI updates

────────────────────────────────────────
PHASE 4 — MCP TOOL EXTENSIONS
────────────────────────────────────────

Create MCP tools:

- set_priority
- add_tags
- search_tasks
- filter_tasks
- sort_tasks
- set_due_date
- set_reminder
- set_recurrence

Each tool must:

- Validate inputs
- Call backend API
- Return structured response

Deliverables:
- MCP definitions
- Tool implementations

────────────────────────────────────────
PHASE 5 — CHAT AGENT INTENT MAPPING
────────────────────────────────────────

Extend chatbot:

1. Add intent classification for:
   - priority
   - tags
   - due dates
   - reminders
   - recurrence
   - search/filter/sort

2. Map intents to MCP tools.

3. Add confirmation responses.

4. Add graceful error handling.

Deliverables:
- Updated agent routing logic
- Prompt updates
- Tool bindings

────────────────────────────────────────
PHASE 6 — FRONTEND FEATURE INTEGRATION
────────────────────────────────────────

Add UI components:

- Priority selector
- Tags input
- Due date picker
- Reminder picker
- Recurrence controls
- Search bar
- Filter dropdown
- Sort dropdown

Enhance task cards:

- Priority badges
- Tag chips
- Recurring indicators

Ensure:

- Instant UI refresh
- Chat/UI parity

Deliverables:
- Updated React components
- API hooks
- Styling updates

────────────────────────────────────────
PHASE 7 — END TO END VALIDATION
────────────────────────────────────────

Test flows:

- Create recurring task
- Complete task → regenerate
- Set reminder
- Priority change
- Tagging
- Search/filter/sort
- Chat commands vs UI actions

Deliverables:
- Integration tests
- Manual QA checklist

────────────────────────────────────────
PHASE 8 — FINALIZATION
────────────────────────────────────────

1. Update documentation.
2. Update API contracts.
3. Summarize changes.

Generate completion report.

────────────────────────────────────────
OUTPUT REQUIREMENTS
────────────────────────────────────────

Claude Code must produce:

- Code changes
- Migrations
- Tests
- Updated UI
- MCP tools
- Agent mapping
- Docs

Then halt.

End Plan.
```

## Response

Created a comprehensive implementation plan for the Advanced + Intermediate Todo Features. The plan is structured in 8 sequential phases following the dependency order required by the architecture.

Key highlights of the plan:

Phase 1 - Database Evolution: Extends the Task model with all new fields and creates supporting tables (RecurringTaskTemplate and TaskAudit).

Phase 2 - Backend Domain Logic: Implements the recurring task engine, reminder storage, priority/tagging logic, and audit trail functionality.

Phase 3 - REST API Expansion: Creates all required new endpoints for search, filter, sort, and enhanced update/complete operations.

Phase 4 - MCP Tool Extensions: Develops all 8 required MCP tools with proper validation and error handling.

Phase 5 - Chat Agent Intent Mapping: Extends the AI agent with intent recognition and mapping for all new features.

Phase 6 - Frontend Feature Integration: Creates all necessary UI components and enhances existing ones with new functionality.

Phase 7 - End to End Validation: Ensures comprehensive testing across all new functionality.

Phase 8 - Finalization: Updates documentation and creates release notes.

The plan leverages the existing codebase architecture while maintaining backward compatibility and following the established patterns in the application. Each phase has specific deliverables and success criteria to ensure quality implementation.

## Outcome

Successfully created a detailed implementation plan that follows the architecture of the existing application and provides a clear roadmap for implementing all advanced and intermediate todo features in a structured, dependency-aware manner.

## Evaluation

The plan addresses all requirements from the user input:
- ✅ Covers database evolution with all specified fields
- ✅ Implements backend domain logic for recurring tasks and audit trails
- ✅ Expands REST API with all required endpoints
- ✅ Extends MCP tools with all 8 required tools
- ✅ Maps chat agent intents for all new features
- ✅ Integrates frontend UI components for all features
- ✅ Plans for end-to-end validation and testing
- ✅ Includes finalization steps with documentation updates
- ✅ Maintains strict dependency order across phases
- ✅ Respects existing architecture patterns
- ✅ Preserves backward compatibility
- ✅ Excludes infrastructure concerns as specified