# Full-Stack Multi-User Todo Application

This is a secure, full-stack todo application featuring user authentication, task management, and JWT-based authorization.

## Features

- User registration and login with secure authentication
- JWT-based authorization for API requests
- Todo management: create, read, update, delete, and mark tasks as complete
- Responsive design for mobile and desktop
- Secure session management across browser tabs
- Network failure handling with retry mechanism

## Tech Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- React 19+
- Tailwind CSS for styling
- Axios for API requests
- Better Auth for authentication

### Backend
- Python FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL

## Getting Started

### Prerequisites

- Node.js 18+ for frontend
- Python 3.9+ for backend
- Access to Neon PostgreSQL database

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create environment file:
   ```bash
   cp .env.local.example .env.local
   ```
4. Update `.env.local` with your environment variables
5. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables
4. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## Architecture

The application follows a component-based architecture with:

- **Frontend**: Located in `frontend/` directory with Next.js App Router
- **Backend**: Located in `backend/` directory with FastAPI and SQLModel
- **Specifications**: Located in `specs/` directory with feature specifications

## Security Features

- Passwords must meet security requirements (min 8 chars, mixed case, numbers, special chars)
- JWT tokens are stored securely with proper expiration checks
- Proactive token refresh 5 minutes before expiration
- Unauthorized access attempts are logged for security monitoring
- Shared session state across browser tabs

## API Integration

The frontend communicates with the backend via REST API endpoints:

- `/api/{user_id}/tasks` - Task management endpoints
- Better Auth endpoints for authentication

All API requests automatically include the JWT token via the centralized API client.

## Development Workflow

This project follows a Spec-Driven Development approach:

1. Define specifications in the `specs/` directory
2. Generate implementation plans with `/sp.plan`
3. Create task lists with `/sp.tasks`
4. Implement features following the generated tasks
5. Test and validate the implementation