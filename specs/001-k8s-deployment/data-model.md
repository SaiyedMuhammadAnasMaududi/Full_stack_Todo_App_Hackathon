# Data Model: Cloud-Native Kubernetes Deployment of AI Todo Chatbot

## Overview

The data model remains unchanged from Phase III, as the containerization and deployment to Kubernetes do not alter the underlying data structures. All data continues to be stored in the external Neon PostgreSQL database with the same schema.

## Key Entities

### Task
- **Description**: Represents a todo item created by a user
- **Fields**:
  - id: Unique identifier (UUID/String)
  - title: Task title (String)
  - description: Task details (String, nullable)
  - completed: Status indicator (Boolean)
  - user_id: Owner identifier (String/UUID)
  - created_at: Timestamp of creation (DateTime)
  - updated_at: Timestamp of last update (DateTime)

### User
- **Description**: Represents an authenticated user of the system
- **Fields**:
  - id: Unique identifier (String/UUID) - provided by Better Auth
  - email: User's email address (String)
  - created_at: Account creation timestamp (DateTime)
  - updated_at: Last update timestamp (DateTime)

### Conversation
- **Description**: Represents a chat conversation with the AI assistant
- **Fields**:
  - id: Unique identifier (UUID/String)
  - user_id: Owner identifier (String/UUID)
  - title: Conversation title (String)
  - created_at: Timestamp of creation (DateTime)
  - updated_at: Timestamp of last update (DateTime)

### Message
- **Description**: Represents a message within a conversation
- **Fields**:
  - id: Unique identifier (UUID/String)
  - conversation_id: Associated conversation (UUID/String)
  - role: Sender role ('user' or 'assistant') (String)
  - content: Message content (String)
  - created_at: Timestamp of creation (DateTime)

## Relationships

- **User → Task**: One-to-many (one user can have many tasks)
- **User → Conversation**: One-to-many (one user can have many conversations)
- **Conversation → Message**: One-to-many (one conversation contains many messages)

## Validation Rules

- **Task**: Must have a non-empty title, must be associated with a valid user_id
- **User**: Email must be unique and valid
- **Conversation**: Must be associated with a valid user_id
- **Message**: Must be associated with a valid conversation_id, role must be either 'user' or 'assistant'

## State Transitions

- **Task**: `completed` field can transition from `false` to `true` (via completion) or `true` to `false` (via uncompletion)
- **Message**: Immutable once created (append-only model for conversation history)

## Data Access Patterns

- **Task queries**: Always filtered by user_id for user isolation
- **Conversation queries**: Always filtered by user_id for user isolation
- **Message queries**: Always accessed through conversation_id with user validation
- **All queries**: Must validate user ownership for security