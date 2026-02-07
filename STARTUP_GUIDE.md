# Todo App - Complete Startup Guide (From Shutdown)

Run these commands in order after opening your laptop / restarting WSL.

---

## Step 1: Start Docker Desktop

Open **Docker Desktop** from Windows Start Menu and wait until it shows "Docker is running".

If using WSL without Docker Desktop, start the daemon:
```bash
sudo service docker start
```

Verify:
```bash
docker info > /dev/null 2>&1 && echo "Docker OK" || echo "Docker NOT running"
```

---

## Step 2: Start Minikube

```bash
minikube start --driver=docker --cpus=2 --memory=2048
```

Verify:
```bash
minikube status
```

Expected output — all three should say `Running` / `Configured`:
```
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

---

## Step 3: Verify All Pods Are Running

```bash
kubectl get pods -n todo-app
kubectl get pods -n dapr-system
```

All pods should show `Running`. If any pod is stuck in `CrashLoopBackOff` or `Error`:
```bash
kubectl logs -n todo-app <pod-name>
kubectl describe pod -n todo-app <pod-name>
```

To restart a stuck deployment:
```bash
kubectl rollout restart deployment/<name> -n todo-app
```

---

## Step 4: Start Port Forwarding

Open **two separate terminals** (or use `&` to background):

**Terminal 1 — Backend (port 8080):**
```bash
kubectl port-forward -n todo-app svc/backend 8080:80 --address 0.0.0.0
```

**Terminal 2 — Frontend (port 3000):**
```bash
kubectl port-forward -n todo-app deployment/frontend 3000:3000 --address 0.0.0.0
```

Or run both in one terminal (backgrounded):
```bash
kubectl port-forward -n todo-app svc/backend 8080:80 --address 0.0.0.0 &
kubectl port-forward -n todo-app deployment/frontend 3000:3000 --address 0.0.0.0 &
```

---

## Step 5: Open in Browser

| Service              | URL                          |
|----------------------|------------------------------|
| Frontend (App)       | http://localhost:3000         |
| Backend Health Check | http://localhost:8080/health  |
| Backend Swagger Docs | http://localhost:8080/docs    |

---

## Quick One-Liner (Copy-Paste After Reboot)

```bash
minikube start --driver=docker --cpus=2 --memory=2048 && \
echo "Waiting for pods..." && sleep 10 && \
kubectl get pods -n todo-app && \
kubectl port-forward -n todo-app svc/backend 8080:80 --address 0.0.0.0 & \
kubectl port-forward -n todo-app deployment/frontend 3000:3000 --address 0.0.0.0 & \
echo "" && \
echo "========================================" && \
echo "  Frontend:  http://localhost:3000" && \
echo "  Backend:   http://localhost:8080/health" && \
echo "  API Docs:  http://localhost:8080/docs" && \
echo "========================================"
```

---

## Troubleshooting

### Port-forward dies / "connection refused"
```bash
# Restart the port-forwards
kubectl port-forward -n todo-app svc/backend 8080:80 --address 0.0.0.0 &
kubectl port-forward -n todo-app deployment/frontend 3000:3000 --address 0.0.0.0 &
```

### Pod stuck in ContainerCreating
```bash
kubectl describe pod -n todo-app <pod-name>
# Usually means image is being pulled — wait a minute
```

### Port 8080 already in use
```bash
# Use a different port
kubectl port-forward -n todo-app svc/backend 9090:80 --address 0.0.0.0 &
# Then access at http://localhost:9090/health
```

### Minikube won't start
```bash
minikube delete
minikube start --driver=docker --cpus=2 --memory=2048
# Then redeploy (see Redeploy section below)
```

### Check Docker images inside Minikube
```bash
eval $(minikube docker-env)
docker images | grep todo
```

---

## Redeploy (Only If Minikube Was Deleted)

If you ran `minikube delete`, you need to redeploy everything:

```bash
# 1. Start fresh Minikube
minikube start --driver=docker --cpus=2 --memory=2048

# 2. Create namespace
kubectl create namespace todo-app

# 3. Install Dapr
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
helm upgrade --install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

# 4. Build images inside Minikube's Docker
eval $(minikube docker-env)
docker build -t todo-backend:latest ./backend/
docker build -t todo-frontend:latest ./frontend/

# 5. Deploy backend
helm upgrade --install backend ./charts/backend -n todo-app \
  --set image.repository=todo-backend \
  --set image.tag=latest \
  --set image.pullPolicy=Never \
  --set replicaCount=1 \
  --set autoscaling.enabled=false \
  --set "secrets.database_url=postgresql://neondb_owner:npg_bKkhetAP28ZF@ep-wispy-brook-adk28oxi-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" \
  --set secrets.better_auth_secret=fd5dee830896cab655b4aea325843c70b709564adec9149bbf5c7e1df4b1c174 \
  --set secrets.cohere_api_key=1L1KXLfZUQ7mKhsUfXgzaKq34w65DAEXDuWxokfz \
  --set resources.requests.cpu=100m \
  --set resources.requests.memory=128Mi \
  --set resources.limits.cpu=300m \
  --set resources.limits.memory=256Mi

# 6. Deploy frontend
helm upgrade --install frontend ./charts/frontend -n todo-app \
  --set image.repository=todo-frontend \
  --set image.tag=latest \
  --set image.pullPolicy=Never \
  --set replicaCount=1 \
  --set autoscaling.enabled=false \
  --set env.NEXT_PUBLIC_BACKEND_URL=http://backend.todo-app.svc.cluster.local \
  --set secrets.next_public_better_auth_secret=fd5dee830896cab655b4aea325843c70b709564adec9149bbf5c7e1df4b1c174 \
  --set secrets.next_public_cohere_api_key=1L1KXLfZUQ7mKhsUfXgzaKq34w65DAEXDuWxokfz \
  --set resources.requests.cpu=50m \
  --set resources.requests.memory=64Mi \
  --set resources.limits.cpu=200m \
  --set resources.limits.memory=128Mi

# 7. Apply Dapr components
kubectl apply -f ./infra/dapr/ -n todo-app

# 8. Wait and verify
sleep 30
kubectl get pods -n todo-app

# 9. Port-forward
kubectl port-forward -n todo-app svc/backend 8080:80 --address 0.0.0.0 &
kubectl port-forward -n todo-app deployment/frontend 3000:3000 --address 0.0.0.0 &
```

---

## Stop Everything

```bash
# Kill port-forwards
pkill -f "port-forward"

# Stop Minikube (preserves all deployments for next startup)
minikube stop
```
