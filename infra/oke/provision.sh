#!/bin/bash
set -e

echo "=== Oracle OKE Cluster Provisioning ==="

# Prerequisites: OCI CLI configured with proper tenancy/compartment

COMPARTMENT_ID="${OCI_COMPARTMENT_ID}"
CLUSTER_NAME="todo-app-oke"
K8S_VERSION="v1.28.2"
NODE_SHAPE="VM.Standard.E4.Flex"
NODE_COUNT=3

if [ -z "$COMPARTMENT_ID" ]; then
  echo "ERROR: Set OCI_COMPARTMENT_ID environment variable"
  exit 1
fi

# 1. Create VCN
echo "[1/5] Creating VCN..."
VCN_ID=$(oci network vcn create \
  --compartment-id "$COMPARTMENT_ID" \
  --display-name "todo-vcn" \
  --cidr-blocks '["10.0.0.0/16"]' \
  --query 'data.id' --raw-output)

# 2. Create subnets
echo "[2/5] Creating subnets..."
SUBNET_ID=$(oci network subnet create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "todo-node-subnet" \
  --cidr-block "10.0.10.0/24" \
  --query 'data.id' --raw-output)

LB_SUBNET_ID=$(oci network subnet create \
  --compartment-id "$COMPARTMENT_ID" \
  --vcn-id "$VCN_ID" \
  --display-name "todo-lb-subnet" \
  --cidr-block "10.0.20.0/24" \
  --query 'data.id' --raw-output)

# 3. Create OKE cluster
echo "[3/5] Creating OKE cluster..."
CLUSTER_ID=$(oci ce cluster create \
  --compartment-id "$COMPARTMENT_ID" \
  --name "$CLUSTER_NAME" \
  --kubernetes-version "$K8S_VERSION" \
  --vcn-id "$VCN_ID" \
  --service-lb-subnet-ids "[\"$LB_SUBNET_ID\"]" \
  --query 'data.id' --raw-output)

echo "Waiting for cluster to be ACTIVE..."
oci ce cluster get --cluster-id "$CLUSTER_ID" --query 'data."lifecycle-state"' --raw-output
# Poll until active (simplified)
sleep 300

# 4. Create node pool
echo "[4/5] Creating node pool..."
oci ce node-pool create \
  --compartment-id "$COMPARTMENT_ID" \
  --cluster-id "$CLUSTER_ID" \
  --name "todo-node-pool" \
  --kubernetes-version "$K8S_VERSION" \
  --node-shape "$NODE_SHAPE" \
  --node-shape-config '{"ocpus": 2, "memoryInGBs": 16}' \
  --size "$NODE_COUNT" \
  --placement-configs "[{\"availabilityDomain\": \"$(oci iam availability-domain list --compartment-id $COMPARTMENT_ID --query 'data[0].name' --raw-output)\", \"subnetId\": \"$SUBNET_ID\"}]"

# 5. Get kubeconfig
echo "[5/5] Downloading kubeconfig..."
oci ce cluster create-kubeconfig \
  --cluster-id "$CLUSTER_ID" \
  --file ~/.kube/config-oke \
  --region "$OCI_REGION" \
  --token-version 2.0.0

export KUBECONFIG=~/.kube/config-oke

echo ""
echo "=== OKE Cluster Ready ==="
echo "Cluster ID: $CLUSTER_ID"
echo "Run: export KUBECONFIG=~/.kube/config-oke"
echo "Then: kubectl get nodes"
