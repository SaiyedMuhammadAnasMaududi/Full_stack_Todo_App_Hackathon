# Implementation Plan: AI-Powered Conversational Todo Chatbot

**Branch**: `003-ai-chatbot-integration` | **Date**: 2026-01-15 | **Spec**: [specs/003-ai-chatbot-integration/spec.md](../003-ai-chatbot-integration/spec.md)

**Input**: Feature specification from `/specs/003-ai-chatbot-integration/spec.md`

## Summary

Implementation of an AI-powered conversational Todo chatbot that integrates with the existing full-stack Todo application. The system will use OpenAI Agents SDK with Cohere as the LLM provider, expose task operations via an Official MCP Server, and maintain stateless architecture with database-persisted conversation state. The chatbot will enable natural language task management (add, list, update, complete, delete) while preserving all existing REST-based functionality.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/Next.js 14+
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Cohere, Official MCP SDK, Better Auth
**Storage**: Neon Serverless PostgreSQL (existing + new tables for conversations/messages)
**Testing**: pytest (backend), vitest (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <3 second response times for typical chat interactions, maintain existing REST API performance within 10%
**Constraints**: <200ms p95 for database queries, stateless backend (no in-memory session state), secure user isolation
**Scale/Scope**: Up to 10k concurrent users, persistent conversations for 30+ days

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Statelessness**: All conversational state must be stored in the database, no server-side session memory allowed
- ✅ **Single Source of Truth**: Database is the only source of truth for tasks, conversations, messages
- ✅ **Authentication & Identity**: Better Auth JWT tokens mandatory for all APIs (REST and Chat)
- ✅ **User Isolation**: Every task, conversation, and message owned by exactly one user with proper filtering
- ✅ **REST API Stability**: Existing REST endpoints must not change (URLs, HTTP methods, semantics)
- ✅ **AI & Agent Rules**: AI agent can only change state via MCP tools, cannot access DB directly
- ✅ **Conversational Architecture**: Chat endpoint must load history from DB, run agent, persist response
- ✅ **Environment Variables**: All secrets via env vars only (no hardcoding)

## Project Structure

### Documentation (this feature)
```text
specs/003-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py          # Existing task model
│   │   ├── conversation.py  # New: Conversation model
│   │   └── message.py       # New: Message model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # JWT verification
│   │   ├── tasks.py         # Task operations
│   │   └── conversations.py # New: Conversation operations
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tasks.py         # Existing task routes
│   │   └── chat.py          # New: Chat API endpoint
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── agent.py         # New: AI agent configuration
│   │   └── tools.py         # New: MCP tools implementation
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── server.py        # New: MCP server implementation
│   └── db.py                # Database connection
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatBot/
│   │   │   ├── ChatBot.tsx      # New: Main chat interface
│   │   │   ├── ChatWindow.tsx   # New: Chat window component
│   │   │   └── MessageBubble.tsx # New: Message display component
│   │   ├── TaskList/
│   │   └── AppWrapper/
│   ├── pages/
│   │   ├── index.tsx
│   │   └── chat.tsx             # New: Dedicated chat page or integrated component
│   ├── lib/
│   │   ├── api.ts               # API client (existing)
│   │   └── auth.ts              # Auth utilities (existing)
│   └── hooks/
│       └── useChat.ts           # New: Chat-related hooks
└── tests/
    └── components/

```

**Structure Decision**: Web application structure with separate backend and frontend directories. Backend handles AI agent logic, MCP tools, and conversation persistence. Frontend provides chat interface integrated with existing Todo UI.

## Phase 1: Architecture & Integration Design

### 1.1 High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   External      │
│   (Next.js)     │    │    (FastAPI)     │    │   Services      │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│                 │    │                  │    │                 │
│ Chat Interface  │◄──►│  Chat Endpoint   │    │   Cohere LLM    │
│ (ChatKit UI)    │    │ POST /api/{id}/  │    │                 │
│                 │    │     chat         │    │                 │
└─────────────────┘    │                  │    │                 │
                       ├──────────────────┤    ├─────────────────┤
                       │                  │    │                 │
                       │  OpenAI Agent    │◄──►│ MCP Tools       │
                       │    SDK           │    │ (via MCP server)│
                       │                  │    │                 │
                       ├──────────────────┤    ├─────────────────┤
                       │                  │    │                 │
                       │  JWT Auth        │    │                 │
                       │  Validation      │    │                 │
                       │                  │    │                 │
                       ├──────────────────┤    ├─────────────────┤
                       │                  │    │                 │
                       │ Neon PostgreSQL  │    │                 │
                       │ - Tasks          │    │                 │
                       │ - Conversations  │    │                 │
                       │ - Messages       │    │                 │
                       │                  │    │                 │
                       └──────────────────┘    └─────────────────┘
```

Data flow: User message → JWT validation → Conversation history fetch → Agent execution with MCP tools → Response persistence → Client response

### 1.2 Component Responsibilities

**Frontend Components:**
- ChatBot: Main chat interface component with message history display
- ChatWindow: Container for chat interactions
- MessageBubble: Individual message display with sender differentiation
- useChat hook: Manages chat state and API communication

**Backend Components:**
- Chat endpoint: `/api/{user_id}/chat` - handles JWT validation, conversation persistence
- OpenAI Agent: Processes natural language and selects appropriate MCP tools
- MCP Server: Exposes task operations as tools for the agent
- Database models: Conversation and Message entities with user relationships

### 1.3 Key Decisions & Rationale

**Stateless Architecture Decision:**
- Why: Ensures horizontal scalability and fault tolerance
- Alternative: In-memory session state
- Rationale: Constitution mandates no server-side session memory; database persistence ensures reliability

**MCP Tool-Only Access Decision:**
- Why: Maintains clean separation between AI reasoning and data operations
- Alternative: Direct database access from AI agent
- Rationale: Constitution requires all state changes via MCP tools; ensures proper validation and user isolation

**Cohere as LLM Provider Decision:**
- Why: Specific requirement from user specifications
- Alternative: OpenAI GPT, Anthropic Claude
- Rationale: User explicitly requested Cohere integration via OpenAI Agents SDK abstraction

**Preserve REST APIs Decision:**
- Why: Maintain backward compatibility and existing functionality
- Alternative: Redesign entire API around AI interactions
- Rationale: Constitution requires no changes to existing REST endpoints; preserves existing client integrations

## Phase 2: Specification-to-Tool Mapping

### 2.1 Natural Language Intents → MCP Tools Mapping

| User Intent | MCP Tool | Parameters | Example Queries |
|-------------|----------|------------|-----------------|
| Add Task | `add_task` | `title`, `description` (optional) | "Add a task: Buy groceries", "Create task to finish report" |
| List Tasks | `list_tasks` | `status` (optional) | "Show my tasks", "What do I have to do?", "List incomplete tasks" |
| Update Task | `update_task` | `task_id`, `title` (optional), `description` (optional) | "Change task 'buy milk' to 'buy almond milk'", "Update my meeting time" |
| Complete Task | `complete_task` | `task_id` | "Mark task 5 as complete", "Finish my meeting task", "Done with grocery list" |
| Delete Task | `delete_task` | `task_id` | "Delete task 3", "Remove my shopping list" |

### 2.2 Error Handling Strategy

**Task Not Found Errors:**
- Scenario: User references a task that doesn't exist
- Response: Agent explains the task wasn't found and suggests alternatives
- MCP Tool Behavior: Tools return appropriate error responses

**Invalid Task ID Errors:**
- Scenario: User provides malformed task ID
- Response: Agent requests clarification with valid examples
- MCP Tool Behavior: Tools validate input and return validation errors

**Empty List Errors:**
- Scenario: User requests tasks but none exist
- Response: Agent confirms no tasks found and invites creating new tasks
- MCP Tool Behavior: Tools return empty array with appropriate messaging

### 2.3 Confirmation Message Patterns

**Success Confirmations:**
- Add: "I've added the task '{title}' to your list."
- List: "Here are your tasks: {list of tasks}"
- Update: "I've updated the task '{title}'."
- Complete: "I've marked '{title}' as complete."
- Delete: "I've removed the task '{title}'."

**Error Confirmations:**
- Invalid input: "I couldn't understand that. Could you please rephrase?"
- Permission denied: "You don't have permission to access that task."
- Not found: "I couldn't find the task you're looking for."

## Phase 3: MCP Server Planning

### 3.1 MCP Server Responsibilities

**Stateless Tool Execution:**
- Each tool invocation is independent with no shared state
- Tools receive all necessary context via parameters
- No persistent connections or cached data between invocations

**Task Ownership Enforcement:**
- Each tool validates that the requesting user owns the target task
- Database queries are filtered by authenticated user ID
- Unauthorized access attempts are logged and rejected

**Database Persistence via SQLModel:**
- All data operations use existing SQLModel patterns
- Consistent transaction handling and error management
- Proper relationship mapping between users, tasks, and conversations

### 3.2 MCP Tools Specification

**add_task(title: str, description: str = None) -> dict**
- Creates a new task for the authenticated user
- Validates input parameters
- Returns created task object with ID

**list_tasks(status: str = None) -> list**
- Retrieves tasks for the authenticated user
- Optionally filters by completion status
- Returns list of task objects

**update_task(task_id: int, title: str = None, description: str = None) -> dict**
- Updates specified fields of an existing task
- Validates user ownership of the task
- Returns updated task object

**complete_task(task_id: int) -> dict**
- Marks a task as completed
- Validates user ownership of the task
- Returns updated task object

**delete_task(task_id: int) -> dict**
- Deletes an existing task
- Validates user ownership of the task
- Returns deletion confirmation

### 3.3 Input Validation Strategy

Each MCP tool implements comprehensive input validation:
- Type checking for all parameters
- Length and format validation for strings
- Range validation for numeric values
- Existence validation for referenced entities
- Ownership validation for user-specific resources

### 3.4 Ownership Verification Logic

All MCP tools follow the pattern:
1. Extract user_id from authenticated context
2. Verify the target resource belongs to the authenticated user
3. Proceed with operation only if ownership is confirmed
4. Return appropriate error if ownership validation fails

### 3.5 Consistent Tool Response Schema

All MCP tools return standardized responses:
```json
{
  "success": true/false,
  "data": { ... }, // Operation result or null
  "error": { ... }, // Error details or null
  "timestamp": "ISO datetime"
}
```

## Phase 4: AI Agent Design (OpenAI Agents SDK)

### 4.1 Agent Configuration

**Agent Instructions:**
- Focus on task-oriented interactions
- Prioritize tool usage over generating responses
- Maintain friendly, helpful tone
- Confirm all actions with user-appropriate language
- Handle errors gracefully with helpful suggestions

**Tool Availability Rules:**
- Only MCP tools are available to the agent
- No direct database or API access
- Tools are registered dynamically based on user permissions
- Tool parameters are validated before execution

**Multi-Tool Chaining Logic:**
- Agent can execute multiple tools in a single interaction
- Sequential execution with context passing between tools
- Error handling to prevent cascading failures
- Transaction-like behavior where possible

### 4.2 LLM Provider Configuration

**Cohere Integration:**
- Use Cohere via OpenAI Agents SDK abstraction
- Configure API key from environment variables
- Set appropriate model parameters for task-focused interactions
- Implement fallback mechanisms for service availability

**Provider-Agnostic Design:**
- Abstract LLM provider behind consistent interface
- Allow easy switching between providers if needed
- Minimize provider-specific configurations
- Maintain consistent behavior across providers

## Phase 5: Chat API Endpoint Planning

### 5.1 Endpoint Design

**POST /api/{user_id}/chat**
- Accepts user message and conversation context
- Requires valid JWT authentication
- Validates user_id against token identity
- Returns AI response and any tool call results

### 5.2 Request Lifecycle

1. **JWT Verification**: Validate token signature and extract user identity
2. **User ID Validation**: Confirm request user_id matches token identity
3. **Conversation History Fetch**: Load recent conversation from database
4. **Message Persistence**: Store incoming user message in database
5. **Agent Input Construction**: Combine history + new message for agent
6. **Agent Execution**: Run agent with MCP tools
7. **Response Persistence**: Store assistant response in database
8. **Response Construction**: Return response + tool calls to client

### 5.3 Statelessness Design

**Database-Backed Conversations:**
- No server-side session memory
- Each request loads necessary context from database
- Conversation state persists across server restarts
- Multiple server instances can handle requests equally

## Phase 6: Frontend Chat Integration Planning

### 6.1 UI Integration Points

**Chat Interface Options:**
- Dedicated chat page accessible from main navigation
- Integrated chat panel that overlays the task list
- Floating chat widget that can be toggled open/closed

**Message Display:**
- Differentiated styling for user vs assistant messages
- Loading indicators during AI processing
- Clear display of action confirmations
- Support for rich text and structured responses

### 6.2 Security Implementation

**JWT Token Attachment:**
- Attach JWT token to all chat API requests
- Handle 401 responses gracefully with redirect to login
- Refresh token mechanism if needed
- Secure storage of tokens in browser

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional database tables | Need to store conversations and messages | Would violate statelessness principle without persistence |
| MCP server architecture | Required by constitution for AI-to-data access | Direct database access would violate tool-only rule |
| Separate AI agent layer | Provides proper abstraction and reasoning capability | Embedding logic in endpoints would create tight coupling |
