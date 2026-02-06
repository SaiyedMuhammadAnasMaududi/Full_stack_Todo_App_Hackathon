#!/bin/bash

# Deploy Full Stack Todo Application
# This script deploys both frontend and backend services to Kubernetes

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -f FRONTEND_PATH    Path to frontend source code (default: ./frontend)"
    echo "  -b BACKEND_PATH     Path to backend source code (default: ./backend)"
    echo "  -n NAMESPACE        Kubernetes namespace (default: todo-app)"
    echo "  -r REPLICAS_FRONT   Frontend replicas (default: 2)"
    echo "  -s REPLICAS_BACK    Backend replicas (default: 2)"
    echo "  -h                  Show this help message"
    exit 1
}

# Default values
FRONTEND_PATH="./frontend"
BACKEND_PATH="./backend"
NAMESPACE="todo-app"
REPLICAS_FRONT=2
REPLICAS_BACK=2

# Parse command line options
while getopts "f:b:n:r:s:h" opt; do
    case $opt in
        f) FRONTEND_PATH="$OPTARG" ;;
        b) BACKEND_PATH="$OPTARG" ;;
        n) NAMESPACE="$OPTARG" ;;
        r) REPLICAS_FRONT="$OPTARG" ;;
        s) REPLICAS_BACK="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

echo "🚀 Starting Full Stack Todo App Deployment..."
echo "Frontend Path: $FRONTEND_PATH"
echo "Backend Path: $BACKEND_PATH"
echo "Namespace: $NAMESPACE"
echo "Frontend Replicas: $REPLICAS_FRONT"
echo "Backend Replicas: $REPLICAS_BACK"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed or not in PATH"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ docker is not installed or not in PATH"
    exit 1
fi

echo "✅ Prerequisites verified"
echo ""

# Create namespace if it doesn't exist
echo "🏗️ Creating namespace $NAMESPACE..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
echo ""

# Build Docker images
echo "🐳 Building Docker images..."

echo "Building frontend image..."
cd $FRONTEND_PATH
docker build -t todo-frontend:latest .
cd -

echo "Building backend image..."
cd $BACKEND_PATH
docker build -t todo-backend:latest .
cd -

echo "✅ Docker images built"
echo ""

# Deploy backend first (dependency)
echo "📦 Deploying backend service..."
cat > backend-values.yaml <<EOF
replicaCount: $REPLICAS_BACK
image:
  repository: todo-backend
  tag: latest
  pullPolicy: Never
service:
  type: ClusterIP
  port: 8000
ingress:
  enabled: false
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
autoscaling:
  enabled: true
  minReplicas: $REPLICAS_BACK
  maxReplicas: $(($REPLICAS_BACK * 2))
  targetCPUUtilizationPercentage: 70
EOF

helm upgrade --install backend ./charts/backend \
    --namespace $NAMESPACE \
    -f backend-values.yaml \
    --wait
echo "✅ Backend deployed"
echo ""

# Deploy frontend
echo "📱 Deploying frontend service..."
cat > frontend-values.yaml <<EOF
replicaCount: $REPLICAS_FRONT
image:
  repository: todo-frontend
  tag: latest
  pullPolicy: Never
service:
  type: ClusterIP
  port: 80
ingress:
  enabled: false
resources:
  limits:
    cpu: 300m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
autoscaling:
  enabled: true
  minReplicas: $REPLICAS_FRONT
  maxReplicas: $(($REPLICAS_FRONT * 2))
  targetCPUUtilizationPercentage: 70
env:
  NEXT_PUBLIC_BACKEND_URL: http://backend.$NAMESPACE.svc.cluster.local:8000
EOF

helm upgrade --install frontend ./charts/frontend \
    --namespace $NAMESPACE \
    -f frontend-values.yaml \
    --wait
echo "✅ Frontend deployed"
echo ""

# Verify deployment
echo "🔍 Verifying deployment..."

echo "Checking pods..."
kubectl get pods -n $NAMESPACE

echo "Checking services..."
kubectl get services -n $NAMESPACE

echo "Checking deployments..."
kubectl get deployments -n $NAMESPACE

echo "Checking HPAs..."
kubectl get hpa -n $NAMESPACE

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl rollout status deployment/backend -n $NAMESPACE --timeout=300s
kubectl rollout status deployment/frontend -n $NAMESPACE --timeout=300s

echo ""
echo "✅ Full stack deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "- Namespace: $NAMESPACE"
echo "- Backend: deployment/backend with $REPLICAS_BACK replicas"
echo "- Frontend: deployment/frontend with $REPLICAS_FRONT replicas"
echo "- Services: backend (ClusterIP), frontend (ClusterIP)"
echo "- Auto-scaling: Enabled for both deployments"
echo ""

echo "🎉 Todo application is now running on Kubernetes!"