#!/bin/bash

# Complete Deployment Script for AI Todo Chatbot on Minikube
# This script will deploy the full-stack application using the cloud-native-todo-deployer skill components

set -e  # Exit on any error

echo "🚀 Starting AI Todo Chatbot Deployment to Minikube..."
echo ""

# Check if required tools are installed
echo "🔍 Checking prerequisites..."

if ! command -v minikube &> /dev/null; then
    echo "❌ minikube is not installed or not in PATH"
    echo "Please install it via Chocolatey: choco install minikube"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    echo "Please install it via Chocolatey: choco install kubernetes-cli"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed or not in PATH"
    echo "Please install it via Chocolatey: choco install kubernetes-helm"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ docker is not installed or not in PATH"
    echo "Please install Docker Desktop or ensure Docker service is running"
    exit 1
fi

echo "✅ All prerequisites verified"
echo ""

# Start Minikube if not already running
echo "📍 Checking Minikube status..."
if ! minikube status &> /dev/null; then
    echo "🔄 Starting Minikube cluster..."
    minikube start --memory=4096 --cpus=2 --disk-size=20g
else
    echo "✅ Minikube is already running"
fi

# Enable ingress addon
echo "🔌 Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

echo "✅ Minikube addons enabled"
echo ""

# Verify cluster connectivity
echo "📡 Verifying cluster connectivity..."
kubectl cluster-info
echo ""

# Create namespace
echo "🏗️ Creating namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
echo "✅ Namespace created"
echo ""

# Build Docker images
echo "🐳 Building Docker images..."

# Set Docker environment to Minikube
eval $(minikube docker-env)

echo "Building backend image..."
cd backend
docker build -t todo-backend:latest .
cd ..

echo "Building frontend image..."
cd frontend
docker build -t todo-frontend:latest .
cd ..

echo "✅ Docker images built"
echo ""

# Create Kubernetes secrets (you'll need to replace these with your actual values)
echo "🔐 Creating secrets..."

# Create a temporary secrets file
cat > temp-secrets.yaml <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: todo-app-secrets
  namespace: todo-app
type: Opaque
data:
  database_url: $(echo "postgresql://user:password@postgres:5432/todo_db" | base64 -w 0)
  cohere_api_key: $(echo "your-cohere-api-key" | base64 -w 0)
  better_auth_secret: $(echo "your-jwt-secret" | base64 -w 0)
EOF

kubectl apply -f temp-secrets.yaml
rm temp-secrets.yaml

echo "✅ Secrets created"
echo ""

# Create ConfigMaps
echo "⚙️ Creating ConfigMaps..."

kubectl create configmap todo-backend-config \
  --namespace todo-app \
  --from-literal=LOG_LEVEL=INFO \
  --from-literal=DEBUG=False \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create configmap todo-frontend-config \
  --namespace todo-app \
  --from-literal=PORT=3000 \
  --from-literal=NODE_ENV=production \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✅ ConfigMaps created"
echo ""

# Deploy Backend First (as frontend depends on it)
echo "📦 Deploying Backend Service..."

# Create backend deployment YAML
cat > backend-deployment.yaml <<EOF
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
EOF

kubectl apply -f backend-deployment.yaml
rm backend-deployment.yaml

echo "✅ Backend deployed"
echo ""

# Deploy Frontend
echo "📱 Deploying Frontend Service..."

# Create frontend deployment YAML
cat > frontend-deployment.yaml <<EOF
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
EOF

kubectl apply -f frontend-deployment.yaml
rm frontend-deployment.yaml

echo "✅ Frontend deployed"
echo ""

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."

echo "Waiting for backend deployment..."
kubectl rollout status deployment/backend -n todo-app --timeout=300s

echo "Waiting for frontend deployment..."
kubectl rollout status deployment/frontend -n todo-app --timeout=300s

echo "✅ Deployments are ready"
echo ""

# Verify deployment
echo "🔍 Verifying deployment..."

echo "Checking pods..."
kubectl get pods -n todo-app

echo ""
echo "Checking services..."
kubectl get services -n todo-app

echo ""
echo "Checking deployments..."
kubectl get deployments -n todo-app

echo ""
echo "Checking HPAs..."
kubectl get hpa -n todo-app

echo ""
echo "Checking ConfigMaps and Secrets..."
kubectl get configmaps -n todo-app
kubectl get secrets -n todo-app

echo ""
echo "✅ Deployment verification complete"
echo ""

# Get service URLs
echo "🌐 Access Information:"
echo ""
echo "Frontend URL: $(minikube service frontend -n todo-app --url 2>/dev/null || echo "Not available yet, check with: minikube service frontend -n todo-app --url")"
echo "Backend URL: $(minikube service backend -n todo-app --url 2>/dev/null || echo "Not available yet, check with: minikube service backend -n todo-app --url")"
echo ""

echo "📋 Deployment Summary:"
echo "- Namespace: todo-app"
echo "- Backend: deployment/backend with 2 replicas (ClusterIP service)"
echo "- Frontend: deployment/frontend with 2 replicas (LoadBalancer service)"
echo "- Services: backend (internal), frontend (external access via Minikube)"
echo "- Auto-scaling: Enabled for both deployments"
echo "- Health checks: Configured for both services"
echo ""

echo "💡 To access the application:"
echo "  1. Visit the Frontend URL above"
echo "  2. Or run: minikube tunnel (in another terminal) and use the LoadBalancer IP"
echo ""

echo "🔧 Useful commands for management:"
echo "  View logs: kubectl logs -n todo-app deployment/backend"
echo "  Scale manually: kubectl scale -n todo-app deployment/backend --replicas=3"
echo "  Check HPA: kubectl get hpa -n todo-app"
echo "  Uninstall: kubectl delete namespace todo-app"

echo ""
echo "🎉 AI Todo Chatbot is now running on Minikube!"
echo "The full-stack application with AI chatbot functionality is deployed and accessible."