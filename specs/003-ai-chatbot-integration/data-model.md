# Data Model: AI-Powered Conversational Todo Chatbot

## Overview

This document defines the data models required for implementing the AI-powered conversational Todo chatbot. The design extends the existing task management system with new entities for conversations and messages while maintaining user isolation and security requirements.

## Entity Models

### 1. Conversation Model

**Entity Name**: `Conversation`
**Purpose**: Represents a sequence of messages between a user and the AI assistant

**Fields**:
- `id` (Integer, Primary Key, Auto-increment)
  - Unique identifier for the conversation
  - Required: Yes
  - Constraints: Auto-generated, unique

- `user_id` (String, Foreign Key)
  - References the user who owns this conversation
  - Required: Yes
  - Constraints: Must reference a valid user, indexed for performance

- `title` (String, Optional)
  - Human-readable title for the conversation (auto-generated from first message or topic)
  - Required: No
  - Constraints: Max length 200 characters

- `created_at` (DateTime)
  - Timestamp when the conversation was created
  - Required: Yes
  - Constraints: Auto-set on creation

- `updated_at` (DateTime)
  - Timestamp when the conversation was last updated
  - Required: Yes
  - Constraints: Auto-updated on modification

- `is_active` (Boolean)
  - Indicates if the conversation is currently active
  - Required: Yes
  - Default: True
  - Constraints: Used for soft deletion/archive

**Relationships**:
- One-to-Many: User has many conversations
- One-to-Many: Conversation has many messages

**Validation Rules**:
- `user_id` must correspond to an existing user
- `title` must be less than 200 characters if provided
- `created_at` cannot be in the future
- `updated_at` cannot be before `created_at`

### 2. Message Model

**Entity Name**: `Message`
**Purpose**: Represents an individual message within a conversation

**Fields**:
- `id` (Integer, Primary Key, Auto-increment)
  - Unique identifier for the message
  - Required: Yes
  - Constraints: Auto-generated, unique

- `conversation_id` (Integer, Foreign Key)
  - References the conversation this message belongs to
  - Required: Yes
  - Constraints: Must reference a valid conversation

- `sender_type` (Enum: 'user' | 'assistant')
  - Indicates who sent the message
  - Required: Yes
  - Constraints: Must be either 'user' or 'assistant'

- `content` (Text)
  - The actual message content
  - Required: Yes
  - Constraints: Max length 10,000 characters

- `role` (Enum: 'user' | 'assistant' | 'tool_call' | 'tool_response')
  - The role this message plays in the conversation context
  - Required: Yes
  - Constraints: Defines how the message should be processed by the AI agent

- `tool_calls` (JSON, Optional)
  - Stores any tool calls made in this message (for assistant messages)
  - Required: No
  - Format: Array of tool call objects with name, arguments, etc.

- `tool_responses` (JSON, Optional)
  - Stores responses from tools called in this conversation turn (for assistant messages)
  - Required: No
  - Format: Array of tool response objects

- `timestamp` (DateTime)
  - When the message was created
  - Required: Yes
  - Constraints: Auto-set on creation

- `sequence_number` (Integer)
  - Order of the message within the conversation
  - Required: Yes
  - Constraints: Unique within conversation, auto-incremented

**Relationships**:
- Many-to-One: Message belongs to one Conversation
- One-to-Many: Message may have many tool call responses (conceptual)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `sender_type` must be 'user' or 'assistant'
- `role` must be one of the allowed values
- `content` must be provided and not exceed length limits
- `sequence_number` must be unique within the conversation
- `timestamp` cannot be in the future

### 3. Task Model (Existing - Extended)

**Entity Name**: `Task`
**Purpose**: Represents a user's todo item (existing model with extended considerations)

**Extended Relationships**:
- One-to-Many: User has many tasks (existing)
- One-to-Many: Conversation messages may reference tasks (conceptual via content)

**Considerations for AI Integration**:
- Task operations will be performed via MCP tools
- No direct foreign key relationships between messages and tasks
- Task references will be handled through natural language processing

## Database Schema

```sql
-- Conversation table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_conversations_user_id (user_id),
    INDEX idx_conversations_created_at (created_at)
);

-- Message table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    sender_type VARCHAR(20) NOT NULL CHECK (sender_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'tool_call', 'tool_response')),
    tool_calls JSON,
    tool_responses JSON,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sequence_number INTEGER NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    UNIQUE (conversation_id, sequence_number),
    INDEX idx_messages_conversation_id (conversation_id),
    INDEX idx_messages_timestamp (timestamp)
);
```

## Indexing Strategy

### Primary Indexes
- `conversations.id`: Primary key index (auto-created)
- `messages.id`: Primary key index (auto-created)

### Secondary Indexes
- `conversations.user_id`: For efficient user-based queries
- `conversations.created_at`: For chronological ordering
- `messages.conversation_id`: For conversation-based queries
- `messages.timestamp`: For chronological ordering within conversations

### Composite Indexes
- `(conversation_id, sequence_number)`: For ordered message retrieval within conversations

## State Transitions

### Conversation States
- `Active` → `Archived`: When user indicates conversation is complete
- `Active` → `Deleted`: When user deletes conversation (soft delete with `is_active = FALSE`)

### Message States
- Messages are immutable once created
- No state transitions for individual messages
- Entire conversation can be archived or deleted

## Validation Rules

### Business Logic Validation
1. **User Ownership**: All queries must filter by authenticated user ID
2. **Conversation Limits**: Maximum 10,000 messages per conversation to prevent excessive storage
3. **Message Length**: Content must be between 1 and 10,000 characters
4. **Temporal Consistency**: Timestamps must be logically consistent

### Data Integrity Validation
1. **Foreign Key Constraints**: All relationships enforced at database level
2. **Type Constraints**: Proper data types for all fields
3. **Required Fields**: Non-null constraints for mandatory fields
4. **Check Constraints**: Enum values and business rules enforced

## Relationship Constraints

### Referential Integrity
- Cascading delete from Conversation to Messages
- Restrict deletion of user if active conversations exist (configurable)

### Access Control
- All queries must include user_id filter
- No cross-user access allowed
- Authentication required for all operations

## Performance Considerations

### Query Optimization
- Most queries will be by user_id and conversation context
- Pagination support for long conversations
- Efficient retrieval of recent conversations

### Storage Optimization
- Text compression for message content (database-level)
- Automatic archival of old conversations (application-level)
- Index optimization for common query patterns

## Extension Points

### Future Enhancements
- Message reactions/annotations
- Conversation tagging/categorization
- Message threading/replies
- Rich media content support

### Integration Points
- AI agent context windows
- Tool call result tracking
- Conversation analytics
- Export functionality