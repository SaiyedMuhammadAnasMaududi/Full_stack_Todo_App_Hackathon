# Manual Deployment Script for AI Todo Chatbot

Write-Host "🚀 Starting Manual Deployment of AI Todo Chatbot..." -ForegroundColor Green

# Set Docker environment to minikube
Write-Host "🐳 Setting Docker environment..." -ForegroundColor Yellow
minikube docker-env | Invoke-Expression

# Build the images
Write-Host "🏗️ Building backend image..." -ForegroundColor Yellow
Set-Location backend
docker build -t todo-backend:latest .
Set-Location ..

Write-Host "🏗️ Building frontend image..." -ForegroundColor Yellow
Set-Location frontend
docker build -t todo-frontend:latest .
Set-Location ..

# Create temporary files for the deployments
Write-Host "📄 Creating deployment files..." -ForegroundColor Yellow

# Backend deployment file
@"
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
        imagePullPolicy: Never
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
"@ | Out-File -FilePath backend-deployment.yaml -Encoding UTF8

# Frontend deployment file
@"
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
        imagePullPolicy: Never
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
"@ | Out-File -FilePath frontend-deployment.yaml -Encoding UTF8

# Apply the deployments
Write-Host "🔄 Applying deployments..." -ForegroundColor Yellow
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml

# Clean up deployment files
Remove-Item backend-deployment.yaml
Remove-Item frontend-deployment.yaml

Write-Host ""
Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To access the application:" -ForegroundColor Yellow
Write-Host "1. Run 'minikube tunnel' in another terminal" -ForegroundColor White
Write-Host "2. Access the frontend via the LoadBalancer IP shown by: kubectl get services -n todo-app" -ForegroundColor White