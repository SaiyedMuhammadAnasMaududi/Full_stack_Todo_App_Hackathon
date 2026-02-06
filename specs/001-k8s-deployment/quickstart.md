# Quickstart: Cloud-Native Kubernetes Deployment of AI Todo Chatbot

## Prerequisites

- Docker Desktop with Kubernetes enabled OR Minikube installed
- Helm 3.x
- kubectl
- Access to AI tools (Gordon, kubectl-ai, Kagent) - if unavailable, Claude Code will generate commands
- Environment variables configured (see .env.example)

## Setup Instructions

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Set up environment variables
cp .env.example .env
# Edit .env with your actual values for DATABASE_URL, COHERE_API_KEY, etc.
```

### 2. Start Minikube Cluster

```bash
# Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=2

# Enable ingress addon for external access
minikube addons enable ingress
```

### 3. Containerize Applications

Using Gordon (Docker AI Agent) for containerization:

```bash
# Containerize frontend (using Gordon)
docker ai "create optimized Dockerfile for Next.js frontend in ./frontend"
docker ai "build frontend image with production optimizations"

# Containerize backend (using Gordon)
docker ai "create optimized Dockerfile for FastAPI backend in ./backend with health checks"
docker ai "build backend image with production optimizations"
```

If Gordon is unavailable, Claude Code will generate the Dockerfiles and build commands.

### 4. Deploy with Helm

```bash
# Navigate to charts directory
cd charts

# Deploy backend first (to ensure services are available)
kubectl-ai "install backend helm chart with 2 replicas and health checks"

# Deploy frontend (with reference to backend service)
kubectl-ai "install frontend helm chart with 2 replicas and connect to backend service"
```

### 5. Verify Deployment

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

### 6. Validate Functionality

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

## Troubleshooting

### Common Issues

- **Pods failing to start**: Check logs with `kubectl-ai "show logs for failed pods"`
- **Service connectivity**: Verify environment variables and service discovery with `kubectl-ai "debug service connectivity"`
- **Database connection**: Confirm DATABASE_URL is properly configured in Kubernetes Secrets

### Health Checks

- **Frontend**: `/health` endpoint should return 200
- **Backend**: `/health` endpoint should return 200
- **AI functionality**: Chat endpoint should respond to requests

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

## Cleanup

```bash
# Uninstall Helm releases
helm uninstall frontend-release
helm uninstall backend-release

# Stop Minikube
minikube stop
```

## AI Tool Commands Reference

- `docker ai "build optimized image for [service]"`: Containerize applications
- `kubectl-ai "deploy [resource] with [configuration]"`: Deploy and manage resources
- `kubectl-ai "scale [deployment] to [replicas]"`: Scale deployments
- `kagent "analyze [aspect] and suggest improvements"`: Get optimization recommendations