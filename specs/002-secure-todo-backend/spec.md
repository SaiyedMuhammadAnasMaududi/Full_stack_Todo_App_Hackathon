# Secure Multi-User Todo Backend API

## Feature Overview
Implement a secure, multi-user todo application backend using Python FastAPI with JWT-based authentication and Neon Serverless PostgreSQL for data persistence. The system will provide RESTful APIs for todo task management while enforcing strict user isolation for all operations.

## Target Audience
- Backend developers implementing the API
- Frontend developers consuming the API
- Security auditors reviewing the implementation
- DevOps engineers deploying the service

## Success Criteria
The backend specification is considered satisfied when:

- All defined REST API endpoints are implemented and functional
- Every API request requires a valid JWT token
- JWT tokens are verified using a shared secret
- Authenticated users can only access their own tasks
- All 6 required Todo operations work correctly with proper authentication:
  - View Task List (GET /api/{user_id}/tasks)
  - Add Task (POST /api/{user_id}/tasks)
  - View Task Details (GET /api/{user_id}/tasks/{id})
  - Update Task (PUT /api/{user_id}/tasks/{id})
  - Delete Task (DELETE /api/{user_id}/tasks/{id})
  - Mark Task as Complete (PATCH /api/{user_id}/tasks/{id}/complete)
- Requests without valid authentication return `401 Unauthorized`
- Task ownership is enforced on every operation
- Data is persisted correctly in Neon PostgreSQL
- 99.9% API availability is maintained
- API response times remain under 200ms for 95% of requests

## User Scenarios & Testing

### Primary User Flow
1. User authenticates via frontend and receives JWT token
2. User makes API calls with Authorization header containing JWT
3. Backend verifies JWT and extracts user identity
4. Backend validates that user matches the user_id in the URL path
5. Backend performs requested operation on user's tasks only
6. Backend returns appropriate response or error

### Edge Cases
- Invalid JWT tokens return 401 Unauthorized
- User ID mismatch in URL vs JWT returns 403 Forbidden
- Attempting to access non-existent tasks returns 404 Not Found
- Malformed request bodies return 400 Bad Request
- Database connection failures return 500 Internal Server Error

## Functional Requirements

### Authentication & Authorization
- FR-001: System must verify JWT tokens sent in `Authorization: Bearer <JWT_TOKEN>` header
- FR-002: JWT verification must validate token signature using shared secret
- FR-003: JWT verification must validate token expiration
- FR-004: JWT verification must extract user identity (user_id, email)
- FR-005: System must reject requests where JWT is missing
- FR-006: System must reject requests where JWT is invalid or expired
- FR-007: System must reject requests where URL `user_id` does not match JWT user ID
- FR-008: System must enforce user isolation - users can only access their own tasks

### Todo Management Operations
- FR-009: GET /api/{user_id}/tasks must return only tasks owned by the authenticated user
- FR-010: POST /api/{user_id}/tasks must create a new task associated with the authenticated user
- FR-011: GET /api/{user_id}/tasks/{id} must return task only if owned by the authenticated user
- FR-012: PUT /api/{user_id}/tasks/{id} must allow modification only for user-owned tasks
- FR-013: DELETE /api/{user_id}/tasks/{id} must delete only tasks owned by the authenticated user
- FR-014: PATCH /api/{user_id}/tasks/{id}/complete must toggle completion status for user-owned task only

### Data Persistence
- FR-015: All task data must be stored in Neon Serverless PostgreSQL
- FR-016: Each task record must be associated with a user ID
- FR-017: System must use SQLModel as the ORM for database operations
- FR-018: System must not return data belonging to other users

### Error Handling
- FR-019: All unauthorized requests must return 401 Unauthorized status
- FR-020: All forbidden requests must return 403 Forbidden status
- FR-021: All non-existent resource requests must return 404 Not Found status
- FR-022: All malformed requests must return 400 Bad Request status

## Non-Functional Requirements

### Performance
- NFR-001: API response time should be under 200ms for 95% of requests
- NFR-002: System should support 100 concurrent users
- NFR-003: Database queries should complete within 100ms for 95% of requests

### Reliability
- NFR-004: System should maintain 99.9% uptime
- NFR-005: System should gracefully handle database connection failures
- NFR-006: System should implement proper error logging and monitoring

### Security
- NFR-007: All sensitive data must be encrypted at rest
- NFR-008: JWT tokens must be properly validated on each request
- NFR-009: SQL injection prevention through parameterized queries
- NFR-010: Input validation on all endpoints

### Scalability
- NFR-011: System should support horizontal scaling
- NFR-012: Database connection pooling should be implemented
- NFR-013: System should be stateless with no session storage

## Key Entities

### Task Entity
- ID: Unique identifier for the task (UUID, required, primary key)
- Title: Task title (string, required, max 255 characters)
- Description: Task description (string, optional, nullable)
- Completed: Boolean indicating completion status (boolean, default: false)
- User ID: Foreign key linking to user (UUID, required, foreign key to User.id)
- Created At: Timestamp of creation (datetime, required, auto-generated)
- Updated At: Timestamp of last update (datetime, required, auto-generated)

### User Entity
- ID: Unique identifier for the user (UUID, required, primary key)
- Email: User's email address (string, required, unique)
- Created At: Timestamp of account creation (datetime, required, auto-generated)
- Updated At: Timestamp of last update (datetime, required, auto-generated)

## API Endpoints Specification

### Authentication Headers
All endpoints require the following header:
- `Authorization: Bearer <JWT_TOKEN>`

### Common Response Formats

#### Success Responses
- `200 OK`: Operation successful with response body
- `201 Created`: Resource successfully created
- `204 No Content`: Operation successful with no response body

#### Error Responses
- `400 Bad Request`: Invalid request format or validation error
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: User ID mismatch or insufficient permissions
- `404 Not Found`: Requested resource does not exist
- `500 Internal Server Error`: Server-side error occurred

### Endpoint Details

#### 1. View Task List
- **Method**: GET
- **Path**: `/api/{user_id}/tasks`
- **Description**: Retrieve all tasks belonging to the authenticated user
- **Path Parameters**: user_id (UUID)
- **Query Parameters**: None
- **Request Body**: None
- **Response Body**: Array of Task objects
- **Success Status**: 200 OK

#### 2. Add Task
- **Method**: POST
- **Path**: `/api/{user_id}/tasks`
- **Description**: Create a new task for the authenticated user
- **Path Parameters**: user_id (UUID)
- **Request Body**:
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "completed": "boolean (optional, default: false)"
  }
  ```
- **Response Body**: Created Task object
- **Success Status**: 201 Created

#### 3. View Task Details
- **Method**: GET
- **Path**: `/api/{user_id}/tasks/{id}`
- **Description**: Retrieve details of a specific task
- **Path Parameters**: user_id (UUID), id (UUID)
- **Request Body**: None
- **Response Body**: Single Task object
- **Success Status**: 200 OK

#### 4. Update Task
- **Method**: PUT
- **Path**: `/api/{user_id}/tasks/{id}`
- **Description**: Update properties of an existing task
- **Path Parameters**: user_id (UUID), id (UUID)
- **Request Body**:
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
  ```
- **Response Body**: Updated Task object
- **Success Status**: 200 OK

#### 5. Delete Task
- **Method**: DELETE
- **Path**: `/api/{user_id}/tasks/{id}`
- **Description**: Delete a specific task
- **Path Parameters**: user_id (UUID), id (UUID)
- **Request Body**: None
- **Response Body**: None
- **Success Status**: 204 No Content

#### 6. Mark Task as Complete
- **Method**: PATCH
- **Path**: `/api/{user_id}/tasks/{id}/complete`
- **Description**: Toggle or set the completion status of a task
- **Path Parameters**: user_id (UUID), id (UUID)
- **Request Body**:
  ```json
  {
    "completed": "boolean (required)"
  }
  ```
- **Response Body**: Updated Task object
- **Success Status**: 200 OK

## Dependencies
- Better Auth: For JWT token generation and validation
- Neon PostgreSQL: For data persistence
- Python FastAPI: For API framework
- SQLModel: For ORM operations
- python-jose: For JWT handling

## Assumptions
- The frontend will handle user authentication and provide valid JWT tokens
- The BETTER_AUTH_SECRET environment variable will be properly configured
- Neon PostgreSQL database will be available and accessible
- Better Auth will provide JWT tokens with user_id and email claims
- The system will run in a stateless environment without server-side session storage

## Out of Scope
- Frontend UI or rendering logic
- Authentication UI flows (signup/signin pages)
- Role-based access control (admin, moderator, etc.)
- Real-time updates (WebSockets, SSE)
- Background jobs or task scheduling
- Analytics, logging dashboards, or monitoring tools
- Multi-tenant or organization-level features