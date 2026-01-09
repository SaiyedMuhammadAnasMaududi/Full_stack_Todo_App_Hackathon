# Data Model: Secure Multi-User Todo Backend API

## Entity: User

### Fields
- **id**: UUID (Primary Key)
  - Type: `str` (UUID string format)
  - Required: Yes
  - Unique: Yes
  - Default: Generated using `uuid.uuid4()`
  - Purpose: Unique identifier for each user

- **email**: Email Address
  - Type: `str`
  - Required: Yes
  - Unique: Yes (Database constraint)
  - Index: Yes (For efficient lookups)
  - Purpose: User's email for identification

- **hashed_password**: Password Hash
  - Type: `str`
  - Required: Yes
  - Purpose: Securely stored password hash using bcrypt

- **created_at**: Creation Timestamp
  - Type: `datetime`
  - Required: Yes
  - Default: `datetime.utcnow()`
  - Purpose: Track when user account was created

- **updated_at**: Update Timestamp
  - Type: `datetime`
  - Required: Yes
  - Default: `datetime.utcnow()`
  - Purpose: Track when user account was last modified

### Relationships
- **tasks**: One-to-Many relationship with Task entity
  - Type: `List[Task]`
  - Back reference: `user` field in Task model
  - Cascade: Delete tasks when user is deleted

## Entity: Task

### Fields
- **id**: Task ID
  - Type: `str` (UUID string format)
  - Required: Yes
  - Primary Key: Yes
  - Default: Generated using `uuid.uuid4()`
  - Purpose: Unique identifier for each task

- **title**: Task Title
  - Type: `str`
  - Required: Yes
  - Max Length: 255 characters
  - Purpose: Brief description of the task

- **description**: Task Description
  - Type: `str` (Optional)
  - Required: No
  - Max Length: 1000 characters
  - Nullable: Yes
  - Purpose: Detailed description of the task

- **completed**: Completion Status
  - Type: `bool`
  - Required: Yes
  - Default: `False`
  - Purpose: Track whether task is completed

- **user_id**: Owner User ID (Foreign Key)
  - Type: `str` (UUID string format)
  - Required: Yes
  - Foreign Key: References `users.id`
  - Index: Yes (For efficient user-based queries)
  - Purpose: Link task to its owner user

- **created_at**: Creation Timestamp
  - Type: `datetime`
  - Required: Yes
  - Default: `datetime.utcnow()`
  - Purpose: Track when task was created

- **updated_at**: Update Timestamp
  - Type: `datetime`
  - Required: Yes
  - Default: `datetime.utcnow()`
  - Purpose: Track when task was last modified

### Relationships
- **user**: Many-to-One relationship with User entity
  - Type: `User`
  - Back reference: `tasks` field in User model
  - Purpose: Reference to the user who owns this task

## Validation Rules

### User Entity
- Email must be unique across all users
- Email format must be valid
- Password must be hashed before storage
- User ID must be unique and non-modifiable after creation

### Task Entity
- Title must be provided and not exceed 255 characters
- Task must be associated with a valid user (foreign key constraint)
- Only the task owner can modify or delete the task
- Task ID must be unique and non-modifiable after creation
- Completed status can be toggled by the task owner

## State Transitions

### Task State Transitions
- **Incomplete → Complete**: When user marks task as complete via PATCH `/api/{user_id}/tasks/{id}/complete`
- **Complete → Incomplete**: When user unmarks task as complete via PATCH `/api/{user_id}/tasks/{id}/complete`
- **Created**: When new task is added via POST `/api/{user_id}/tasks`
- **Updated**: When task details are modified via PUT `/api/{user_id}/tasks/{id}`
- **Deleted**: When task is removed via DELETE `/api/{user_id}/tasks/{id}`

## Database Constraints

### Primary Keys
- `users.id`: Unique identifier for each user
- `tasks.id`: Unique identifier for each task

### Foreign Keys
- `tasks.user_id` references `users.id`
- Enforces referential integrity between tasks and users

### Unique Constraints
- `users.email`: Ensures no duplicate email addresses

### Indexes
- `users.email`: For efficient user lookup by email
- `tasks.user_id`: For efficient task filtering by user
- `tasks.id`: For efficient task lookup by ID

## Security Considerations

### Data Isolation
- Each task is associated with a specific user via `user_id`
- All database queries must filter by `user_id` to enforce user isolation
- Foreign key constraints prevent orphaned tasks

### Access Control
- User authentication required for all operations
- User ID in JWT token must match `user_id` in database query
- No cross-user data access allowed