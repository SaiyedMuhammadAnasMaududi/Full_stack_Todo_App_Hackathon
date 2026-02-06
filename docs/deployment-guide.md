# Deployment Guide: AI Todo Chatbot on Kubernetes

This guide provides instructions for deploying the AI Todo Chatbot to a Kubernetes cluster using the prepared containerized images and Helm charts.

## Prerequisites

- **Kubernetes cluster** (Minikube, Kind, or cloud-based)
- **Helm 3.x** installed
- **kubectl** installed and configured
- **Docker** (for local image building)

## Deployment Architecture

The application consists of:

- **Frontend**: Next.js application serving the UI and chatbot interface
- **Backend**: FastAPI application providing REST APIs and MCP tools
- **External Database**: Neon PostgreSQL (configured via secrets)
- **AI Services**: Cohere integration for chatbot functionality

## Quick Deploy (Minikube)

For local testing with Minikube:

```bash
# Start Minikube
minikube start --memory=4096 --cpus=2



# Deploy using the provided script
./scripts/deploy-k8s.sh
```

## Manual Deployment Steps

### 1. Prepare Container Images

Build the container images:

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..
```

### 2. Create Namespace

```bash
kubectl create namespace todo-app
```

### 3. Configure Environment Variables

Create a `secrets.yaml` file with your actual secrets:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
  namespace: todo-app
type: Opaque
data:
  database_url: <base64-encoded-database-url>
  cohere_api_key: <base64-encoded-cohere-key>
  better_auth_secret: <base64-encoded-jwt-secret>
```

Apply the secrets:

```bash
kubectl apply -f secrets.yaml
```

### 4. Deploy with Helm

```bash
# Install backend first
helm upgrade --install backend ./charts/backend \
    --namespace todo-app \
    --set image.repository=todo-backend \
    --set image.tag=latest \
    --set secrets.existingSecret=todo-app-secrets

# Install frontend
helm upgrade --install frontend ./charts/frontend \
    --namespace todo-app \
    --set image.repository=todo-frontend \
    --set image.tag=latest \
    --set env.NEXT_PUBLIC_BACKEND_URL=http://backend.todo-app.svc.cluster.local \
    --set secrets.existingSecret=todo-app-secrets
```

## Environment Configuration

Required environment variables for deployment:

### Backend Secrets
- `DATABASE_URL` - PostgreSQL connection string
- `COHERE_API_KEY` - Cohere API key for AI services
- `BETTER_AUTH_SECRET` - JWT secret for authentication

### Backend Configuration
- `BACKEND_PORT` - Port to listen on (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)
- `DEBUG` - Debug mode (default: False)

### Frontend Configuration
- `NEXT_PUBLIC_BACKEND_URL` - URL of the backend service
- `NEXT_PUBLIC_COHERE_API_KEY` - Cohere API key (if needed client-side)
- `NEXT_PUBLIC_BETTER_AUTH_SECRET` - JWT secret (if needed client-side)

## Scaling Configuration

The deployment includes Horizontal Pod Autoscalers:

- **Backend**: Scales based on CPU and memory usage
- **Frontend**: Scales based on CPU and memory usage

Default configuration:
- Min replicas: 2
- Max replicas: 5
- Target CPU utilization: 70%
- Target memory utilization: 80%

To update scaling configuration:

```bash
# Update backend HPA
helm upgrade --install backend ./charts/backend \
    --namespace todo-app \
    --set autoscaling.enabled=true \
    --set autoscaling.minReplicas=3 \
    --set autoscaling.maxReplicas=10 \
    --set autoscaling.targetCPUUtilizationPercentage=60
```

## Health Checks

The application provides health check endpoints:

- **Backend**: `GET /health` - Returns service status
- **Frontend**: `GET /api/health` - Returns application status

These are used for Kubernetes liveness and readiness probes.

## Service Discovery

Services communicate internally using Kubernetes DNS:

- Backend service: `backend.todo-app.svc.cluster.local`
- Frontend service: `frontend.todo-app.svc.cluster.local`

## Validation

After deployment, validate the installation:

```bash
./scripts/validate-deployment.sh
```

Or manually check:

```bash
# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get services -n todo-app

# Check deployments
kubectl get deployments -n todo-app

# Check HPA
kubectl get hpa -n todo-app

# View logs
kubectl logs -n todo-app deployment/backend
kubectl logs -n todo-app deployment/frontend
```

## Monitoring

Monitor the deployed application:

```bash
# Watch pods
kubectl get pods -n todo-app --watch

# Check resource usage
kubectl top pods -n todo-app

# Monitor events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

## Troubleshooting

Common issues and solutions:

### Pods Not Starting
- Check pod logs: `kubectl logs -n todo-app <pod-name>`
- Check events: `kubectl describe pod -n todo-app <pod-name>`
- Verify secrets are properly configured

### Health Checks Failing
- Verify environment variables are set correctly
- Check that services can communicate with each other
- Ensure database connectivity

### Scaling Issues
- Verify metrics server is running: `kubectl top nodes`
- Check HPA configuration: `kubectl describe hpa -n todo-app <hpa-name>`

### Service Connectivity
- Check Service configuration: `kubectl describe service -n todo-app <service-name>`
- Verify network policies aren't blocking traffic

## Rolling Updates

To update the application:

```bash
# Update images
helm upgrade --install backend ./charts/backend \
    --namespace todo-app \
    --set image.repository=todo-backend \
    --set image.tag=<new-tag>

# Or update configuration without changing images
helm upgrade --install frontend ./charts/frontend \
    --namespace todo-app \
    --set config.NEW_VAR=value
```

## Cleanup

To remove the deployment:

```bash
# Uninstall Helm releases
helm uninstall backend frontend -n todo-app

# Remove namespace (optional)
kubectl delete namespace todo-app
```

## AI Tool Integration

The deployment is designed to work with AI-assisted DevOps tools:

- **Gordon**: For container image building and optimization
- **kubectl-ai**: For deployment, scaling, and troubleshooting
- **Kagent**: For monitoring and resource optimization

Example AI commands:
```bash
# Deploy using kubectl-ai
kubectl-ai "install backend helm chart with 2 replicas and health checks"

# Scale using kubectl-ai
kubectl-ai "scale backend deployment to 5 replicas"

# Monitor with Kagent
kagent "analyze cluster resource usage and optimization opportunities"
```

## Success Criteria

The deployment is successful when:

- [ ] All pods are running and healthy
- [ ] Services are accessible
- [ ] Health checks are passing
- [ ] Auto-scaling is configured
- [ ] External database connectivity is established
- [ ] AI chatbot functionality is working
- [ ] All Phase III functionality is preserved