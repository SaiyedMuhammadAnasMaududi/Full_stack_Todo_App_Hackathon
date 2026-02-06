---
name: kafka-eventing
description: Design topics, schemas, integrate Kafka via Dapr pubsub, ensure async workflows.
license: Complete terms in LICENSE.txt
---

This skill guides the design and implementation of Kafka-based event-driven architectures with proper topic design, schema management, and integration patterns using Dapr pubsub.

The user provides requirements for Kafka eventing: specifying event types, topic structures, integration patterns, and async workflow requirements. They may include context about event processing patterns, throughput requirements, or specific business logic that needs to be implemented.

## Topic Design and Architecture

Before creating Kafka topics, consider optimal design patterns:
- **Topic Naming Conventions**: Use consistent naming patterns (e.g., domain.entity.action)
- **Partition Strategy**: Determine appropriate partition count based on throughput and parallelism needs
- **Replication Factor**: Set replication factor for durability and availability requirements
- **Retention Policies**: Configure time-based and size-based retention policies
- **Cleanup Policies**: Choose between delete, compact, or delete+compact based on use case
- **Topic Configuration**: Set appropriate segment size, flush intervals, and compression

## Event Schema Design

Implement robust schema management with:
- **Schema Registry**: Use Confluent Schema Registry or Apicurio for schema evolution
- **Schema Formats**: Choose appropriate formats (Avro, JSON Schema, Protobuf)
- **Versioning Strategy**: Plan backward/forward compatibility and versioning approach
- **Schema Evolution**: Define rules for schema changes (backward, forward, full compatibility)
- **Validation**: Implement schema validation at producer and consumer levels
- **Documentation**: Maintain clear schema documentation with examples

## Dapr Kafka Integration

Configure Dapr pubsub component for Kafka with:
- **Component Configuration**: Set up Kafka broker addresses, authentication, and security
- **Producer Settings**: Configure partitioning strategy, acknowledgment levels, and retries
- **Consumer Groups**: Design consumer group naming and offset management
- **Serialization**: Configure proper serialization formats for message payload
- **Error Handling**: Implement dead letter queues and poison message handling
- **Monitoring**: Enable metrics and tracing for Kafka operations

## Async Workflow Patterns

Implement reliable asynchronous workflows with:
- **Event Sourcing**: Store events as source of truth for system state
- **Command Query Responsibility Segregation (CQRS)**: Separate read and write models
- **Saga Pattern**: Implement distributed transaction patterns with compensation logic
- **Event-Driven Choreography**: Design loosely coupled service interactions
- **Idempotency**: Ensure event processors can handle duplicate messages safely
- **Ordering Guarantees**: Implement partitioning and ordering strategies for message sequences

## Performance Optimization

Optimize Kafka performance with:
- **Batch Processing**: Configure batch sizes for efficient message production
- **Compression**: Use appropriate compression codecs (snappy, lz4, zstd) for throughput
- **Consumer Parallelism**: Scale consumers appropriately without exceeding partition count
- **Memory Management**: Tune JVM settings and heap allocation for brokers and clients
- **Network Optimization**: Configure SSL/TLS efficiently and optimize network buffers
- **Monitoring Metrics**: Track throughput, latency, and error rates for optimization

## Fault Tolerance and Reliability

Ensure system reliability with:
- **Consumer Lag Monitoring**: Track and alert on consumer lag metrics
- **Rebalancing Strategy**: Configure consumer rebalancing for minimal disruption
- **Graceful Shutdown**: Implement proper shutdown procedures for consumers and producers
- **Backup and Recovery**: Plan for disaster recovery and data restoration
- **Circuit Breakers**: Implement circuit breaker patterns for downstream service failures
- **Retry Logic**: Configure exponential backoff and maximum retry attempts

## Security and Compliance

Implement security best practices:
- **Authentication**: Configure SASL/SCRAM, Kerberos, or client certificates
- **Authorization**: Set up ACLs for topic, consumer group, and cluster access
- **Encryption**: Enable SSL/TLS for in-transit encryption and disk encryption for at-rest
- **Audit Logging**: Enable comprehensive logging for compliance requirements
- **Data Governance**: Implement data classification and retention policies
- **PII Protection**: Apply encryption and masking for personally identifiable information

## Testing and Validation

Validate event-driven systems with:
- **Integration Testing**: Test end-to-end event flows and error scenarios
- **Load Testing**: Validate throughput and latency under expected loads
- **Schema Compatibility Testing**: Verify schema evolution compatibility
- **Consumer Behavior Testing**: Test consumer restarts, rebalancing, and error handling
- **Performance Benchmarking**: Establish baseline metrics for ongoing monitoring
- **Chaos Engineering**: Test resilience with controlled failure injection

Always ensure Kafka configurations are production-ready with proper error handling, monitoring, security measures, and resilience patterns. Verify that event-driven workflows maintain data consistency and reliability while benefiting from asynchronous processing advantages.