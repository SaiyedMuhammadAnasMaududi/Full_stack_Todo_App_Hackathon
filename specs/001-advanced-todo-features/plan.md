# Implementation Plan: Advanced + Intermediate Todo Features

**Feature**: 001-advanced-todo-features
**Created**: 2026-02-06
**Status**: Approved
**Author**: Claude Code

## Overview

This plan outlines the implementation of advanced and intermediate todo features in strict dependency order. The implementation will extend the existing Phase III Todo Chatbot to add recurring tasks, due dates, reminders, priorities, tags, search, filter, and sort functionality.

## Architecture Context

Based on analysis of the existing codebase:
- **Backend**: Python FastAPI with SQLModel ORM
- **Database**: PostgreSQL via Neon (no formal migration system - uses SQLModel metadata creation)
- **Frontend**: Next.js 16+ with App Router
- **AI Layer**: Cohere API integration with MCP tools
- **Authentication**: Better Auth with JWT tokens

## Phase 1 — Database Evolution

### 1.1 Extend Task Model
- **Location**: `backend/models.py`
- **Changes**:
  - Add `priority` enum field (low, medium, high)
  - Add `tags` field (JSON array of strings)
  - Add `due_at` datetime field (nullable)
  - Add `reminder_at` datetime field (nullable)
  - Add `recurrence_rule` string field (nullable, RFC 5545 format)
  - Add `is_recurring` boolean field
  - Add `parent_task_id` integer field (nullable, foreign key to Task)
  - Add `completed_at` datetime field (nullable)

### 1.2 Create Supporting Tables
- **RecurringTaskTemplate**:
  - id (primary key)
  - rrule (string)
  - base_task_id (foreign key to Task)
  - **Location**: `backend/models.py`

- **TaskAudit** (pre-Kafka placeholder):
  - id (primary key)
  - task_id (foreign key to Task)
  - action (string)
  - timestamp (datetime)
  - user_id (foreign key to User)
  - **Location**: `backend/models.py`

### 1.3 Update SQLModel Relationships
- Update Task model to handle parent/child relationships for recurring tasks
- Ensure proper cascading behaviors for related records

### 1.4 Validation Requirements
- Add validation for due_at to ensure it's not in the past
- Add validation for recurrence_rule to ensure RFC 5545 compliance
- Add validation for priority enum values

**Deliverables**:
- Updated `backend/models.py` with extended Task model and new tables
- Updated Pydantic request/response models to include new fields

## Phase 2 — Backend Domain Logic

### 2.1 Implement Recurring Task Engine
- **Location**: `backend/services/recurrence.py`
- **Features**:
  - Detect when a recurring task is completed
  - Parse recurrence rule using dateutil.rrule
  - Generate next task instance based on recurrence pattern
  - Maintain parent-child relationship between task instances
  - Handle recurrence termination conditions

### 2.2 Implement Reminder Metadata Storage
- **Location**: Update `backend/routes/tasks.py`
- **Features**:
  - Store reminder times with tasks
  - Expose reminder information via API (without scheduling)
  - Validate reminder times are in the future

### 2.3 Implement Priority and Tagging Logic
- **Location**: Update `backend/routes/tasks.py`
- **Features**:
  - Validate priority enum values
  - Handle tag array operations (add/remove/search)
  - Ensure proper validation for new fields

### 2.4 Implement Task Audit Trail
- **Location**: `backend/services/audit.py`
- **Features**:
  - Log create/update/complete/delete actions
  - Associate audit records with user IDs
  - Store action context and timestamps
  - Ensure all CRUD operations are audited

### 2.5 Update Existing Task Operations
- Enhance existing CRUD operations in `backend/routes/tasks.py` to handle new fields
- Maintain backward compatibility for existing functionality

**Deliverables**:
- New service files for recurrence and audit logic
- Updated task routes with enhanced functionality
- Validation and error handling for new features

## Phase 3 — REST API Expansion

### 3.1 Create Search Endpoint
- **Endpoint**: `POST /api/{user_id}/tasks/search`
- **Location**: `backend/routes/tasks.py`
- **Functionality**:
  - Accept search query string
  - Filter tasks by content across title, description, tags
  - Return paginated results
  - Apply user authorization checks

### 3.2 Create Filter Endpoint
- **Endpoint**: `POST /api/{user_id}/tasks/filter`
- **Location**: `backend/routes/tasks.py`
- **Functionality**:
  - Accept filter criteria (priority, tags, due date range, status, etc.)
  - Apply multiple filters simultaneously
  - Return filtered results with pagination

### 3.3 Create Sort Endpoint
- **Endpoint**: `POST /api/{user_id}/tasks/sort`
- **Location**: `backend/routes/tasks.py`
- **Functionality**:
  - Accept sort criteria (priority, due date, creation date, title)
  - Support ascending/descending order
  - Allow multiple sort criteria

### 3.4 Enhance Update Endpoint
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/update`
- **Location**: `backend/routes/tasks.py`
- **Functionality**:
  - Support partial updates for any field
  - Maintain backward compatibility with existing update functionality

### 3.5 Enhance Complete Endpoint
- **Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`
- **Location**: `backend/routes/tasks.py`
- **Functionality**:
  - Set completed_at timestamp
  - Trigger recurring task logic if task is recurring
  - Create audit record

### 3.6 Update Request Validation
- **Location**: `backend/models.py` (Pydantic models)
- **Functionality**:
  - Add validation for new fields in request models
  - Ensure proper validation for date formats and enum values
  - Add validation for recurrence rule format

**Deliverables**:
- New API endpoints in `backend/routes/tasks.py`
- Updated Pydantic models for request/response validation
- Enhanced OpenAPI documentation

## Phase 4 — MCP Tool Extensions

### 4.1 Create Priority Setting Tool
- **Tool**: `set_priority`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept task ID and priority value
  - Validate priority enum
  - Update task priority via backend API
  - Return confirmation

### 4.2 Create Tag Management Tool
- **Tool**: `add_tags`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept task ID and array of tags
  - Add tags to existing task
  - Validate tag format
  - Return updated task

### 4.3 Create Search Tool
- **Tool**: `search_tasks`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept search query
  - Call backend search API
  - Return matching tasks
  - Format results for chatbot

### 4.4 Create Filter Tool
- **Tool**: `filter_tasks`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept filter criteria
  - Call backend filter API
  - Return filtered tasks
  - Format results for chatbot

### 4.5 Create Sort Tool
- **Tool**: `sort_tasks`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept sort criteria
  - Call backend sort API
  - Return sorted tasks
  - Format results for chatbot

### 4.6 Create Due Date Tool
- **Tool**: `set_due_date`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept task ID and due date
  - Validate date format
  - Update task due date
  - Return confirmation

### 4.7 Create Reminder Tool
- **Tool**: `set_reminder`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept task ID and reminder time
  - Validate reminder time is in the future
  - Update task reminder time
  - Return confirmation

### 4.8 Create Recurrence Tool
- **Tool**: `set_recurrence`
- **Location**: `backend/src/mcp/server.py`
- **Functionality**:
  - Accept task ID and recurrence rule
  - Validate recurrence rule format
  - Update task recurrence settings
  - Return confirmation

### 4.9 Update MCP Server
- **Location**: `backend/src/mcp/server.py`
- Register all new tools with the MCP server
- Ensure proper authentication and user context
- Handle errors gracefully with user-friendly messages

**Deliverables**:
- All new MCP tools implemented in `backend/src/mcp/server.py`
- Proper error handling and validation for all tools
- Registration of tools with MCP server

## Phase 5 — Chat Agent Intent Mapping

### 5.1 Extend Intent Classification
- **Location**: `backend/src/ai/agent.py`
- **Functionality**:
  - Add detection for priority-related phrases ("set priority high", "priority low", etc.)
  - Add detection for tag-related phrases ("add tag work", "tag this", etc.)
  - Add detection for due date phrases ("due tomorrow", "due date", etc.)
  - Add detection for reminder phrases ("remind me", "set reminder", etc.)
  - Add detection for recurring phrases ("make recurring", "repeat weekly", etc.)
  - Add detection for search phrases ("search for", "find tasks", etc.)
  - Add detection for filter phrases ("show high priority", "filter by tag", etc.)
  - Add detection for sort phrases ("sort by date", "sort by priority", etc.)

### 5.2 Map Intents to MCP Tools
- **Location**: `backend/src/ai/agent.py`
- **Functionality**:
  - Map priority intents to `set_priority` tool
  - Map tag intents to `add_tags` tool
  - Map due date intents to `set_due_date` tool
  - Map reminder intents to `set_reminder` tool
  - Map recurring intents to `set_recurrence` tool
  - Map search intents to `search_tasks` tool
  - Map filter intents to `filter_tasks` tool
  - Map sort intents to `sort_tasks` tool

### 5.3 Update Agent Response Logic
- **Location**: `backend/src/ai/agent.py`
- **Functionality**:
  - Add confirmation responses for new actions
  - Add error handling for new tool failures
  - Enhance response formatting for new features
  - Maintain consistency with existing behavior

### 5.4 Update Prompt Engineering
- **Location**: `backend/src/ai/agent.py`
- **Functionality**:
  - Update system prompt to include new capabilities
  - Add examples for new natural language commands
  - Ensure agent knows about all new features

**Deliverables**:
- Updated AI agent with new intent classification
- Proper mapping to MCP tools for all new features
- Enhanced response formatting and error handling

## Phase 6 — Frontend Feature Integration

### 6.1 Create Priority Selector Component
- **Location**: `frontend/components/PrioritySelector/PrioritySelector.tsx`
- **Functionality**:
  - Dropdown or button group for selecting priority
  - Visual indication of priority levels (colors/icons)
  - Proper accessibility attributes

### 6.2 Create Tags Input Component
- **Location**: `frontend/components/TagsInput/TagsInput.tsx`
- **Functionality**:
  - Input field with tag chips display
  - Ability to add/remove tags
  - Validation for tag format
  - Suggestions for existing tags

### 6.3 Create Due Date Picker Component
- **Location**: `frontend/components/DatePicker/DatePicker.tsx`
- **Functionality**:
  - Calendar interface for selecting due dates
  - Time selection capability
  - Validation for future dates
  - Integration with task form

### 6.4 Create Reminder Picker Component
- **Location**: `frontend/components/ReminderPicker/ReminderPicker.tsx`
- **Functionality**:
  - Interface for setting reminder time
  - Time picker interface
  - Validation for future times
  - Integration with task form

### 6.5 Create Recurrence Controls Component
- **Location**: `frontend/components/RecurrenceControls/RecurrenceControls.tsx`
- **Functionality**:
  - Toggle for enabling recurrence
  - Selection for recurrence frequency
  - Form for recurrence rules
  - Integration with task form

### 6.6 Create Search Bar Component
- **Location**: `frontend/components/SearchBar/SearchBar.tsx`
- **Functionality**:
  - Input field for search queries
  - Integration with tasks list
  - Real-time filtering capability
  - Integration with API search endpoint

### 6.7 Create Filter Dropdown Component
- **Location**: `frontend/components/FilterDropdown/FilterDropdown.tsx`
- **Functionality**:
  - Multi-select interface for various filters
  - Priority filter
  - Status filter
  - Date range filter
  - Tag filter
  - Integration with API filter endpoint

### 6.8 Create Sort Dropdown Component
- **Location**: `frontend/components/SortDropdown/SortDropdown.tsx`
- **Functionality**:
  - Select for sort criteria
  - Direction control (ascending/descending)
  - Integration with API sort endpoint
  - Default sorting options

### 6.9 Enhance Task Card Component
- **Location**: `frontend/components/TaskItem/TaskItem.tsx`
- **Functionality**:
  - Display priority badges with appropriate colors
  - Show tag chips
  - Indicate recurring tasks with icon
  - Show due date with visual indicator
  - Show reminder time indicator

### 6.10 Update Task Form
- **Location**: `frontend/components/TaskForm/TaskForm.tsx`
- **Functionality**:
  - Integrate all new components (priority, tags, due date, etc.)
  - Handle new fields in form submission
  - Validate new fields before submission
  - Update success/error handling

### 6.11 Update API Client
- **Location**: `frontend/lib/api.ts`
- **Functionality**:
  - Add methods for new endpoints (search, filter, sort)
  - Add methods for updating new fields
  - Handle new field types in request/response
  - Maintain backward compatibility

### 6.12 Update Tasks Page
- **Location**: `frontend/app/tasks/page.tsx`
- **Functionality**:
  - Integrate search bar component
  - Integrate filter dropdown
  - Integrate sort dropdown
  - Update layout to accommodate new features
  - Update loading and error states

**Deliverables**:
- All new frontend components created
- Enhanced task card with visual indicators
- Updated task form with new inputs
- Updated API client with new methods
- Enhanced tasks page with search/filter/sort

## Phase 7 — End to End Validation

### 7.1 Create Integration Tests
- **Location**: `backend/tests/integration_test.py`
- **Functionality**:
  - Test recurring task creation and generation
  - Test priority setting and retrieval
  - Test tagging functionality
  - Test due date and reminder handling
  - Test search, filter, and sort functionality
  - Test audit trail recording

### 7.2 Create API Tests
- **Location**: `backend/tests/api_test.py`
- **Functionality**:
  - Test all new endpoints (search, filter, sort)
  - Test MCP tool calls
  - Test edge cases and error conditions
  - Test authentication for new endpoints

### 7.3 Create Frontend Tests
- **Location**: `frontend/tests/`
- **Functionality**:
  - Test new component rendering
  - Test user interactions with new features
  - Test API integration for new functionality
  - Test visual indicators and feedback

### 7.4 Manual QA Checklist
- **Document**: `docs/manual-qa-checklist.md`
- **Functionality**:
  - Create checklist for manual testing
  - Cover all new features
  - Include edge cases
  - Verify chat/UI parity

### 7.5 Performance Testing
- **Location**: `backend/tests/performance_test.py`
- **Functionality**:
  - Test API performance with new features
  - Verify response times are acceptable
  - Test with realistic data volumes

**Deliverables**:
- Integration tests for all new functionality
- API tests for new endpoints
- Manual QA checklist
- Performance validation

## Phase 8 — Finalization

### 8.1 Update Documentation
- **Location**: `docs/advanced-features.md`
- **Functionality**:
  - Document all new features and their usage
  - API endpoint documentation
  - Database schema changes
  - Frontend component documentation

### 8.2 Update API Contracts
- **Location**: `openapi.json` (auto-generated) and `docs/api-contracts.md`
- **Functionality**:
  - Ensure OpenAPI spec reflects new endpoints
  - Update API documentation with new request/response models
  - Document authentication for new endpoints

### 8.3 Create Release Notes
- **Document**: `docs/release-notes-phase-v.md`
- **Functionality**:
  - Summarize all changes made in this phase
  - Highlight breaking changes (if any)
  - Document migration requirements

### 8.4 Code Quality Review
- **Process**: Peer review of all new code
- **Functionality**:
  - Ensure all new code follows project standards
  - Verify security best practices
  - Check for potential performance issues

**Deliverables**:
- Updated documentation for new features
- Updated API contracts
- Release notes for Phase V
- Code quality review completion

## Success Criteria

- [ ] All new database fields are implemented and validated
- [ ] Recurring task functionality generates new instances correctly
- [ ] All new API endpoints function as specified
- [ ] MCP tools properly integrate with new functionality
- [ ] Chatbot recognizes and processes new natural language commands
- [ ] Frontend components provide intuitive interfaces for all features
- [ ] All tests pass successfully
- [ ] Existing functionality remains intact
- [ ] Documentation is updated and comprehensive
- [ ] Performance meets established benchmarks

## Risks & Mitigation

- **Risk**: Database schema changes affecting existing functionality
  - **Mitigation**: Thorough testing with backup/restore procedures

- **Risk**: Performance degradation with new search/filter operations
  - **Mitigation**: Proper indexing and performance testing

- **Risk**: Complexity in recurring task logic
  - **Mitigation**: Unit tests for each recurrence scenario

- **Risk**: Inconsistent behavior between UI and chatbot
  - **Mitigation**: Shared validation logic and integration tests

## Dependencies

- [ ] Phase III Todo Chatbot implementation (already completed)
- [ ] Existing authentication system (Better Auth/JWT)
- [ ] Database (Neon PostgreSQL)
- [ ] Cohere API for chatbot functionality
- [ ] MCP SDK for tool integration