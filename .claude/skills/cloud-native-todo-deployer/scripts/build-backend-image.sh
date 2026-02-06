#!/bin/bash

# Build Backend Container Image
# This script builds the backend container image using Docker

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -p PATH              Path to backend source code (default: ./backend)"
    echo "  -t TAG               Image tag (default: latest)"
    echo "  -n NAME              Image name (default: todo-backend)"
    echo "  -h                   Show this help message"
    exit 1
}

# Default values
PATH="./backend"
TAG="latest"
NAME="todo-backend"

# Parse command line options
while getopts "p:t:n:h" opt; do
    case $opt in
        p) PATH="$OPTARG" ;;
        t) TAG="$OPTARG" ;;
        n) NAME="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

echo "🐳 Building backend container image..."
echo "Path: $PATH"
echo "Image: $NAME:$TAG"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

# Check if path exists
if [ ! -d "$PATH" ]; then
    echo "❌ Backend source path does not exist: $PATH"
    exit 1
fi

# Check if Dockerfile exists, if not create one
if [ ! -f "$PATH/Dockerfile" ]; then
    echo "📄 Creating Dockerfile for backend..."
    cat > "$PATH/Dockerfile" <<EOF
# Multi-stage build for production-ready backend image
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \\
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed at runtime
RUN apt-get update && apt-get install -y \\
    && rm -rf /var/lib/apt/lists/* \\
    && apt-get clean

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy wheels and install them
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
    echo "✅ Dockerfile created for backend"
fi

# Build the image
echo "🔨 Building image $NAME:$TAG from $PATH..."
docker build -t $NAME:$TAG $PATH

echo "✅ Backend image built successfully!"
echo "Image: $NAME:$TAG"