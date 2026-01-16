# Quickstart Guide: Secure Multi-User Todo Backend API

## Prerequisites

- Python 3.9+
- pip package manager
- Neon PostgreSQL account and connection string
- Better Auth secret key

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi sqlmodel python-jose uvicorn psycopg2-binary python-multipart
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.us-east-1.aws.neon.tech/db_name?sslmode=require
BETTER_AUTH_SECRET=your-better-auth-secret-key
JWT_ALGORITHM=HS256
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── models.py               # SQLModel database models
├── auth.py                 # JWT authentication utilities
├── db.py                   # Database connection and session management
├── routes/
│   └── tasks.py            # Task-related API routes
└── requirements.txt        # Project dependencies
```

## Database Setup

### 1. Initialize Database Tables
```bash
# This would typically be done in a separate script or via alembic migrations
python -c "
from models import create_db_and_tables
create_db_and_tables()
"
```

### 2. Verify Connection
```bash
python -c "
from db import engine
from sqlmodel import create_engine
try:
    with engine.connect() as conn:
        print('Database connection successful!')
except Exception as e:
    print(f'Database connection failed: {e}')
"
```

## Running the Application

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

Once the server is running, the following endpoints will be available:

### Authentication Required
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

### Available Endpoints

1. **Get User's Tasks**
   - `GET /api/{user_id}/tasks`
   - Returns all tasks for the specified user

2. **Create New Task**
   - `POST /api/{user_id}/tasks`
   - Creates a new task for the specified user
   - Request body: `{"title": "Task title", "description": "Optional description", "completed": false}`

3. **Get Specific Task**
   - `GET /api/{user_id}/tasks/{id}`
   - Returns details of a specific task

4. **Update Task**
   - `PUT /api/{user_id}/tasks/{id}`
   - Updates an existing task
   - Request body: `{"title": "New title", "description": "New description", "completed": true}`

5. **Delete Task**
   - `DELETE /api/{user_id}/tasks/{id}`
   - Deletes a specific task

6. **Toggle Task Completion**
   - `PATCH /api/{user_id}/tasks/{id}/complete`
   - Updates the completion status of a task
   - Request body: `{"completed": true}`

## Testing the API

### Using curl (replace YOUR_JWT_TOKEN and USER_ID with actual values):

```bash
# Get user's tasks
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/USER_ID/tasks

# Create a new task
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"title":"Sample Task","description":"A sample task","completed":false}' \
     http://localhost:8000/api/USER_ID/tasks

# Update a task
curl -X PUT \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"title":"Updated Task","completed":true}' \
     http://localhost:8000/api/USER_ID/tasks/TASK_ID

# Toggle task completion
curl -X PATCH \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"completed":true}' \
     http://localhost:8000/api/USER_ID/tasks/TASK_ID/complete
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify `DATABASE_URL` is correct
   - Ensure Neon PostgreSQL is accessible
   - Check firewall settings

2. **JWT Authentication Failures**
   - Confirm `BETTER_AUTH_SECRET` matches the one used to generate tokens
   - Verify token is not expired
   - Check that token format is "Bearer <TOKEN>"

3. **User ID Mismatch Errors**
   - Ensure the user_id in the URL matches the user_id in the JWT token
   - Verify the authenticated user has access to the requested resource

### Enable Logging
Add the following to your main.py for debugging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Security Notes

- Never expose the `BETTER_AUTH_SECRET` in client-side code
- Use HTTPS in production environments
- Validate and sanitize all user inputs
- Regularly rotate the JWT secret
- Monitor for unusual API usage patterns