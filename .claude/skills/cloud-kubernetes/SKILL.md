---
name: cloud-kubernetes
description: Provision AKS/GKE/OKE clusters, configure networking, connect managed Kafka.
license: Complete terms in LICENSE.txt
---

This skill guides the provisioning and configuration of cloud-managed Kubernetes clusters across multiple providers with proper networking setup and managed Kafka integration.

The user provides requirements for cloud Kubernetes infrastructure: specifying cluster configurations, networking requirements, security needs, and integration with managed Kafka services. They may include context about the target cloud provider, compliance requirements, or specific operational needs.

## Cluster Provisioning Strategies

Before provisioning clusters, consider optimal configurations for each provider:
- **AKS (Azure Kubernetes Service)**: Configure node pools, virtual nodes, and Azure CNI networking
- **GKE (Google Kubernetes Engine)**: Set up autopilot/node pools, VPC-native networking, and workload identity
- **OKE (Oracle Kubernetes Engine)**: Configure node pools, VCN networking, and bastion access
- **Resource Sizing**: Plan appropriate VM types and resource allocation for workloads
- **High Availability**: Configure multi-zone deployments for production workloads
- **Cost Optimization**: Implement spot instances, reserved capacity, and cluster autoscaling

## Networking Configuration

Implement robust networking with:
- **VPC/VNet Setup**: Configure virtual networks with proper CIDR ranges and subnets
- **Load Balancer Integration**: Set up application and network load balancers
- **DNS Configuration**: Configure internal and external DNS resolution
- **Network Security**: Implement network policies, NSGs, and firewall rules
- **VPN/Peering**: Configure VPC peering and VPN connections for hybrid scenarios
- **Ingress Controllers**: Deploy and configure NGINX, Traefik, or cloud-native ingress controllers

## Managed Kafka Integration

Connect to managed Kafka services with:
- **AKS - Azure Event Hubs Kafka**: Configure Event Hubs with Kafka protocol support
- **GKE - Confluent Cloud/AWS MSK**: Connect to managed Kafka services via VPC peering
- **OKE - Oracle Streaming**: Integrate with Oracle Streaming service
- **Security Configuration**: Implement SSL/TLS, SASL authentication, and network security
- **Connection Management**: Configure connection pooling and failover mechanisms
- **Monitoring**: Enable Kafka metrics and integration with cloud monitoring services

## Security and Access Control

Implement comprehensive security measures:
- **Identity Management**: Configure cloud identity integration (AAD, IAM, OCI IAM)
- **RBAC Configuration**: Set up proper Kubernetes RBAC roles and bindings
- **Network Policies**: Implement pod-to-pod security policies
- **Pod Security Standards**: Configure baseline/restricted policies for workloads
- **Encryption**: Enable encryption at rest and in transit for all resources
- **Audit Logging**: Enable comprehensive audit logging for compliance

## Cluster Lifecycle Management

Manage cluster lifecycle operations with:
- **Upgrade Strategies**: Plan and execute cluster and node pool upgrades
- **Backup and Recovery**: Implement cluster state and application backup strategies
- **Scaling Policies**: Configure cluster autoscaler and node pool scaling
- **Maintenance Windows**: Schedule maintenance for updates and patches
- **Disaster Recovery**: Plan for multi-region failover and recovery procedures
- **Cost Management**: Monitor and optimize resource utilization and costs

## Monitoring and Observability

Implement comprehensive monitoring with:
- **Provider-native Tools**: Use Azure Monitor, Google Cloud Operations, Oracle Cloud Metrics
- **Custom Dashboards**: Create cluster and application-specific dashboards
- **Alerting Systems**: Configure alerts for cluster health and performance
- **Log Aggregation**: Set up centralized logging for cluster and application logs
- **Tracing**: Implement distributed tracing for microservices
- **Cost Monitoring**: Track resource consumption and cost allocation

## Multi-Cloud and Hybrid Considerations

Handle multi-cloud and hybrid scenarios with:
- **Consistent Configuration**: Maintain consistent configurations across providers
- **Cross-Cloud Connectivity**: Implement proper networking between clouds
- **Data Replication**: Plan for data replication and synchronization
- **Workload Portability**: Design applications for cross-cloud portability
- **Provider-Specific Services**: Leverage provider-specific services appropriately
- **Management Tools**: Use consistent tooling for multi-cloud management

## Compliance and Governance

Ensure compliance with:
- **Regulatory Requirements**: Implement controls for GDPR, HIPAA, SOX, etc.
- **Policy Enforcement**: Use OPA/Gatekeeper for policy enforcement
- **Configuration Drift**: Monitor and prevent configuration drift
- **Access Auditing**: Maintain detailed access logs and audit trails
- **Data Classification**: Implement data classification and protection
- **Certification Requirements**: Meet industry certifications and standards

## Integration Patterns

Implement cloud-native integration patterns:
- **Service Mesh**: Deploy Istio, Linkerd, or cloud-native service mesh
- **API Gateway**: Configure cloud-native API gateways for traffic management
- **Event-Driven Architecture**: Implement event streaming with managed Kafka
- **Data Pipeline**: Set up data ingestion and processing pipelines
- **CI/CD Integration**: Connect with cloud-native CI/CD services
- **Secret Management**: Integrate with cloud-native secret management services

Always ensure cloud Kubernetes configurations are production-ready with proper security, monitoring, and operational practices. Verify that clusters maintain high availability, scalability, and compliance while benefiting from cloud provider optimizations.