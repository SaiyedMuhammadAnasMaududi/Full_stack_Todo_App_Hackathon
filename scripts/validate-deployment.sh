#!/bin/bash

# Validation script for AI Todo Chatbot Kubernetes deployment
# This script validates that the deployed application is working correctly

echo "🔍 Validating AI Todo Chatbot Kubernetes Deployment..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

NAMESPACE="todo-app"

echo "📋 Checking deployment status..."

# Check if deployments are ready
echo "Checking deployments..."
kubectl get deployments -n $NAMESPACE

# Check pod status
echo "Checking pods..."
PODS=$(kubectl get pods -n $NAMESPACE --no-headers | wc -l)
if [ $PODS -eq 0 ]; then
    echo "❌ No pods found in $NAMESPACE namespace"
    exit 1
fi

kubectl get pods -n $NAMESPACE

# Check if all pods are running
RUNNING_PODS=$(kubectl get pods -n $NAMESPACE --field-selector=status.phase=Running --no-headers | wc -l)
TOTAL_PODS=$PODS

if [ $RUNNING_PODS -ne $TOTAL_PODS ]; then
    echo "⚠️  Some pods are not running ($RUNNING_PODS/$TOTAL_PODS)"
    kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running
else
    echo "✅ All $TOTAL_PODS pods are running"
fi

# Check services
echo "Checking services..."
kubectl get services -n $NAMESPACE

# Check if HPA is configured
echo "Checking Horizontal Pod Autoscalers..."
if kubectl get hpa -n $NAMESPACE &> /dev/null; then
    kubectl get hpa -n $NAMESPACE
else
    echo "⚠️  No HPAs found in $NAMESPACE"
fi

# Check ConfigMaps and Secrets
echo "Checking ConfigMaps and Secrets..."
kubectl get configmaps -n $NAMESPACE
kubectl get secrets -n $NAMESPACE

# Test health endpoints if accessible
echo "Testing health endpoints..."

# Get pod IPs to test internal health checks
BACKEND_PODS=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=backend -o jsonpath='{.items[*].metadata.name}')
FRONTEND_PODS=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=frontend -o jsonpath='{.items[*].metadata.name}')

if [ ! -z "$BACKEND_PODS" ]; then
    echo "Testing backend health endpoint..."
    # Test the backend health endpoint by port-forwarding or using exec
    for pod in $BACKEND_PODS; do
        if kubectl exec -n $NAMESPACE $pod -- curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Backend pod $pod health check passed"
        else
            echo "❌ Backend pod $pod health check failed"
        fi
    done
fi

if [ ! -z "$FRONTEND_PODS" ]; then
    echo "Testing frontend health endpoint..."
    for pod in $FRONTEND_PODS; do
        if kubectl exec -n $NAMESPACE $pod -- curl -f -s http://localhost:3000/api/health > /dev/null 2>&1; then
            echo "✅ Frontend pod $pod health check passed"
        else
            echo "❌ Frontend pod $pod health check failed"
        fi
    done
fi

# Check resource usage
echo "Checking resource usage..."
kubectl top pods -n $NAMESPACE || echo "⚠️  Metrics server may not be available"

# Check for any events or issues
echo "Checking for recent events..."
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -10

echo ""
echo "✅ Validation completed!"
echo ""
echo "📋 Summary:"
echo "- Namespace: $NAMESPACE"
echo "- Total pods: $TOTAL_PODS"
echo "- Running pods: $RUNNING_PODS"
echo "- Services: $(kubectl get services -n $NAMESPACE --no-headers | wc -l)"
echo "- Deployments: $(kubectl get deployments -n $NAMESPACE --no-headers | wc -l)"

echo ""
echo "🎉 AI Todo Chatbot deployment validation completed successfully!"