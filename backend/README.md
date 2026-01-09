# Secure Multi-User Todo Backend API

A secure, multi-user todo application backend built with Python FastAPI, JWT authentication, and Neon Serverless PostgreSQL.

## Features

- JWT-based authentication and authorization
- Multi-user support with strict user isolation
- Full CRUD operations for tasks
- Rate limiting to prevent abuse
- Performance monitoring and metrics
- Caching for frequently accessed data
- Connection pooling for database optimization

## Prerequisites

- Python 3.9+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

1. Install UV package manager:
   ```bash
   pip install uv
   ```

2. Clone the repository and navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create a virtual environment:
   ```bash
   uv venv
   ```

4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   uv pip install -e .
   ```

### Using pip

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the backend directory with the following variables:

```env
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

Generate a secret key using:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

For Neon Serverless PostgreSQL, your DATABASE_URL would look like:
```
postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## Running the Application

### Development

```bash
uvicorn main:app --reload --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

Or using a process manager like gunicorn:

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Documentation

Once the application is running, API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Authentication
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/register` - Register a new user

### Tasks (per user)
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

### System
- `GET /health` - Health check
- `GET /metrics` - Performance metrics

## Security Features

- JWT token-based authentication
- User ID validation in JWT vs URL path
- Task ownership verification in database queries
- Rate limiting on all endpoints
- Input validation for all requests
- Proper error responses (401, 403, 404)

## Performance Features

- Database connection pooling
- Response time metrics and monitoring
- Caching for frequently accessed data
- Proper indexing for optimized queries

## Environment Variables

- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: Algorithm for JWT encoding (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `DATABASE_URL`: Database connection string
- `ENVIRONMENT`: Environment (development, production)

## Docker Support

To run with Docker:

```bash
# Build the image
docker build -t secure-todo-backend .

# Run the container
docker run -p 8000:8000 -e DATABASE_URL=your_db_url secure-todo-backend
```

## Testing

To run tests:

```bash
pytest
```

## Deployment

### Heroku

1. Create a new Heroku app
2. Add PostgreSQL addon
3. Deploy using Git

### AWS/GCP/Azure

1. Set up a VM or container service
2. Configure environment variables
3. Deploy using Docker or directly with Python

## Monitoring

The application exposes metrics at `/metrics` endpoint with:
- Total requests
- Error rates
- Response time percentiles (p50, p95, p99)
- Per-endpoint statistics