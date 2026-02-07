#!/bin/bash
set -e

echo "=== Phase V: Minikube + Dapr + Kafka Setup ==="

# 1. Start Minikube
echo "[1/7] Starting Minikube..."
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Install Dapr
echo "[2/7] Installing Dapr..."
dapr init -k --wait

# 3. Create namespaces
echo "[3/7] Creating namespaces..."
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# 4. Install Strimzi Kafka Operator
echo "[4/7] Installing Strimzi operator..."
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
echo "Waiting for Strimzi operator..."
kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator -n kafka --timeout=120s

# 5. Deploy Kafka cluster + topics
echo "[5/7] Deploying Kafka cluster..."
kubectl apply -f ../kafka/kafka-cluster.yaml -n kafka
echo "Waiting for Kafka cluster (this may take 2-3 minutes)..."
kubectl wait kafka/kafka-cluster --for=condition=Ready --timeout=300s -n kafka

# 6. Create secrets
echo "[6/7] Creating secrets..."
kubectl create secret generic db-secret -n todo-app \
  --from-literal=DATABASE_URL="${DATABASE_URL}" \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl create secret generic app-secrets -n todo-app \
  --from-literal=BETTER_AUTH_SECRET="${BETTER_AUTH_SECRET}" \
  --from-literal=COHERE_API_KEY="${COHERE_API_KEY}" \
  --dry-run=client -o yaml | kubectl apply -f -

# 7. Apply Dapr components
echo "[7/7] Applying Dapr components..."
kubectl apply -f ../dapr/ -n todo-app

echo ""
echo "=== Setup Complete ==="
echo "Next: Build images and deploy with Helm"
echo "  eval \$(minikube docker-env)"
echo "  docker build -t todo-backend:latest ../../backend"
echo "  docker build -t todo-frontend:latest ../../frontend"
echo "  helm install backend ../../charts/backend -n todo-app"
echo "  helm install frontend ../../charts/frontend -n todo-app"
