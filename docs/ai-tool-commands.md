# AI Tool Commands for Cloud-Native Deployment

This document lists all the AI-assisted DevOps commands used in the Phase IV deployment of the AI Todo Chatbot.

## Gordon (Docker AI Agent)

Gordon is used for containerization tasks, including Dockerfile generation and image building.

### Dockerfile Generation
```bash
# Generate optimized Dockerfile for frontend
docker ai "create optimized Dockerfile for Next.js frontend in ./frontend with health checks"

# Generate optimized Dockerfile for backend
docker ai "create optimized Dockerfile for FastAPI backend in ./backend with health checks"
```

### Image Building
```bash
# Build optimized frontend image
docker ai "build frontend image with production optimizations and security scanning"

# Build optimized backend image
docker ai "build backend image with production optimizations and security scanning"
```

## kubectl-ai

kubectl-ai is used for Kubernetes operations including deployment, scaling, and troubleshooting.

### Deployment Operations
```bash
# Install backend Helm chart
kubectl-ai "install backend helm chart with 2 replicas and health checks"

# Install frontend Helm chart
kubectl-ai "install frontend helm chart with 2 replicas and connect to backend service"

# Deploy with specific configurations
kubectl-ai "deploy the todo backend with 2 replicas and resource limits"
```

### Scaling Operations
```bash
# Scale deployments
kubectl-ai "scale backend deployment to 3 replicas"

# Enable horizontal pod autoscaler
kubectl-ai "enable horizontal pod autoscaler for backend with CPU threshold 70%"

# Scale frontend deployment
kubectl-ai "scale frontend deployment to 4 replicas"
```

### Troubleshooting
```bash
# Show logs for failed pods
kubectl-ai "show logs for failed pods"

# Debug service connectivity
kubectl-ai "debug service connectivity between frontend and backend"

# Analyze deployment issues
kubectl-ai "check why pods are failing"
```

### Configuration Management
```bash
# Update ConfigMap
kubectl-ai "update frontend configmap with new environment variables"

# Perform rolling updates
kubectl-ai "perform rolling update for frontend deployment"

# Update secrets
kubectl-ai "update backend secrets with new API keys"
```

## Kagent

Kagent is used for cluster health monitoring and resource optimization.

### Health Monitoring
```bash
# Analyze cluster resource usage
kagent "analyze cluster resource usage and optimization opportunities"

# Monitor cluster health
kagent "analyze cluster health and suggest improvements"

# Resource optimization
kagent "suggest resource optimization for deployed services"
```

## Common Command Patterns

### For Containerization
- `docker ai "build optimized image for [service]"`
- `docker ai "create Dockerfile for [language/tech] with multi-stage build"`
- `docker ai "optimize existing Dockerfile for security and size"`

### For Kubernetes Deployment
- `kubectl-ai "deploy [resource] with [configuration]"`
- `kubectl-ai "[operation] [resource-type] [resource-name] [parameters]"`
- `kubectl-ai "troubleshoot [issue-description]"`

### For Cluster Management
- `kagent "analyze [aspect] and suggest improvements"`
- `kagent "monitor [component] for [duration]"`
- `kagent "optimize [resource-type] for [goal]"`