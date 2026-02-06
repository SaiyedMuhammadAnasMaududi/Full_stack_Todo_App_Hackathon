---
name: dapr-runtime
description: Configure Dapr sidecars, components, pubsub, state, jobs, secrets.
license: Complete terms in LICENSE.txt
---

This skill guides the configuration and deployment of Dapr (Distributed Application Runtime) components for microservices applications with production-ready patterns.

The user provides requirements for Dapr configuration: specifying sidecar configurations, component types (pubsub, state management, secrets, jobs), and integration requirements. They may include context about the hosting environment, security requirements, or specific Dapr capabilities needed.

## Dapr Sidecar Configuration

Before configuring Dapr sidecars, consider optimal setup for your application:
- **Sidecar Injection**: Configure automatic or manual sidecar injection with proper annotations
- **Resource Allocation**: Set appropriate CPU/memory limits for sidecar containers
- **Configuration Files**: Create daprd configuration with tracing, metrics, and security settings
- **App Channel Settings**: Configure HTTP/gRPC communication between app and sidecar
- **Health Probes**: Set up liveness and readiness probes for sidecar monitoring

## PubSub Components

Implement robust pubsub configurations with:
- **Message Brokers**: Configure Kafka, RabbitMQ, Azure Service Bus, AWS SQS, GCP PubSub
- **Topics and Subscriptions**: Define topic names, subscription patterns, and delivery policies
- **Message Serialization**: Set up proper serialization formats (JSON, Protobuf)
- **Retry Policies**: Configure exponential backoff and maximum retry attempts
- **Dead Letter Queues**: Implement poison message handling and error recovery
- **Ordering Guarantees**: Configure partitioning and ordering based on requirements

## State Management Components

Configure reliable state storage with:
- **State Stores**: Set up Redis, CosmosDB, DynamoDB, Firestore, PostgreSQL
- **Consistency Levels**: Define strong/weak consistency requirements
- **Partitioning**: Configure key-based partitioning for scalability
- **Encryption**: Enable at-rest and in-transit encryption for sensitive data
- **Concurrency**: Set up optimistic/pessimistic locking mechanisms
- **TTL and Expiration**: Configure automatic cleanup for temporary data

## Jobs and Workflows

Implement distributed job processing with:
- **Temporal Integration**: Configure Temporal workflows for long-running processes
- **Dapr Workflows**: Use Dapr's native workflow capability for stateful operations
- **Cron Jobs**: Set up scheduled tasks with proper error handling
- **Saga Patterns**: Implement compensation logic for distributed transactions
- **Timeout Management**: Configure appropriate timeouts for job execution
- **Monitoring**: Track job status, retries, and completion metrics

## Secrets Management

Secure secret handling with:
- **Secret Stores**: Configure Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, Kubernetes secrets
- **Access Control**: Implement proper RBAC and access policies
- **Mounting Secrets**: Configure secret mounting as environment variables or files
- **Rotation Policies**: Set up automatic secret rotation schedules
- **Reference Syntax**: Use proper secret reference syntax in Dapr components
- **Validation**: Ensure secrets are properly encrypted and validated

## Component Configuration Patterns

Follow best practices for component configuration:
- **Environment Separation**: Maintain different configurations for dev/staging/prod
- **Component Scopes**: Limit component access to specific applications or namespaces
- **Health Monitoring**: Implement health checks for all Dapr components
- **Performance Tuning**: Optimize connection pooling, buffer sizes, and timeouts
- **Backup and Recovery**: Plan for disaster recovery of stateful components
- **Migration Strategies**: Plan component upgrades and schema migrations

## Security and Compliance

Implement security best practices:
- **mTLS Configuration**: Enable mutual TLS between Dapr services
- **Service Invocation**: Configure proper authentication for service-to-service calls
- **Authorization**: Implement role-based access control for Dapr APIs
- **Audit Logging**: Enable comprehensive logging for compliance requirements
- **Network Policies**: Secure Dapr communication with network policies
- **Certificate Management**: Automate certificate renewal and rotation

Always ensure Dapr configurations are production-ready with proper error handling, monitoring, security measures, and resilience patterns. Verify that applications maintain the same functionality while benefiting from Dapr's distributed application runtime capabilities.