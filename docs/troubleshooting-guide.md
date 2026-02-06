# Troubleshooting Guide for AI Todo Chatbot Deployment

This guide provides solutions for common issues encountered when deploying the AI Todo Chatbot to Kubernetes.

## Common Issues and Solutions

### 1. Pod Startup Failures

**Problem**: Pods fail to start or crash immediately after startup

**Solutions**:
- Check pod logs: `kubectl logs <pod-name>`
- Verify environment variables are correctly set in ConfigMaps/Secrets
- Check resource limits and requests in deployment configuration
- Verify image name and tag are correct
- Ensure required secrets are available

**AI Command**:
```bash
kubectl-ai "show logs for failed pods"
```

### 2. Service Connectivity Issues

**Problem**: Services cannot communicate with each other or external dependencies

**Solutions**:
- Verify service names and namespaces match deployment configuration
- Check if services are correctly exposing the right ports
- Verify environment variables for service URLs are set correctly
- Ensure network policies (if any) allow required traffic

**AI Command**:
```bash
kubectl-ai "debug service connectivity between frontend and backend"
```

### 3. Database Connection Problems

**Problem**: Backend service cannot connect to the database

**Solutions**:
- Verify DATABASE_URL in secrets is correctly formatted
- Check if database is accessible from Kubernetes cluster
- Verify database credentials are correct
- Ensure database connection pool settings are appropriate for containerized environment

**AI Command**:
```bash
kubectl-ai "check database connection for backend service"
```

### 4. AI Chatbot Not Responding

**Problem**: AI chatbot functionality is not working

**Solutions**:
- Verify COHERE_API_KEY is correctly set in secrets
- Check if MCP tools are properly configured and accessible
- Verify AI agent configuration parameters
- Ensure proper network connectivity to AI provider

**AI Command**:
```bash
kubectl-ai "troubleshoot ai chatbot connectivity issues"
```

### 5. Health Check Failures

**Problem**: Liveness or readiness probes are failing

**Solutions**:
- Verify health check endpoints exist and return correct status codes
- Adjust probe parameters (initial delay, timeout, failure threshold)
- Check if application is properly initialized before health checks
- Verify service is listening on the expected port

**AI Command**:
```bash
kubectl-ai "analyze health check failures for deployments"
```

### 6. Scaling Issues

**Problem**: Horizontal Pod Autoscaler (HPA) not working properly

**Solutions**:
- Verify metrics server is running in the cluster
- Check HPA configuration and target metrics
- Ensure resource requests are set for CPU/memory metrics
- Verify application can handle increased load

**AI Command**:
```bash
kubectl-ai "analyze horizontal pod autoscaler configuration"
```

### 7. Ingress/Load Balancer Issues

**Problem**: Application is not accessible externally

**Solutions**:
- Verify ingress controller is installed and running
- Check ingress resource configuration
- Ensure service type is set correctly (LoadBalancer or ClusterIP with ingress)
- Verify DNS and routing rules

**AI Command**:
```bash
kubectl-ai "debug ingress and external access issues"
```

### 8. Resource Exhaustion

**Problem**: Nodes running out of memory or CPU

**Solutions**:
- Review resource requests and limits for all deployments
- Check if applications are consuming more resources than allocated
- Adjust resource configuration based on actual usage
- Consider increasing node resources or adding more nodes

**AI Command**:
```bash
kubectl-ai "analyze resource usage and suggest optimizations"
```

### 9. Authentication/Authorization Failures

**Problem**: Users cannot log in or access protected resources

**Solutions**:
- Verify BETTER_AUTH_SECRET is correctly set in secrets
- Check JWT configuration and expiration settings
- Ensure authentication service is accessible
- Verify session management in containerized environment

**AI Command**:
```bash
kubectl-ai "troubleshoot authentication service issues"
```

### 10. Configuration Updates Not Applied

**Problem**: Changes to ConfigMaps or Secrets are not reflected in running pods

**Solutions**:
- Restart deployments after configuration changes: `kubectl rollout restart deployment/<name>`
- Verify configuration values are correctly mounted as volumes or environment variables
- Check if application supports hot-reloading of configuration
- Ensure proper rollout strategy is configured

**AI Command**:
```bash
kubectl-ai "restart deployment to apply configuration changes"
```

## Diagnostic Commands

### Check Overall System Status
```bash
kubectl-ai "show overall system status and health"
```

### Check All Resources
```bash
kubectl get all
```

### Check Events
```bash
kubectl get events --sort-by='.lastTimestamp'
```

### Check Resource Utilization
```bash
kubectl top nodes
kubectl top pods
```

## Prevention Strategies

1. **Proactive Monitoring**: Set up monitoring and alerting for key metrics
2. **Resource Planning**: Properly size resources based on expected load
3. **Health Checks**: Implement comprehensive liveness and readiness probes
4. **Rollback Plans**: Maintain ability to rollback to previous working versions
5. **Regular Testing**: Regularly test deployments in staging environments

## When to Escalate

Contact the development team if:
- Issues persist after following troubleshooting steps
- Root cause involves application code rather than infrastructure
- Security-related issues are discovered
- Performance issues cannot be resolved with configuration changes