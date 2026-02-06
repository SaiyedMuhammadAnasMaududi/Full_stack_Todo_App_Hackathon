---
name: dockerization
description: Build multi-stage Docker images for frontend and backend, optimize layers, expose ports, push to registry.
license: Complete terms in LICENSE.txt
---

This skill guides the creation of optimized Docker images for full-stack applications with multi-stage builds, layer optimization, and production-ready configurations.

The user provides requirements for containerizing their application: specifying frontend and backend services, deployment targets, and any special requirements for the build process. They may include context about the runtime environment, security requirements, or performance constraints.

## Docker Image Optimization

Before building, consider the optimal architecture for multi-stage builds:
- **Base Images**: Select minimal base images (Alpine, Distroless) to reduce attack surface and image size
- **Layer Caching**: Order Dockerfile instructions to maximize layer reuse (dependencies before application code)
- **Multi-stage Builds**: Separate build and runtime environments to reduce final image size
- **Security**: Run containers as non-root users, scan for vulnerabilities, implement minimal privilege

## Frontend Docker Configuration

For frontend applications (Next.js, React, Vue, etc.), implement:
- Multi-stage build with separate build and production stages
- Dependency installation in separate layer for caching
- Static asset optimization and compression
- Proper port exposure (typically 3000, 80, or 443)
- Health checks and graceful shutdown
- Environment variable handling

## Backend Docker Configuration

For backend services (FastAPI, Express, etc.), implement:
- Virtual environment isolation for Python/Node.js
- Dependency caching layers
- Production-ready WSGI/ASGI server configuration (uvicorn, gunicorn)
- Proper signal handling and graceful shutdown
- Security hardening (non-root user, read-only filesystem where possible)
- Resource limits and health checks

## Build Optimization Strategies

Follow these optimization techniques:
- **Builder Pattern**: Use build stage to compile assets, copy artifacts to runtime stage
- **Dependency Layering**: Separate dependency installation from application code
- **.dockerignore**: Exclude unnecessary files (node_modules, .git, logs, etc.)
- **Image Squashing**: Minimize layers and remove temporary files
- **Security Scanning**: Integrate vulnerability scanning in build pipeline

## Registry and Deployment Preparation

Configure for deployment with:
- Proper tagging strategy (semantic versioning, git SHA)
- Multi-platform support (amd64, arm64) when needed
- Credential management for private registries
- Image signing and verification
- Cleanup of intermediate images

Always ensure images are production-ready with proper logging, monitoring hooks, and security considerations. Verify that the containerized application maintains the same functionality as the original application while benefiting from containerization advantages.