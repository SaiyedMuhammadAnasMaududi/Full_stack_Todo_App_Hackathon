#!/bin/bash

# Script to validate Helm charts for the AI Todo Chatbot deployment

echo "Validating Helm charts for AI Todo Chatbot..."

# Validate backend Helm chart
echo "Validating backend Helm chart..."
if [ -d "charts/backend" ]; then
    if command -v helm &> /dev/null; then
        helm lint charts/backend
        if [ $? -eq 0 ]; then
            echo "✓ Backend Helm chart validation passed"
        else
            echo "✗ Backend Helm chart validation failed"
        fi
    else
        echo "⚠ Helm not installed, skipping validation"
    fi
else
    echo "✗ Backend Helm chart directory not found"
fi

# Validate frontend Helm chart
echo "Validating frontend Helm chart..."
if [ -d "charts/frontend" ]; then
    if command -v helm &> /dev/null; then
        helm lint charts/frontend
        if [ $? -eq 0 ]; then
            echo "✓ Frontend Helm chart validation passed"
        else
            echo "✗ Frontend Helm chart validation failed"
        fi
    else
        echo "⚠ Helm not installed, skipping validation"
    fi
else
    echo "✗ Frontend Helm chart directory not found"
fi

echo "Helm chart validation complete."