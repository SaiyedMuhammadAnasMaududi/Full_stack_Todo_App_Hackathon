# Quickstart Guide: AI-Powered Conversational Todo Chatbot

## Overview

This guide provides step-by-step instructions to set up, configure, and run the AI-powered conversational Todo chatbot. Follow these steps to get the system running locally or deploy it to production.

## Prerequisites

### System Requirements
- Python 3.11+ (backend)
- Node.js 18+ (frontend)
- PostgreSQL-compatible database (Neon recommended)
- Docker (optional, for containerized deployment)

### Account Requirements
- Cohere API key (for LLM provider)
- Better Auth account (for authentication)
- OpenAI account (for ChatKit integration)

## Environment Setup

### Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# Database Configuration
DATABASE_URL="postgresql://username:password@host:port/database_name"

# Authentication
BETTER_AUTH_SECRET="your-better-auth-secret-key"

# AI Provider Configuration
COHERE_API_KEY="your-cohere-api-key"

# Optional: OpenAI Configuration (if using OpenAI for any components)
OPENAI_API_KEY="your-openai-api-key"
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory with the following variables:

```bash
# Backend API Configuration
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"

# Authentication
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:8000"

# Chat Integration
NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your-openai-domain-key"  # Required for ChatKit
```

## Installation Steps

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd <project-directory>
cd backend
```

### 2. Backend Setup

#### Install Backend Dependencies

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Initialize Database

```bash
# Apply database migrations (if using alembic)
alembic upgrade head

# Or run initial setup manually
python -c "from db import create_db_and_tables; create_db_and_tables()"
```

#### Run Backend Server

```bash
# Development mode
uvicorn main:app --reload --port 8000

# Or using the run script
python main.py
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

#### Run Frontend Development Server

```bash
npm run dev
```

## Key Configuration Files

### Backend Configuration (`backend/config.py`)

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # Authentication
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET")

    # AI Provider
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")

    # Application
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Todo Chatbot API"

    class Config:
        env_file = ".env"

settings = Settings()
```

### MCP Server Configuration (`backend/mcp/server.py`)

```python
from mcp.server import Server
from mcp.types import Tool, Completion, TextContent, ToolCallResult
import asyncio

# Initialize MCP server
server = Server("todo-chatbot-mcp")

# The server will be configured with the tools defined in the tools module
```

## Running the Application

### Development Mode

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

### Production Deployment

#### Backend

```bash
# Build and run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend

```bash
# Build the application
npm run build

# Serve the built application
npm run start
```

## Testing the Chatbot

### API Testing

Once the backend is running, you can test the chat endpoint:

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer <valid-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

### Frontend Testing

1. Navigate to the chat interface in the frontend application
2. Authenticate with your user account
3. Try sending messages like:
   - "Add a task: Buy groceries"
   - "Show me my tasks"
   - "Complete task 1"
   - "Update task 2 to 'Call mom tomorrow'"

## Troubleshooting

### Common Issues

#### Issue: Database Connection Failed
**Solution**: Verify `DATABASE_URL` in your `.env` file and ensure the database server is running.

#### Issue: Authentication Errors
**Solution**: Check that `BETTER_AUTH_SECRET` matches between frontend and backend configurations.

#### Issue: AI Provider Not Responding
**Solution**: Verify `COHERE_API_KEY` is valid and has sufficient quota.

#### Issue: Chat Endpoint Returns 401
**Solution**: Ensure JWT token is properly attached to requests and is not expired.

### Verification Steps

1. **Database Connection**:
   ```bash
   python -c "from db import engine; print('DB connected')"
   ```

2. **AI Provider**:
   ```bash
   python -c "from cohere import Client; client = Client(os.getenv('COHERE_API_KEY')); print('Cohere connected')"
   ```

3. **MCP Server**:
   ```bash
   python -c "from backend.ai.tools import *; print('MCP tools loaded')"
   ```

## Next Steps

1. **Customize Agent Behavior**: Modify the system prompt in `backend/ai/agent.py` to adjust the chatbot's personality and capabilities.

2. **Extend MCP Tools**: Add new tools in `backend/ai/tools.py` to expand the chatbot's capabilities.

3. **UI Customization**: Modify the chat interface components in `frontend/src/components/ChatBot/` to match your design requirements.

4. **Production Deployment**: Set up proper environment variables, SSL certificates, and monitoring for production deployment.

## Resources

- [API Documentation](contracts/openapi.yaml) - Detailed API specifications
- [Data Models](data-model.md) - Database schema and relationships
- [MCP Server Design](mcp-server-design.md) - Tool architecture and implementation
- [Troubleshooting Guide](troubleshooting.md) - Advanced debugging tips