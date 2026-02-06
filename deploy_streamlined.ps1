# Streamlined Deployment Script for AI Todo Chatbot to Minikube

Write-Host "🚀 Starting Streamlined AI Todo Chatbot Deployment to Minikube..." -ForegroundColor Green
Write-Host ""

# Verify prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

$prerequisites = @("minikube", "kubectl", "docker")
foreach ($tool in $prerequisites) {
    try {
        Get-Command $tool -ErrorAction Stop | Out-Null
        Write-Host "✅ $tool is installed" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ $tool is not installed or not in PATH" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All prerequisites verified" -ForegroundColor Green
Write-Host ""

# Try to start minikube
Write-Host "🐳 Starting Minikube cluster..." -ForegroundColor Yellow
try {
    minikube start --driver=docker --memory=2048 --cpus=2 --disk-size=8g --quiet
    Start-Sleep -Seconds 10
    Write-Host "✅ Minikube started successfully" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ Minikube start may have taken longer - checking status..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}

# Verify kubectl can connect
Write-Host "🔗 Verifying kubectl connection..." -ForegroundColor Yellow
try {
    kubectl cluster-info | Out-Null
    kubectl config use-context minikube | Out-Null
    Write-Host "✅ Connected to Minikube cluster" -ForegroundColor Green
}
catch {
    Write-Host "❌ Could not connect to Minikube cluster. Please ensure it's running." -ForegroundColor Red
    exit 1
}

# Set Docker environment to Minikube
Write-Host "🐳 Setting Docker environment to Minikube..." -ForegroundColor Yellow
minikube docker-env | Invoke-Expression
Write-Host "✅ Docker environment set to Minikube" -ForegroundColor Green

# Build the existing Dockerfiles
Write-Host "🏗️ Building backend Docker image from existing Dockerfile..." -ForegroundColor Yellow
Set-Location backend
try {
    docker build -t todo-backend:latest .
    Write-Host "✅ Backend image built successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error building backend image: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Set-Location ..

Write-Host "🏗️ Building frontend Docker image from existing Dockerfile..." -ForegroundColor Yellow
Set-Location frontend
try {
    docker build -t todo-frontend:latest .
    Write-Host "✅ Frontend image built successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error building frontend image: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
Set-Location ..

Write-Host "✅ All Docker images built successfully" -ForegroundColor Green
Write-Host ""

# Create the namespace
Write-Host "_namespace/todo-app --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✅ Namespace created" -ForegroundColor Green

# Create secrets (using placeholder values for now)
Write-Host "🔐 Creating secrets..." -ForegroundColor Yellow
$secretsYaml = @"
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
  namespace: todo-app
type: Opaque
data:
  database_url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc3dvcmRAaG9zdC5kb2NrZXIuaW50ZXJuYWw6NTQzMi90b2Rv
  cohere_api_key: Y29oZXJlLWtleS1wbGFjZWhvbGRlcg==
  better_auth_secret: eW91ci1zZWNyZXQtcGxhY2Vob2xkZXI=
"@

$secretsYaml | Out-File -FilePath temp-secrets.yaml -Encoding UTF8
kubectl apply -f temp-secrets.yaml
Remove-Item temp-secrets.yaml
Write-Host "✅ Secrets created" -ForegroundColor Green

# Create ConfigMaps
Write-Host "⚙️ Creating ConfigMaps..." -ForegroundColor Yellow
kubectl create configmap backend-config --namespace todo-app --from-literal=BACKEND_PORT=8000 --dry-run=client -o yaml | kubectl apply -f -
kubectl create configmap frontend-config --namespace todo-app --from-literal=PORT=3000 --dry-run=client -o yaml | kubectl apply -f -
Write-Host "✅ ConfigMaps created" -ForegroundColor Green

# Create deployments using the existing Docker images
Write-Host "🔄 Creating deployments..." -ForegroundColor Yellow

# Backend deployment
$backendYaml = @"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
spec:
  replicas: 1
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
        imagePullPolicy: Never  # Use local image
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
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
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
"@

$backendYaml | Out-File -FilePath backend-deployment.yaml -Encoding UTF8
kubectl apply -f backend-deployment.yaml
Remove-Item backend-deployment.yaml

# Frontend deployment
$frontendYaml = @"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
spec:
  replicas: 1
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
        imagePullPolicy: Never  # Use local image
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
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
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
"@

$frontendYaml | Out-File -FilePath frontend-deployment.yaml -Encoding UTF8
kubectl apply -f frontend-deployment.yaml
Remove-Item frontend-deployment.yaml

Write-Host "✅ Deployments created" -ForegroundColor Green
Write-Host ""

# Wait for deployments to be ready
Write-Host "⏳ Waiting for deployments to be ready..." -ForegroundColor Yellow

Write-Host "Waiting for backend deployment..." -ForegroundColor Cyan
$timeout = 300  # 5 minutes
$elapsed = 0
while ($elapsed -lt $timeout) {
    try {
        $readyReplicas = kubectl get deployment backend -n todo-app -o jsonpath='{.status.readyReplicas}' 2>$null
        if ($readyReplicas -eq "1") {
            Write-Host "✅ Backend deployment is ready" -ForegroundColor Green
            break
        }
    }
    catch {}

    Start-Sleep -Seconds 10
    $elapsed += 10

    if ($elapsed -ge $timeout) {
        Write-Host "⚠️ Timeout waiting for backend deployment" -ForegroundColor Yellow
    }
}

Write-Host "Waiting for frontend deployment..." -ForegroundColor Cyan
$elapsed = 0
while ($elapsed -lt $timeout) {
    try {
        $readyReplicas = kubectl get deployment frontend -n todo-app -o jsonpath='{.status.readyReplicas}' 2>$null
        if ($readyReplicas -eq "1") {
            Write-Host "✅ Frontend deployment is ready" -ForegroundColor Green
            break
        }
    }
    catch {}

    Start-Sleep -Seconds 10
    $elapsed += 10

    if ($elapsed -ge $timeout) {
        Write-Host "⚠️ Timeout waiting for frontend deployment" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "📋 Final Status:" -ForegroundColor Green
kubectl get pods -n todo-app
Write-Host ""
kubectl get services -n todo-app
Write-Host ""
kubectl get deployments -n todo-app

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host "💡 To access the application:" -ForegroundColor Yellow
Write-Host "   1. Run 'minikube tunnel' in another terminal to expose LoadBalancer services" -ForegroundColor White
Write-Host "   2. Check the external IP with: kubectl get services -n todo-app" -ForegroundColor White
Write-Host ""
Write-Host "The AI Todo Chatbot is now deployed to Minikube!" -ForegroundColor Green