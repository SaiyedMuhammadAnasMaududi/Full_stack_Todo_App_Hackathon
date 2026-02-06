# Final Deployment Script for AI Todo Chatbot

Write-Host "🚀 Starting Final Deployment of AI Todo Chatbot..." -ForegroundColor Green

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

# Create Kubernetes deployments manually with simple kubectl commands
Write-Host "🔄 Deploying to Kubernetes..." -ForegroundColor Yellow

# Create backend deployment
kubectl apply -f - << 'EOF'
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
EOF

# Create frontend deployment
kubectl apply -f - << 'EOF'
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
EOF

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "Run 'minikube tunnel' in another terminal to access the services" -ForegroundColor Yellow