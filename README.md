# Cloud-Native AI Todo Chatbot - Phase IV Deployment

This repository contains the Phase IV implementation of the AI-powered Todo Chatbot, deployed as a cloud-native application on local Kubernetes (Minikube) using AI-assisted DevOps tools.

## Features

- User registration and login with secure authentication
- JWT-based authorization for API requests
- Todo management: create, read, update, delete, and mark tasks as complete
- Responsive design for mobile and desktop
- Secure session management across browser tabs
- Network failure handling with retry mechanism
- AI-powered chatbot for natural language task management
- MCP tools integration for AI agent interactions
- Containerized deployment with Docker
- Helm-based deployment on Kubernetes
- AI-assisted DevOps operations (Gordon, kubectl-ai, Kagent)

## Architecture Overview

The application consists of:
- **Frontend**: Next.js 16+ application with AI chatbot integration
- **Backend**: FastAPI application with REST APIs and MCP tools
- **Database**: External Neon PostgreSQL database
- **AI Layer**: OpenAI Agents SDK with Cohere LLMs
- **Infrastructure**: Containerized services deployed via Helm charts on Minikube

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
- OpenAI Agents SDK
- Cohere API for LLMs

### Infrastructure
- Docker for containerization
- Kubernetes for orchestration
- Helm for packaging and deployment
- Minikube for local cluster
- AI-assisted DevOps tools (Gordon, kubectl-ai, Kagent)

## Getting Started

### Prerequisites

- Node.js 18+ for frontend
- Python 3.9+ for backend
- Access to Neon PostgreSQL database
- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.x
- kubectl
- Access to AI tools (Gordon, kubectl-ai, Kagent) - if unavailable, Claude Code will generate commands

### Local Development Setup

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

6. Navigate to the backend directory:
   ```bash
   cd backend
   ```
7. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
8. Set up environment variables
9. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## Cloud-Native Deployment

### Prerequisites for Kubernetes Deployment

- Docker Desktop with Kubernetes enabled OR Minikube
- Helm 3.x
- kubectl
- Access to AI tools (Gordon, kubectl-ai, Kagent)
- Environment variables configured (see .env.example)

### Deployment Instructions

#### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values for DATABASE_URL, COHERE_API_KEY, etc.
```

#### 2. Start Minikube Cluster

```bash
# Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=2

# Enable ingress addon for external access
minikube addons enable ingress
```

#### 3. Containerize Applications

Using Gordon (Docker AI Agent) for containerization:

```bash
# Containerize frontend (using Gordon)
docker ai "create optimized Dockerfile for Next.js frontend in ./frontend"
docker ai "build frontend image with production optimizations"

# Containerize backend (using Gordon)
docker ai "create optimized Dockerfile for FastAPI backend in ./backend with health checks"
docker ai "build backend image with production optimizations"
```

#### 4. Deploy with Helm

```bash
# Navigate to charts directory
cd charts

# Deploy backend first (to ensure services are available)
kubectl-ai "install backend helm chart with 2 replicas and health checks"

# Deploy frontend (with reference to backend service)
kubectl-ai "install frontend helm chart with 2 replicas and connect to backend service"
```

#### 5. Verify Deployment

```bash
# Check if pods are running
kubectl get pods

# Check services are available
kubectl get services

# Check if ingress is configured
kubectl get ingress

# Access the application
minikube service frontend-service --url
```

#### 6. Validate Functionality

1. Access the frontend UI and verify:
   - User authentication works
   - Todo CRUD operations function
   - AI chatbot is responsive
   - All Phase III functionality preserved

2. Test scaling:
   ```bash
   # Scale backend to 3 replicas
   kubectl-ai "scale backend deployment to 3 replicas"

   # Monitor resources
   kubectl get pods
   ```

## Helm Charts

### Backend Chart
Located at `charts/backend/`, includes:
- Deployment with health checks and resource limits
- Service for internal communication
- Secret management for sensitive data

### Frontend Chart
Located at `charts/frontend/`, includes:
- Deployment with health checks and resource limits
- Service for external access
- Secret management for frontend configuration

## AI Tool Commands Reference

- `docker ai "build optimized image for [service]"`: Containerize applications
- `kubectl-ai "deploy [resource] with [configuration]"`: Deploy and manage resources
- `kubectl-ai "scale [deployment] to [replicas]"`: Scale deployments
- `kagent "analyze [aspect] and suggest improvements"`: Get optimization recommendations

## Scaling and Management

### Horizontal Scaling

```bash
# Scale with kubectl-ai
kubectl-ai "scale frontend deployment to 4 replicas"
kubectl-ai "enable horizontal pod autoscaler for backend with CPU threshold 70%"

# Monitor with Kagent
kagent "analyze cluster resource usage and optimization opportunities"
```

### Configuration Updates

```bash
# Update configuration via ConfigMap
kubectl-ai "update frontend configmap with new environment variables"

# Apply updates with zero downtime
kubectl-ai "perform rolling update for frontend deployment"
```

## Troubleshooting

### Common Issues

- **Pods failing to start**: Check logs with `kubectl-ai "show logs for failed pods"`
- **Service connectivity**: Verify environment variables and service discovery with `kubectl-ai "debug service connectivity"`
- **Database connection**: Confirm DATABASE_URL is properly configured in Kubernetes Secrets

### Health Checks

- **Frontend**: `/api/health` endpoint should return 200
- **Backend**: `/health` endpoint should return 200
- **AI functionality**: Chat endpoint should respond to requests

## Architecture

The application follows a component-based architecture with:

- **Frontend**: Located in `frontend/` directory with Next.js App Router
- **Backend**: Located in `backend/` directory with FastAPI and SQLModel
- **Specifications**: Located in `specs/` directory with feature specifications
- **Helm Charts**: Located in `charts/` directory for Kubernetes deployment

## Security Features

- Passwords must meet security requirements (min 8 chars, mixed case, numbers, special chars)
- JWT tokens are stored securely with proper expiration checks
- Proactive token refresh 5 minutes before expiration
- Unauthorized access attempts are logged for security monitoring
- Shared session state across browser tabs
- Kubernetes Secrets for sensitive data management
- Container security with non-root users and read-only filesystems

## API Integration

The frontend communicates with the backend via REST API endpoints:

- `/api/{user_id}/tasks` - Task management endpoints
- Better Auth endpoints for authentication
- `/api/{user_id}/chat` - AI chatbot endpoints
- `/health` - Health check endpoints for both services

All API requests automatically include the JWT token via the centralized API client.

## Development Workflow

This project follows a Spec-Driven Development approach:

1. Define specifications in the `specs/` directory
2. Generate implementation plans with `/sp.plan`
3. Create task lists with `/sp.tasks`
4. Implement features following the generated tasks
5. Test and validate the implementation
6. Deploy containerized applications with AI-assisted DevOps tools

## Success Criteria

- [ ] Successfully deploy containerized frontend and backend applications to Minikube cluster
- [ ] Achieve horizontal scaling capability allowing the application to handle 10x concurrent users
- [ ] Maintain all Phase III functionality including Todo CRUD operations and AI chatbot interactions
- [ ] Complete deployment process using AI-assisted tools (Gordon, kubectl-ai, Kagent)
- [ ] Achieve sub-2-second response times for all API endpoints
- [ ] Ensure 100% of sensitive data is properly secured using Kubernetes Secrets