# Access Commands for Full-Stack Todo Application

This file contains the commands to access the deployed frontend and backend services on your Minikube cluster.

## Prerequisites

Make sure your Minikube cluster is running:
```bash
minikube status
```

## Access Commands

### 1. Access via Port Forwarding (Local Development)

#### Frontend Access:
```bash
kubectl port-forward service/todo-frontend 3000:80 -n todo-app
```
Then visit: [http://localhost:3000](http://localhost:3000)

#### Backend Access:
```bash
kubectl port-forward service/todo-backend 7860:80 -n todo-app
```
Then visit: [http://localhost:7860](http://localhost:7860) or [http://localhost:7860/health](http://localhost:7860/health) for health check

### 2. Access via Minikube Tunnel (External Access)

Start a tunnel to expose LoadBalancer services:
```bash
minikube tunnel
```

Then access the frontend using the external IP from:
```bash
kubectl get svc frontend -n todo-app
```

### 3. Verify Services are Running

Check all pods are running:
```bash
kubectl get pods -n todo-app
```

Check all services:
```bash
kubectl get svc -n todo-app
```

## Service Details

- **Frontend Service**:
  - Internal ClusterIP: 10.109.239.24:80
  - Running on port 3000 inside pods
  - 2 replicas running
  - Confirmed accessible and serving the SecureTask Manager application

- **Backend Service**:
  - Internal ClusterIP: 10.104.172.185:80
  - Running on port 7860 inside pods
  - 2 replicas running
  - Confirmed accessible with health endpoint returning: {"status":"healthy","service":"todo-backend-api"}

- **Database**: Connected to Neon PostgreSQL with SSL

## Troubleshooting

If services are not accessible:

1. Check if pods are running:
   ```bash
   kubectl get pods -n todo-app
   ```

2. Check pod logs if there are issues:
   ```bash
   kubectl logs -l app.kubernetes.io/name=backend -n todo-app
   kubectl logs -l app.kubernetes.io/name=frontend -n todo-app
   ```

3. Verify secrets are properly configured:
   ```bash
   kubectl get secrets -n todo-app
   ```

## Cleanup

To stop the application:
```bash
helm uninstall todo-backend todo-frontend -n todo-app
```

To stop port forwarding, press `Ctrl+C` in the terminal where it's running.