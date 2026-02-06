---
name: kubernetes-deployment
description: Create Helm charts, deploy to Minikube and AKS/GKE/OKE, configure ingress, autoscaling, probes.
license: Complete terms in LICENSE.txt
---

This skill guides the creation and deployment of Kubernetes applications using Helm charts with production-ready configurations for various cloud platforms.

The user provides requirements for deploying their application to Kubernetes: specifying the target platform (Minikube, AKS, GKE, OKE), application architecture, scaling requirements, and any special deployment needs. They may include context about networking, security, monitoring, or operational requirements.

## Helm Chart Architecture

Before creating Helm charts, consider the optimal structure for production deployments:
- **Template Organization**: Organize templates logically (deployment, service, ingress, configmap, secret, hpa, pdb)
- **Values Structure**: Create flexible values.yaml with sensible defaults and clear documentation
- **Chart Dependencies**: Manage subcharts and dependencies efficiently
- **Versioning**: Follow semantic versioning for chart releases
- **Testing**: Include tests for chart validation and functionality

## Platform-Specific Deployments

For each target platform, implement appropriate configurations:

### Minikube (Local Development)
- Resource limits appropriate for local development
- Simplified networking and ingress configuration
- Local storage classes and volume configurations
- Development-focused monitoring and logging

### AKS (Azure Kubernetes Service)
- Azure-specific integrations (Key Vault, Storage, Load Balancer)
- Azure AD authentication and RBAC configuration
- Azure Monitor and Application Insights integration
- Private cluster and network security configurations

### GKE (Google Kubernetes Engine)
- Google Cloud integrations (Secret Manager, Cloud Storage)
- Identity and IAM configuration
- Cloud Operations Suite integration
- VPC-native networking and security

### OKE (Oracle Kubernetes Engine)
- Oracle Cloud infrastructure integrations
- OCI authentication and policies
- Object Storage and Load Balancer configurations
- Network security and VCN setup

## Ingress Configuration

Implement robust ingress setups with:
- TLS certificate management (cert-manager, Let's Encrypt)
- Load balancing algorithms and sticky sessions
- Path-based and subdomain routing
- Rate limiting and security headers
- CDN integration where appropriate

## Autoscaling Setup

Configure horizontal and vertical scaling with:
- Horizontal Pod Autoscaler (HPA) based on CPU/memory/custom metrics
- Vertical Pod Autoscaler (VPA) for resource optimization
- Cluster Autoscaler for node-level scaling
- Custom metrics and Prometheus integration
- Scaling policies and cooldown periods

## Health Probes and Monitoring

Implement comprehensive health checking with:
- Liveness and readiness probes with appropriate timeouts
- Startup probes for slow-starting applications
- Custom probe endpoints for complex health checks
- Integration with service mesh health checking
- Metrics collection and alerting rules

## Security and Compliance

Follow security best practices:
- Pod Security Standards and policies
- Network policies for traffic control
- Secret management and encryption
- Resource quotas and limits
- Admission controllers and policy enforcement

## Deployment Strategies

Support various deployment patterns:
- Rolling updates with configurable max surge and unavailable
- Blue-green deployments for zero-downtime releases
- Canary deployments for gradual rollouts
- Recreate strategy for stateful applications
- Automated rollback triggers and conditions

Always ensure deployments are production-ready with proper resource requests/limits, health checks, security configurations, and monitoring integration. Verify that applications maintain the same functionality while benefiting from Kubernetes orchestration advantages.