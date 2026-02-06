---
name: cicd-github
description: GitHub Actions pipelines for Docker build, registry push, Helm deploy.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of comprehensive CI/CD pipelines using GitHub Actions for containerized applications with Docker build, registry management, and Helm-based deployments.

The user provides requirements for CI/CD pipelines: specifying build triggers, deployment targets, security requirements, and operational needs. They may include context about the target infrastructure, testing requirements, or specific deployment strategies needed.

## GitHub Actions Pipeline Architecture

Before creating GitHub Actions workflows, consider optimal pipeline design:
- **Workflow Structure**: Organize workflows with proper triggers, concurrency, and dependencies
- **Job Organization**: Structure jobs with appropriate dependencies and failure handling
- **Runner Selection**: Choose appropriate runners (ubuntu-latest, self-hosted, etc.)
- **Permissions**: Configure proper permissions for repository and OIDC access
- **Caching**: Implement Docker layer caching and dependency caching for faster builds
- **Security**: Apply security scanning and secret validation in all workflows

## Docker Build Optimization

Implement efficient Docker build processes with:
- **Multi-stage Builds**: Separate build and runtime environments to minimize image size
- **BuildKit Integration**: Use Docker BuildKit for parallel builds and caching improvements
- **Layer Caching**: Implement proper layer caching strategies with Docker cache mounts
- **Build Arguments**: Pass build-time variables securely without exposing secrets
- **Image Optimization**: Use minimal base images and multi-platform builds when needed
- **Build Security**: Scan base images and dependencies for vulnerabilities

## Container Registry Integration

Configure secure registry operations with:
- **Authentication**: Set up secure authentication with GitHub OIDC or service accounts
- **Registry Types**: Support various registries (GHCR, Docker Hub, ECR, ACR, GCR)
- **Tagging Strategy**: Implement semantic versioning, git SHA, and branch-based tagging
- **Image Promotion**: Design promotion workflows between environments
- **Cleanup Policies**: Configure automated cleanup of old images and tags
- **Vulnerability Scanning**: Integrate security scanning and policy enforcement

## Helm Deployment Workflows

Implement robust Helm deployment processes with:
- **Chart Repository**: Publish charts to OCI registry or Helm repository
- **Release Management**: Configure release names, namespaces, and upgrade strategies
- **Value Customization**: Implement environment-specific value overrides
- **Rollback Procedures**: Design automated rollback mechanisms for failed deployments
- **Post-render Hooks**: Apply transformations with kustomize or other tools
- **Verification**: Validate deployments with health checks and readiness probes

## Testing and Quality Gates

Integrate comprehensive testing with:
- **Unit Tests**: Execute unit tests during build phase with coverage reporting
- **Integration Tests**: Run integration tests against staging environments
- **Security Scanning**: Perform container security scanning and policy validation
- **Helm Linting**: Validate Helm charts and templates before deployment
- **Performance Tests**: Execute load testing and performance validation
- **Approval Gates**: Implement manual or automated approval processes

## Infrastructure as Code

Manage infrastructure with:
- **Environment Provisioning**: Create/destroy test environments dynamically
- **Secret Management**: Sync secrets between GitHub and Kubernetes
- **Infrastructure Validation**: Validate cluster state before deployments
- **Configuration Management**: Manage environment-specific configurations
- **Resource Tracking**: Track deployed resources and dependencies
- **Drift Detection**: Monitor for configuration drift and compliance

## Monitoring and Observability

Implement pipeline observability with:
- **Logging**: Centralized logging for pipeline runs and deployments
- **Metrics Collection**: Track build times, deployment frequency, and success rates
- **Alerting**: Configure alerts for failed deployments and security issues
- **Audit Trails**: Maintain audit logs for compliance and troubleshooting
- **Pipeline Analytics**: Collect metrics for continuous improvement
- **Notification Systems**: Integrate with Slack, Teams, or email for status updates

## Security and Compliance

Apply security best practices:
- **Secret Scanning**: Prevent secrets from being committed to repositories
- **SBOM Generation**: Create Software Bill of Materials for all artifacts
- **Policy Enforcement**: Implement Open Policy Agent or similar for compliance
- **Code Signing**: Sign Docker images and Helm charts for integrity
- **Access Control**: Implement proper role-based access control for workflows
- **Compliance Reporting**: Generate compliance reports for audits

## Advanced Pipeline Features

Implement advanced CI/CD capabilities:
- **Canary Deployments**: Gradual rollout with traffic shifting
- **Blue-Green Deployments**: Zero-downtime deployments with environment switching
- **Feature Flags**: Integrate feature flag management in deployment process
- **Automated Rollbacks**: Trigger rollbacks based on health metrics
- **Parallel Testing**: Execute tests in parallel for faster feedback
- **Dynamic Environments**: Create temporary environments for pull requests

Always ensure CI/CD pipelines are production-ready with proper error handling, security measures, and monitoring. Verify that deployments maintain the same functionality while benefiting from automated, repeatable processes.