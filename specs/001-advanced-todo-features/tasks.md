# Implementation Tasks: Advanced + Intermediate Todo Features

**Feature**: 001-advanced-todo-features
**Created**: 2026-02-06
**Status**: Ready for Execution

## Phase 1: Setup

- [ ] T001 Set up development environment for advanced features implementation
- [ ] T002 Review existing codebase structure and identify extension points

## Phase 2: Foundational Tasks

- [ ] T003 [P] Install dateutil library for recurrence rule parsing in backend
- [ ] T004 [P] Add necessary validation libraries for enum and date validation
- [ ] T005 [P] Create shared utility functions for date/time handling in UTC

## Phase 3: [US1] Enhanced Task Management with Priorities

### Independent Test: Users can create tasks with priority levels (low, medium, high), see visual indicators for priority levels, and filter/sort tasks by priority. This delivers immediate value by allowing users to focus on the most important tasks first.

### Implementation Tasks:

- [ ] T006 [P] [US1] Extend Task model with priority enum field in backend/models.py
- [ ] T007 [P] [US1] Update Task Pydantic models to include priority field validation
- [ ] T008 [P] [US1] Create PrioritySelector component in frontend/components/PrioritySelector/PrioritySelector.tsx
- [ ] T009 [US1] Update task form UI to include priority selection in frontend/components/TaskForm/TaskForm.tsx
- [ ] T010 [US1] Update task card to display priority visual indicators in frontend/components/TaskItem/TaskItem.tsx
- [ ] T011 [US1] Add priority sorting functionality to existing endpoints
- [ ] T012 [US1] Update MCP set_priority tool in backend/src/mcp/server.py
- [ ] T013 [US1] Extend chat agent to recognize priority-related phrases in backend/src/ai/agent.py
- [ ] T014 [US1] Map priority intents to MCP tools in backend/src/ai/agent.py

## Phase 4: [US2] Due Date and Reminder Management

### Independent Test: Users can assign due dates to tasks, see which tasks are due soon, and get reminders at specified times. This delivers value by preventing missed deadlines and improving time management.

### Implementation Tasks:

- [ ] T015 [P] [US2] Extend Task model with due_at datetime field in backend/models.py
- [ ] T016 [P] [US2] Extend Task model with reminder_at datetime field in backend/models.py
- [ ] T017 [P] [US2] Update Task Pydantic models to include due_at and reminder_at validation
- [ ] T018 [P] [US2] Create DatePicker component in frontend/components/DatePicker/DatePicker.tsx
- [ ] T019 [P] [US2] Create ReminderPicker component in frontend/components/ReminderPicker/ReminderPicker.tsx
- [ ] T020 [US2] Update task form UI to include due date and reminder pickers in frontend/components/TaskForm/TaskForm.tsx
- [ ] T021 [US2] Update task card to display due date and reminder indicators in frontend/components/TaskItem/TaskItem.tsx
- [ ] T022 [US2] Add due date filtering and sorting functionality to existing endpoints
- [ ] T023 [US2] Update MCP set_due_date and set_reminder tools in backend/src/mcp/server.py
- [ ] T024 [US2] Extend chat agent to recognize due date and reminder phrases in backend/src/ai/agent.py
- [ ] T025 [US2] Map due date and reminder intents to MCP tools in backend/src/ai/agent.py

## Phase 5: [US3] Recurring Task Creation

### Independent Test: Users can create a task with a recurrence rule, and when that task is completed, the system automatically creates the next occurrence of the task according to the recurrence pattern. This delivers value by reducing manual task creation.

### Implementation Tasks:

- [ ] T026 [P] [US3] Extend Task model with recurrence_rule string field in backend/models.py
- [ ] T027 [P] [US3] Extend Task model with is_recurring boolean field in backend/models.py
- [ ] T028 [P] [US3] Extend Task model with parent_task_id integer field in backend/models.py
- [ ] T029 [P] [US3] Create RecurringTaskTemplate model in backend/models.py
- [ ] T030 [P] [US3] Update Task Pydantic models to include recurrence fields validation
- [ ] T031 [P] [US3] Create recurrence service in backend/services/recurrence.py
- [ ] T032 [P] [US3] Create RecurrenceControls component in frontend/components/RecurrenceControls/RecurrenceControls.tsx
- [ ] T033 [US3] Update task form UI to include recurrence controls in frontend/components/TaskForm/TaskForm.tsx
- [ ] T034 [US3] Update task card to display recurring indicators in frontend/components/TaskItem/TaskItem.tsx
- [ ] T035 [US3] Implement recurring task generation logic when completing recurring tasks
- [ ] T036 [US3] Update MCP set_recurrence tool in backend/src/mcp/server.py
- [ ] T037 [US3] Extend chat agent to recognize recurring phrases in backend/src/ai/agent.py
- [ ] T038 [US3] Map recurring intents to MCP tools in backend/src/ai/agent.py

## Phase 6: [US4] Task Tagging and Categorization

### Independent Test: Users can add multiple tags to tasks and find tasks by their tags. This delivers value by enabling flexible organization and retrieval of related tasks.

### Implementation Tasks:

- [ ] T039 [P] [US4] Extend Task model with tags array field in backend/models.py
- [ ] T040 [P] [US4] Update Task Pydantic models to include tags validation
- [ ] T041 [P] [US4] Create TagsInput component in frontend/components/TagsInput/TagsInput.tsx
- [ ] T042 [US4] Update task form UI to include tags input in frontend/components/TaskForm/TaskForm.tsx
- [ ] T043 [US4] Update task card to display tag chips in frontend/components/TaskItem/TaskItem.tsx
- [ ] T044 [US4] Implement tag-based search and filtering functionality
- [ ] T045 [US4] Update MCP add_tags tool in backend/src/mcp/server.py
- [ ] T046 [US4] Extend chat agent to recognize tag-related phrases in backend/src/ai/agent.py
- [ ] T047 [US4] Map tag intents to MCP tools in backend/src/ai/agent.py

## Phase 7: [US5] Advanced Task Search and Filtering

### Independent Test: Users can search for tasks by content and filter by various attributes like priority, tags, due date, and completion status. This delivers value by saving time and increasing efficiency.

### Implementation Tasks:

- [ ] T048 [P] [US5] Create search endpoint POST /api/{user_id}/tasks/search in backend/routes/tasks.py
- [ ] T049 [P] [US5] Create filter endpoint POST /api/{user_id}/tasks/filter in backend/routes/tasks.py
- [ ] T050 [P] [US5] Create SearchBar component in frontend/components/SearchBar/SearchBar.tsx
- [ ] T051 [P] [US5] Create FilterDropdown component in frontend/components/FilterDropdown/FilterDropdown.tsx
- [ ] T052 [US5] Update API client with search and filter methods in frontend/lib/api.ts
- [ ] T053 [US5] Update tasks page to include search and filter UI in frontend/app/tasks/page.tsx
- [ ] T054 [US5] Update MCP search_tasks and filter_tasks tools in backend/src/mcp/server.py
- [ ] T055 [US5] Extend chat agent to recognize search and filter phrases in backend/src/ai/agent.py
- [ ] T056 [US5] Map search and filter intents to MCP tools in backend/src/ai/agent.py

## Phase 8: [US6] Task Sorting and Organization

### Independent Test: Users can select different sorting options and see tasks rearranged according to their selection. This delivers value by making the task list more manageable and personalized.

### Implementation Tasks:

- [ ] T057 [P] [US6] Create sort endpoint POST /api/{user_id}/tasks/sort in backend/routes/tasks.py
- [ ] T058 [P] [US6] Create SortDropdown component in frontend/components/SortDropdown/SortDropdown.tsx
- [ ] T059 [US6] Update API client with sort method in frontend/lib/api.ts
- [ ] T060 [US6] Update tasks page to include sort UI in frontend/app/tasks/page.tsx
- [ ] T061 [US6] Update MCP sort_tasks tool in backend/src/mcp/server.py
- [ ] T062 [US6] Extend chat agent to recognize sort phrases in backend/src/ai/agent.py
- [ ] T063 [US6] Map sort intents to MCP tools in backend/src/ai/agent.py

## Phase 9: Backend Enhancement Tasks

### Implementation Tasks:

- [ ] T064 [P] Create TaskAudit model in backend/models.py
- [ ] T065 [P] Create audit service in backend/services/audit.py
- [ ] T066 [P] Enhance complete task endpoint to set completed_at timestamp in backend/routes/tasks.py
- [ ] T067 [P] Enhance update task endpoint with PATCH /api/{user_id}/tasks/{id}/update in backend/routes/tasks.py
- [ ] T068 [P] Implement audit logging for all CRUD operations
- [ ] T069 [P] Update existing task CRUD operations to handle new fields properly

## Phase 10: MCP and AI Integration

### Implementation Tasks:

- [ ] T070 [P] Register all new MCP tools with the server in backend/src/mcp/server.py
- [ ] T071 [P] Update chat agent system prompt to include new capabilities in backend/src/ai/agent.py
- [ ] T072 [P] Enhance chat agent response formatting for new features in backend/src/ai/agent.py
- [ ] T073 [P] Add error handling for new MCP tools in backend/src/ai/agent.py

## Phase 11: Frontend Integration

### Implementation Tasks:

- [ ] T074 [P] Integrate all new components into the main task workflow in frontend/components/TaskForm/TaskForm.tsx
- [ ] T075 [P] Update API client to handle new field types in frontend/lib/api.ts
- [ ] T076 [P] Update tasks page layout to accommodate new features in frontend/app/tasks/page.tsx
- [ ] T077 [P] Ensure proper error handling for new features in frontend

## Phase 12: Polish & Cross-Cutting Concerns

### Implementation Tasks:

- [ ] T078 [P] Update database initialization to include new models in backend/main.py
- [ ] T079 [P] Add proper validation for recurrence rules to ensure RFC 5545 compliance
- [ ] T080 [P] Ensure all datetime fields use UTC consistently
- [ ] T081 [P] Add comprehensive error handling for all new features
- [ ] T082 [P] Add logging for new functionality
- [ ] T083 [P] Create/update documentation for new features in docs/
- [ ] T084 [P] Update OpenAPI documentation with new endpoints
- [ ] T085 [P] Conduct integration testing across all new features
- [ ] T086 [P] Verify backward compatibility with existing functionality

## Dependencies

- **US2 (Due Date/Reminder)** depends on: Foundational Tasks
- **US3 (Recurring Tasks)** depends on: US1 (Priority), US2 (Due Date/Reminder)
- **US4 (Tagging)** depends on: Foundational Tasks
- **US5 (Search/Filter)** depends on: US1 (Priority), US2 (Due Date/Reminder), US4 (Tagging)
- **US6 (Sorting)** depends on: US1 (Priority), US2 (Due Date/Reminder), US4 (Tagging)

## Parallel Execution Examples

- Tasks T006-T010 can run in parallel for US1 (Priority)
- Tasks T015-T021 can run in parallel for US2 (Due Date/Reminder)
- Tasks T026-T032 can run in parallel for US3 (Recurring)
- Tasks T039-T043 can run in parallel for US4 (Tagging)

## Implementation Strategy

- **MVP Scope**: Complete US1 (Priority) and US2 (Due Date/Reminder) as the minimum viable product
- **Incremental Delivery**: Each user story builds upon the previous ones, allowing for phased delivery
- **Consistency**: All features implemented across backend API, MCP tools, chat agent, and frontend UI simultaneously