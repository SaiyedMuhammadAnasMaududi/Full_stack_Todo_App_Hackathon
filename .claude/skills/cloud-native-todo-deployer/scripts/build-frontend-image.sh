#!/bin/bash

# Build Frontend Container Image
# This script builds the frontend container image using Docker

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -p PATH              Path to frontend source code (default: ./frontend)"
    echo "  -t TAG               Image tag (default: latest)"
    echo "  -n NAME              Image name (default: todo-frontend)"
    echo "  -h                   Show this help message"
    exit 1
}

# Default values
PATH="./frontend"
TAG="latest"
NAME="todo-frontend"

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

echo "🐳 Building frontend container image..."
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
    echo "❌ Frontend source path does not exist: $PATH"
    exit 1
fi

# Check if Dockerfile exists, if not create one
if [ ! -f "$PATH/Dockerfile" ]; then
    echo "📄 Creating Dockerfile for frontend..."
    cat > "$PATH/Dockerfile" <<EOF
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \\
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \\
  elif [ -f package-lock.json ]; then npm ci; \\
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \\
    adduser -S nextjs -u 1001

# Copy necessary files from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV NODE_ENV production

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
EOF
    echo "✅ Dockerfile created for frontend"
fi

# Build the image
echo "🔨 Building image $NAME:$TAG from $PATH..."
docker build -t $NAME:$TAG $PATH

echo "✅ Frontend image built successfully!"
echo "Image: $NAME:$TAG"