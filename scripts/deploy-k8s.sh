#!/bin/bash

# Deployment script for AI Todo Chatbot on Kubernetes
# This script deploys the containerized AI Todo Chatbot to a Kubernetes cluster

set -e  # Exit on any error

echo "🚀 Starting AI Todo Chatbot Kubernetes Deployment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check if helm is available
if ! command -v helm &> /dev/null; then
    echo "❌ helm is not installed or not in PATH"
    exit 1
fi

# Check if minikube is available (for local deployment)
if command -v minikube &> /dev/null; then
    echo "✅ Minikube detected, checking status..."
    if minikube status &> /dev/null; then
        echo "✅ Minikube is running"
    else
        echo "💡 Starting Minikube cluster..."
        minikube start --memory=4096 --cpus=2
        minikube addons enable ingress
    fi
else
    echo "⚠️  Minikube not found, assuming external Kubernetes cluster"
fi

echo "📊 Checking current Kubernetes context..."
kubectl cluster-info

echo "📦 Building container images..."

# Build backend image (using Docker if available)
if command -v docker &> /dev/null; then
    echo "🐳 Building backend container image..."
    cd backend
    docker build -t todo-backend:latest .
    cd ..

    echo "🐳 Building frontend container image..."
    cd frontend
    docker build -t todo-frontend:latest .
    cd ..
else
    echo "⚠️  Docker not found, skipping image build"
fi

echo "🔍 Validating Helm charts..."

# Validate Helm charts
if helm lint charts/backend; then
    echo "✅ Backend Helm chart validation passed"
else
    echo "❌ Backend Helm chart validation failed"
    exit 1
fi

if helm lint charts/frontend; then
    echo "✅ Frontend Helm chart validation passed"
else
    echo "❌ Frontend Helm chart validation failed"
    exit 1
fi

echo "🚢 Installing Helm charts..."

# Create namespace if it doesn't exist
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Install backend first (to ensure services are available)
echo " installing backend..."
helm upgrade --install backend charts/backend \
    --namespace todo-app \
    --set image.repository=todo-backend \
    --set image.tag=latest \
    --set image.pullPolicy=Never \
    --set autoscaling.enabled=false \
    --wait

# Install frontend (with reference to backend service)
echo " installing frontend..."
helm upgrade --install frontend charts/frontend \
    --namespace todo-app \
    --set image.repository=todo-frontend \
    --set image.tag=latest \
    --set image.pullPolicy=Never \
    --set autoscaling.enabled=false \
    --set env.NEXT_PUBLIC_BACKEND_URL=http://backend.todo-app.svc.cluster.local \
    --wait

echo "🔄 Enabling Horizontal Pod Autoscaling..."

# Update to enable HPA
helm upgrade --install backend charts/backend \
    --namespace todo-app \
    --set image.repository=todo-backend \
    --set image.tag=latest \
    --set image.pullPolicy=Never \
    --set autoscaling.enabled=true \
    --wait

helm upgrade --install frontend charts/frontend \
    --namespace todo-app \
    --set image.repository=todo-frontend \
    --set image.tag=latest \
    --set image.pullPolicy=Never \
    --set autoscaling.enabled=true \
    --set env.NEXT_PUBLIC_BACKEND_URL=http://backend.todo-app.svc.cluster.local \
    --wait

echo "🔍 Verifying deployment..."

# Check if pods are running
echo "Checking pods..."
kubectl get pods -n todo-app

# Check services
echo "Checking services..."
kubectl get services -n todo-app

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl rollout status deployment/backend -n todo-app --timeout=300s
kubectl rollout status deployment/frontend -n todo-app --timeout=300s

echo "✅ Deployment completed successfully!"

echo ""
echo "📋 Deployment Summary:"
echo "- Namespace: todo-app"
echo "- Backend: deployment/backend with HPA enabled"
echo "- Frontend: deployment/frontend with HPA enabled"
echo "- Services: backend, frontend"
echo ""

if command -v minikube &> /dev/null; then
    echo "🌐 To access the application locally:"
    echo "  Frontend: $(minikube service frontend -n todo-app --url)"
    echo "  Backend: $(minikube service backend -n todo-app --url)"
fi

echo ""
echo "🔧 Useful commands for management:"
echo "  View logs: kubectl logs -n todo-app deployment/backend"
echo "  Scale manually: kubectl scale -n todo-app deployment/backend --replicas=3"
echo "  Check HPA: kubectl get hpa -n todo-app"
echo "  Uninstall: helm uninstall backend frontend -n todo-app"

echo ""
echo "🎉 AI Todo Chatbot is now running on Kubernetes!"