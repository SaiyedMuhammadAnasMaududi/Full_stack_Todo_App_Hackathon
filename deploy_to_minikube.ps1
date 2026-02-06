# PowerShell Script for AI Todo Chatbot Deployment to Minikube
# This script will deploy the full-stack application to Minikube

Write-Host "🚀 Starting AI Todo Chatbot Deployment to Minikube..." -ForegroundColor Green
Write-Host ""

# Check if required tools are installed

Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

$prerequisites = @("minikube", "kubectl", "helm", "docker")

foreach ($tool in $prerequisites) {
    try {
        Get-Command $tool -ErrorAction Stop | Out-Null
        Write-Host "✅ $tool is installed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ $tool is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install it via Chocolatey: choco install $tool" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All prerequisites verified" -ForegroundColor Green
Write-Host ""

# Start Minikube if not already running
Write-Host "📍 Checking Minikube status..." -ForegroundColor Yellow
try {
    minikube status --format='{{.APIServer.Status}}' 2>$null | Out-Null
    Write-Host "✅ Minikube is already running" -ForegroundColor Green
}
catch {
    Write-Host "🔄 Starting Minikube cluster..." -ForegroundColor Cyan
    minikube start --memory=4096 --cpus=2 --disk-size=20g
}

# Enable ingress addon
Write-Host "🔌 Enabling Minikube addons..." -ForegroundColor Yellow
minikube addons enable ingress
minikube addons enable metrics-server

Write-Host "✅ Minikube addons enabled" -ForegroundColor Green
Write-Host ""

# Verify cluster connectivity
Write-Host "📡 Verifying cluster connectivity..." -ForegroundColor Yellow
kubectl cluster-info
Write-Host ""

# Create namespace
Write-Host "🏗️ Creating namespace..." -ForegroundColor Yellow
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✅ Namespace created" -ForegroundColor Green
Write-Host ""

# Build Docker images
Write-Host "🐳 Setting Docker environment to Minikube..." -ForegroundColor Yellow
minikube docker-env | Invoke-Expression

Write-Host "Building Docker images..." -ForegroundColor Yellow

Write-Host "Building backend image..." -ForegroundColor Cyan
Set-Location backend
docker build -t todo-backend:latest .
Set-Location ..

Write-Host "Building frontend image..." -ForegroundColor Cyan
Set-Location frontend
docker build -t todo-frontend:latest .
Set-Location ..

Write-Host "✅ Docker images built" -ForegroundColor Green
Write-Host ""

# Create Kubernetes secrets
Write-Host "🔐 Creating secrets..." -ForegroundColor Yellow

# Create temporary secrets file
@"
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
  namespace: todo-app
type: Opaque
data:
  database_url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc3dvcmRAcG9zdGdyZXM6NTQzMi90b2RvX2Ri
  cohere_api_key: eW91ci1jb2hlcmUtYXBpLWtleQ==
  better_auth_secret: eW91ci1qd3Qtc2VjcmV0
"@ | Out-File -FilePath temp-secrets.yaml -Encoding utf8

kubectl apply -f temp-secrets.yaml
Remove-Item temp-secrets.yaml

Write-Host "✅ Secrets created" -ForegroundColor Green
Write-Host ""

# Create ConfigMaps
Write-Host "⚙️ Creating ConfigMaps..." -ForegroundColor Yellow

kubectl create configmap todo-backend-config `
  --namespace todo-app `
  --from-literal=LOG_LEVEL=INFO `
  --from-literal=DEBUG=False `
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create configmap todo-frontend-config `
  --namespace todo-app `
  --from-literal=PORT=3000 `
  --from-literal=NODE_ENV=production `
  --dry-run=client -o yaml | kubectl apply -f -

Write-Host "✅ ConfigMaps created" -ForegroundColor Green
Write-Host ""

# Deploy Backend First
Write-Host "📦 Deploying Backend Service..." -ForegroundColor Yellow

# Create backend deployment YAML
@"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: database_url
        - name: COHERE_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: cohere_api_key
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: better_auth_secret
        - name: BACKEND_PORT
          value: "8000"
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: todo-backend-config
              key: LOG_LEVEL
        - name: DEBUG
          valueFrom:
            configMapKeyRef:
              name: todo-backend-config
              key: DEBUG
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: todo-app
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"@ | Out-File -FilePath backend-deployment.yaml -Encoding utf8

kubectl apply -f backend-deployment.yaml
Remove-Item backend-deployment.yaml

Write-Host "✅ Backend deployed" -ForegroundColor Green
Write-Host ""

# Deploy Frontend
Write-Host "📱 Deploying Frontend Service..." -ForegroundColor Yellow

# Create frontend deployment YAML
@"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_BACKEND_URL
          value: "http://backend.todo-app.svc.cluster.local"
        - name: NEXT_PUBLIC_COHERE_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: cohere_api_key
        - name: NEXT_PUBLIC_BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-app-secrets
              key: better_auth_secret
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: todo-frontend-config
              key: PORT
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: todo-frontend-config
              key: NODE_ENV
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "300m"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: todo-app
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"@ | Out-File -FilePath frontend-deployment.yaml -Encoding utf8

kubectl apply -f frontend-deployment.yaml
Remove-Item frontend-deployment.yaml

Write-Host "✅ Frontend deployed" -ForegroundColor Green
Write-Host ""

# Wait for deployments to be ready
Write-Host "⏳ Waiting for deployments to be ready..." -ForegroundColor Yellow

Write-Host "Waiting for backend deployment..." -ForegroundColor Cyan
kubectl rollout status deployment/backend -n todo-app --timeout=300s

Write-Host "Waiting for frontend deployment..." -ForegroundColor Cyan
kubectl rollout status deployment/frontend -n todo-app --timeout=300s

Write-Host "✅ Deployments are ready" -ForegroundColor Green
Write-Host ""

# Verify deployment
Write-Host "🔍 Verifying deployment..." -ForegroundColor Yellow

Write-Host "Checking pods..." -ForegroundColor Cyan
kubectl get pods -n todo-app

Write-Host ""
Write-Host "Checking services..." -ForegroundColor Cyan
kubectl get services -n todo-app

Write-Host ""
Write-Host "Checking deployments..." -ForegroundColor Cyan
kubectl get deployments -n todo-app

Write-Host ""
Write-Host "Checking HPAs..." -ForegroundColor Cyan
kubectl get hpa -n todo-app

Write-Host ""
Write-Host "Checking ConfigMaps and Secrets..." -ForegroundColor Cyan
kubectl get configmaps -n todo-app
kubectl get secrets -n todo-app

Write-Host ""
Write-Host "✅ Deployment verification complete" -ForegroundColor Green
Write-Host ""

# Get service URLs
Write-Host "🌐 Access Information:" -ForegroundColor Green
Write-Host ""
try {
    $frontendUrl = minikube service frontend -n todo-app --url 2>$null
    Write-Host "Frontend URL: $frontendUrl" -ForegroundColor Cyan
}
catch {
    Write-Host "Frontend URL: Not available yet, check with: minikube service frontend -n todo-app --url" -ForegroundColor Yellow
}

try {
    $backendUrl = minikube service backend -n todo-app --url 2>$null
    Write-Host "Backend URL: $backendUrl" -ForegroundColor Cyan
}
catch {
    Write-Host "Backend URL: Not available yet, check with: minikube service backend -n todo-app --url" -ForegroundColor Yellow
}

Write-Host ""

Write-Host "📋 Deployment Summary:" -ForegroundColor Green
Write-Host "- Namespace: todo-app"
Write-Host "- Backend: deployment/backend with 2 replicas (ClusterIP service)"
Write-Host "- Frontend: deployment/frontend with 2 replicas (LoadBalancer service)"
Write-Host "- Services: backend (internal), frontend (external access via Minikube)"
Write-Host "- Auto-scaling: Enabled for both deployments"
Write-Host "- Health checks: Configured for both services"
Write-Host ""

Write-Host "💡 To access the application:" -ForegroundColor Yellow
Write-Host "  1. Visit the Frontend URL above"
Write-Host "  2. Or run: minikube tunnel (in another terminal) and use the LoadBalancer IP"
Write-Host ""

Write-Host "🔧 Useful commands for management:" -ForegroundColor Yellow
Write-Host "  View logs: kubectl logs -n todo-app deployment/backend"
Write-Host "  Scale manually: kubectl scale -n todo-app deployment/backend --replicas=3"
Write-Host "  Check HPA: kubectl get hpa -n todo-app"
Write-Host "  Uninstall: kubectl delete namespace todo-app"

Write-Host ""
Write-Host "🎉 AI Todo Chatbot is now running on Minikube!" -ForegroundColor Green
Write-Host "The full-stack application with AI chatbot functionality is deployed and accessible."