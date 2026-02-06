#!/bin/bash

# Validate Full Stack Todo App Deployment
# This script validates that the deployed application is working correctly

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -n NAMESPACE        Kubernetes namespace (default: todo-app)"
    echo "  -h                  Show this help message"
    exit 1
}

# Default values
NAMESPACE="todo-app"

# Parse command line options
while getopts "n:h" opt; do
    case $opt in
        n) NAMESPACE="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

echo "🔍 Validating Full Stack Todo App Deployment in namespace $NAMESPACE..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

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

# Check if all deployments are ready
DEPLOYMENTS_READY=$(kubectl get deployments -n $NAMESPACE --no-headers | awk '$2==$1 {print $1}' | wc -l)
TOTAL_DEPLOYMENTS=$(kubectl get deployments -n $NAMESPACE --no-headers | wc -l)

if [ $DEPLOYMENTS_READY -eq $TOTAL_DEPLOYMENTS ]; then
    echo "✅ All deployments are ready ($DEPLOYMENTS_READY/$TOTAL_DEPLOYMENTS)"
else
    echo "⚠️  Some deployments are not ready ($DEPLOYMENTS_READY/$TOTAL_DEPLOYMENTS)"
fi

echo ""
echo "🎉 Full Stack Todo App deployment validation completed successfully!"

# Additional health check if possible
echo ""
echo "🧪 Performing additional health checks..."

# Get pod names
BACKEND_PODS=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=backend -o jsonpath='{.items[*].metadata.name}' 2>/dev/null)
FRONTEND_PODS=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/name=frontend -o jsonpath='{.items[*].metadata.name}' 2>/dev/null)

if [ ! -z "$BACKEND_PODS" ]; then
    echo "Testing backend health endpoint..."
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