# Quickstart: Phase V Local Development

## Prerequisites
- Docker Desktop
- Minikube (`minikube start --cpus=4 --memory=8192`)
- Dapr CLI (`dapr init -k`)
- Helm 3
- kubectl

## Steps

1. **Start Minikube**
   ```bash
   minikube start --cpus=4 --memory=8192 --driver=docker
   ```

2. **Install Dapr**
   ```bash
   dapr init -k --wait
   ```

3. **Deploy Kafka (Strimzi)**
   ```bash
   kubectl create namespace kafka
   kubectl apply -f infra/kafka/strimzi-operator.yaml -n kafka
   kubectl apply -f infra/kafka/kafka-cluster.yaml -n kafka
   ```

4. **Create App Namespace & Secrets**
   ```bash
   kubectl create namespace todo-app
   kubectl create secret generic db-secret -n todo-app --from-literal=DATABASE_URL=$DATABASE_URL
   kubectl create secret generic app-secrets -n todo-app --from-literal=BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET --from-literal=COHERE_API_KEY=$COHERE_API_KEY
   ```

5. **Apply Dapr Components**
   ```bash
   kubectl apply -f infra/dapr/ -n todo-app
   ```

6. **Build & Deploy**
   ```bash
   eval $(minikube docker-env)
   docker build -t todo-backend:latest ./backend
   docker build -t todo-frontend:latest ./frontend
   helm install todo-app infra/helm/todo-app -n todo-app
   ```

7. **Verify**
   ```bash
   kubectl get pods -n todo-app
   minikube service todo-frontend -n todo-app
   ```
