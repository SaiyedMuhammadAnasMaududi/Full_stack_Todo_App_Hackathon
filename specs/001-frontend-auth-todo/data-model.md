# Data Model: Frontend Authentication and Todo Application

## Frontend Data Models

### User Entity
Represents a registered user of the application

**Fields**:
- `id`: string - Unique identifier for the user
- `email`: string - User's email address (validation: proper email format)
- `password`: string - User's password (validation: min 8 chars, mixed case, numbers, special chars)

**Validation Rules**:
- Email must be unique
- Email must follow standard email format
- Password must meet security requirements (min 8 chars, mixed case, numbers, special chars)

### Todo Task Entity
Represents a task item owned by a specific user

**Fields**:
- `id`: string - Unique identifier for the task
- `title`: string - Task title (required, max 255 chars)
- `description`: string - Optional task description (nullable, max 1000 chars)
- `completed`: boolean - Completion status (default: false)
- `userId`: string - Owner's user ID (foreign key reference)
- `createdAt`: Date - Creation timestamp
- `updatedAt`: Date - Last update timestamp

**Validation Rules**:
- Title is required and cannot be empty
- Title must be less than 255 characters
- Description, if provided, must be less than 1000 characters
- Task must belong to authenticated user

### Authentication Session Entity
Represents the user's authenticated state

**Fields**:
- `jwtToken`: string - JWT token string
- `expiresAt`: Date - Token expiration time
- `userId`: string - Associated user ID
- `refreshToken`: string - Refresh token (optional)

**Validation Rules**:
- JWT token must be valid and not expired
- Session must correspond to an existing user

## State Transitions

### Task State Transitions
- `incomplete` → `complete` (via toggle completion action)
- `complete` → `incomplete` (via toggle completion action)

### Session State Transitions
- `unauthenticated` → `authenticated` (on successful login/signup)
- `authenticated` → `unauthenticated` (on logout or token expiration)

## Relationships
- User (1) → (Many) Todo Task (one-to-many relationship)
- Authentication Session (1) → (1) User (one-to-one relationship)