# Feature Specification: Advanced + Intermediate Todo Features

**Feature Branch**: `001-advanced-todo-features`
**Created**: 2026-02-06
**Status**: Draft
**Input**: User description: "/sp.specify

Project: Phase V – Part A – Advanced + Intermediate Todo Features

You are Claude Code operating under Spec-Driven Development.

This specification covers ONLY application-level features.

DO NOT include:
- Kafka
- Dapr
- Kubernetes
- Helm
- CI/CD
- Cloud

Those belong to later phases.

Scope is strictly:

Frontend + Backend + Database + Chat Agent behavior.

Manual coding is forbidden.

All implementation must be produced via Claude Code tasks.

────────────────────────────────────────
GOALS
────────────────────────────────────────

Extend the existing Phase III Todo Chatbot into a feature-complete application by implementing:

ADVANCED FEATURES:
1. Recurring Tasks
2. Due Dates
3. Reminder Metadata

INTERMEDIATE FEATURES:
4. Priorities
5. Tags
6. Search
7. Filter
8. Sort

These features must be accessible via:

- REST APIs
- Chatbot natural language
- Frontend UI

All three must remain consistent.

────────────────────────────────────────
EXISTING SYSTEM
────────────────────────────────────────

Already implemented:

- FastAPI backend
- SQLModel + PostgreSQL (Neon)
- Authentication (Better Auth)
- Todo CRUD
- Chatbot (OpenAI Agents SDK + Cohere)
- MCP tools for task operations
- Frontend Todo UI + embedded chatbot

This spec must EXTEND — not break — existing functionality.

Backward compatibility is mandatory.

────────────────────────────────────────
DATA MODEL EXTENSIONS
────────────────────────────────────────

Extend Task model with:

- priority: enum [low, medium, high]
- tags: array[string]
- due_at: datetime | null
- reminder_at: datetime | null
- recurrence_rule: string | null (RFC 5545 RRULE format)
- is_recurring: boolean
- parent_task_id: integer | null
- completed_at: datetime | null

Create supporting tables:

RecurringTaskTemplate:
- id
- rrule
- base_task_id

TaskAudit (pre-Kafka placeholder):
- id
- task_id
- action
- timestamp
- user_id

All migrations must be defined.

────────────────────────────────────────
BACKEND REQUIREMENTS
────────────────────────────────────────

Add REST endpoints:

/tasks/search
/tasks/filter
/tasks/sort
/tasks/{id}/complete
/tasks/{id}/update

Recurring logic:

- When recurring task is completed:
  create next task instance using recurrence_rule

Reminder logic:

- Store reminder_at
- Expose reminders via API
- No scheduling yet (infra phase later)

All logic must be deterministic and testable.

────────────────────────────────────────
CHATBOT REQUIREMENTS
────────────────────────────────────────

Chat agent must support:

Natural language:

- "set priority high"
- "add tag work"
- "tasks due tomorrow"
- "show high priority"
- "make this recurring weekly"
- "remind me at 8pm"
- "search meeting"

Agent must map intent → MCP tools.

Add new MCP tools:

- set_priority
- add_tags
- search_tasks
- filter_tasks
- sort_tasks
- set_due_date
- set_reminder
- set_recurrence

Responses must confirm actions.

Errors must be user friendly.

────────────────────────────────────────
FRONTEND REQUIREMENTS
────────────────────────────────────────

UI additions:

- Priority selector
- Tags input
- Due date picker
- Reminder time picker
- Recurring toggle + frequency
- Search bar
- Filter dropdown
- Sort dropdown

Frontend must:

- Reflect backend changes instantly
- Support chat + UI parity
- Show badges for priority/tags
- Visual indicator for recurring tasks

────────────────────────────────────────
NON FUNCTIONAL
────────────────────────────────────────

- Maintain stateless backend
- No breaking API changes
- Validation at API boundaries
- UTC datetime everywhere
- ISO timestamps

────────────────────────────────────────
DELIVERABLES
────────────────────────────────────────

Claude Code must output:

1. Updated database models
2. Migration files
3. Backend endpoints
4. MCP tool extensions
5. Agent intent mapping
6. Frontend UI components
7. API contracts
8. Test cases

Then generate:

/sp.plan

Then break into tasks.

No implementation before plan approval.

End Spec."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enhanced Task Management with Priorities (Priority: P1)

Users need to assign priorities to their tasks to better organize their workflow. Users should be able to set low, medium, or high priority levels to distinguish between urgent and less important tasks.

**Why this priority**: This is fundamental for productivity and task organization. Without priorities, all tasks appear equal in importance, making it difficult for users to decide what to tackle first.

**Independent Test**: Users can create tasks with priority levels (low, medium, high), see visual indicators for priority levels, and filter/sort tasks by priority. This delivers immediate value by allowing users to focus on the most important tasks first.

**Acceptance Scenarios**:
1. **Given** user has created tasks, **When** user sets priority to high on a task, **Then** the task displays with high priority visual indicators
2. **Given** user has tasks with different priorities, **When** user sorts by priority, **Then** tasks appear in priority order (high first)
3. **Given** user has high priority tasks, **When** user uses chatbot saying "show high priority tasks", **Then** chatbot responds with all high priority tasks

---

### User Story 2 - Due Date and Reminder Management (Priority: P1)

Users need to schedule tasks with due dates and set reminders so they don't miss important deadlines. This includes seeing upcoming tasks and getting timely notifications.

**Why this priority**: Due dates and reminders are essential for time-sensitive tasks. This feature directly impacts productivity by helping users manage deadlines effectively.

**Independent Test**: Users can assign due dates to tasks, see which tasks are due soon, and get reminders at specified times. This delivers value by preventing missed deadlines and improving time management.

**Acceptance Scenarios**:
1. **Given** user has a task, **When** user sets a due date for tomorrow, **Then** the task appears in "due tomorrow" view
2. **Given** user has set a reminder time, **When** the time arrives, **Then** user receives a notification (to be implemented in later phase)
3. **Given** user wants to see tasks due today, **When** user uses chatbot saying "show tasks due today", **Then** chatbot returns tasks due today

---

### User Story 3 - Recurring Task Creation (Priority: P1)

Users need to create tasks that repeat automatically, such as weekly team meetings or monthly bill payments, without having to manually recreate them each time.

**Why this priority**: Recurring tasks save users from repetitive work and prevent them from forgetting routine activities that happen on a schedule.

**Independent Test**: Users can create a task with a recurrence rule, and when that task is completed, the system automatically creates the next occurrence of the task according to the recurrence pattern. This delivers value by reducing manual task creation.

**Acceptance Scenarios**:
1. **Given** user has a weekly task, **When** user completes the task, **Then** system creates the next occurrence of the task for next week
2. **Given** user wants to make a task recurring, **When** user selects recurrence frequency, **Then** task becomes recurring with specified pattern
3. **Given** user has recurring tasks, **When** user uses chatbot saying "make this recurring weekly", **Then** the task becomes recurring weekly

---

### User Story 4 - Task Tagging and Categorization (Priority: P2)

Users need to categorize tasks with tags to group related items together, making it easier to organize and find specific tasks later.

**Why this priority**: Tags provide an alternative way to organize tasks beyond priority and due date, allowing users to categorize by project, context, or topic.

**Independent Test**: Users can add multiple tags to tasks and find tasks by their tags. This delivers value by enabling flexible organization and retrieval of related tasks.

**Acceptance Scenarios**:
1. **Given** user has created a task, **When** user adds tags to the task, **Then** the task can be found by searching for those tags
2. **Given** user has tasks with various tags, **When** user filters by a specific tag, **Then** only tasks with that tag are displayed
3. **Given** user wants to tag a task, **When** user uses chatbot saying "add tag work to this task", **Then** the task gets the "work" tag

---

### User Story 5 - Advanced Task Search and Filtering (Priority: P2)

Users need to quickly find specific tasks among potentially hundreds or thousands of entries using search and filter functionality.

**Why this priority**: As users accumulate more tasks, the ability to find specific ones becomes increasingly important for productivity.

**Independent Test**: Users can search for tasks by content and filter by various attributes like priority, tags, due date, and completion status. This delivers value by saving time and increasing efficiency.

**Acceptance Scenarios**:
1. **Given** user has many tasks, **When** user searches for "meeting", **Then** all tasks containing "meeting" are returned
2. **Given** user wants to see only high priority tasks, **When** user applies high priority filter, **Then** only high priority tasks are displayed
3. **Given** user has overdue tasks, **When** user filters for overdue tasks, **Then** only tasks past their due date are shown

---

### User Story 6 - Task Sorting and Organization (Priority: P2)

Users need to organize their tasks in different ways based on their preferences, such as sorting by due date, priority, or creation date.

**Why this priority**: Different users have different preferences for organizing their tasks. Flexible sorting options improve usability and user satisfaction.

**Independent Test**: Users can select different sorting options and see tasks rearranged according to their selection. This delivers value by making the task list more manageable and personalized.

**Acceptance Scenarios**:
1. **Given** user has multiple tasks, **When** user selects sort by due date, **Then** tasks are ordered chronologically by due date
2. **Given** user has tasks with various priorities, **When** user sorts by priority, **Then** tasks appear in priority order (high to low)
3. **Given** user has completed tasks, **When** user sorts by completion status, **Then** completed tasks are grouped separately or appear last

### Edge Cases

- What happens when a recurring task is deleted? The recurrence pattern should stop creating new instances.
- How does the system handle due dates in the past? Past due tasks should be clearly marked as overdue.
- What happens when a user has multiple tags and filters by one? The system should show tasks that contain the specific filter tag, regardless of other tags.
- How does the system handle priority conflicts when sorting? Priority should take precedence over other sorting criteria when specified.
- What happens when a task has both a due date and reminder? Both should be preserved and potentially trigger notifications (later phase implementation).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST extend the Task model with priority field (enum: low, medium, high)
- **FR-002**: System MUST extend the Task model with tags array field (array of strings)
- **FR-003**: System MUST extend the Task model with due_at datetime field (nullable)
- **FR-004**: System MUST extend the Task model with reminder_at datetime field (nullable)
- **FR-005**: System MUST extend the Task model with recurrence_rule string field (nullable, RFC 5545 format)
- **FR-006**: System MUST extend the Task model with is_recurring boolean field
- **FR-007**: System MUST extend the Task model with parent_task_id integer field (nullable)
- **FR-008**: System MUST extend the Task model with completed_at datetime field (nullable)
- **FR-009**: System MUST create RecurringTaskTemplate table with id, rrule, and base_task_id fields
- **FR-010**: System MUST create TaskAudit table with id, task_id, action, timestamp, and user_id fields
- **FR-011**: System MUST provide API endpoint for searching tasks by content
- **FR-012**: System MUST provide API endpoint for filtering tasks by multiple criteria
- **FR-013**: System MUST provide API endpoint for sorting tasks by various attributes
- **FR-014**: System MUST provide API endpoint for updating task with new fields
- **FR-015**: System MUST provide API endpoint for marking tasks as complete with completion timestamp
- **FR-016**: System MUST automatically create next task instance when a recurring task is completed
- **FR-017**: System MUST store reminder times for future notification handling
- **FR-018**: System MUST allow users to add multiple tags to a single task
- **FR-019**: System MUST preserve all existing functionality and maintain backward compatibility
- **FR-020**: System MUST ensure all new API endpoints follow the same authentication requirements as existing ones
- **FR-021**: Chatbot MUST support natural language commands for setting priorities
- **FR-022**: Chatbot MUST support natural language commands for adding tags
- **FR-023**: Chatbot MUST support natural language commands for setting due dates
- **FR-024**: Chatbot MUST support natural language commands for setting reminders
- **FR-025**: Chatbot MUST support natural language commands for making tasks recurring
- **FR-026**: Chatbot MUST support natural language commands for searching tasks
- **FR-027**: Chatbot MUST support natural language commands for filtering tasks
- **FR-028**: Chatbot MUST support natural language commands for sorting tasks
- **FR-029**: Chatbot MUST use new MCP tools for all advanced task operations
- **FR-030**: Frontend MUST provide UI elements for setting priorities
- **FR-031**: Frontend MUST provide UI elements for adding tags
- **FR-032**: Frontend MUST provide UI elements for setting due dates
- **FR-033**: Frontend MUST provide UI elements for setting reminders
- **FR-034**: Frontend MUST provide UI elements for making tasks recurring
- **FR-035**: Frontend MUST provide search functionality
- **FR-036**: Frontend MUST provide filter functionality
- **FR-037**: Frontend MUST provide sort functionality
- **FR-038**: Frontend MUST display visual indicators for priority levels
- **FR-039**: Frontend MUST display visual indicators for tags
- **FR-040**: Frontend MUST display visual indicators for recurring tasks
- **FR-041**: System MUST implement proper data validation at API boundaries
- **FR-042**: System MUST use UTC datetime consistently across all new datetime fields
- **FR-043**: System MUST use ISO timestamp format for all datetime representations
- **FR-044**: System MUST maintain stateless backend architecture in all new endpoints

### Key Entities

- **Extended Task**: Represents a task with additional attributes including priority, tags, due date, reminder, recurrence rule, and completion timestamp. Each task is associated with a single user and maintains its own status and metadata.

- **RecurringTaskTemplate**: Stores the recurrence pattern (RRULE) and links to the base task that defines the recurring series. This entity enables the automatic creation of future task instances based on the recurrence rule.

- **TaskAudit**: Tracks all changes to tasks for accountability and debugging purposes (placeholder before Kafka implementation). Contains information about what action occurred, when, and which user performed it.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can set priority levels (low, medium, high) on tasks with 100% success rate
- **SC-002**: Users can add tags to tasks and retrieve tagged tasks with 95% accuracy
- **SC-003**: Users can set due dates and see tasks organized by due date with 100% correctness
- **SC-004**: Users can create recurring tasks that automatically generate subsequent instances when completed
- **SC-005**: Users can search for tasks by content and find relevant results with 95% relevance
- **SC-006**: Users can filter tasks by multiple criteria (priority, tags, due date, status) with 100% accuracy
- **SC-007**: Users can sort tasks by various attributes (priority, due date, creation date) with correct ordering
- **SC-008**: Chatbot correctly interprets and processes natural language commands for all new features with 90% accuracy
- **SC-009**: All new API endpoints respond with consistent performance matching existing endpoints (under 500ms response time)
- **SC-010**: All new frontend UI components render correctly and allow user interaction without errors
- **SC-011**: Existing functionality remains unchanged and accessible after implementing new features
- **SC-012**: System handles all new datetime fields consistently using UTC and ISO format without conversion errors
