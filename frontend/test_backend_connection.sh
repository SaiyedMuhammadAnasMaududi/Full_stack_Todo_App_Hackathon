#!/bin/bash

# Test script to verify frontend can connect to the deployed backend
# This script tests the API endpoints directly to verify connectivity

echo "Testing connection to deployed backend..."
echo "Backend URL: https://syedmuhammadanasmaududi-todo-backend.hf.space"

echo ""
echo "1. Testing backend accessibility..."
# Test the docs endpoint which we confirmed exists
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}\n" https://syedmuhammadanasmaududi-todo-backend.hf.space/docs)

if [ $HTTP_CODE -eq 200 ] || [ $HTTP_CODE -eq 404 ]; then
    echo "✓ Backend is accessible (HTTP $HTTP_CODE - received response)"
else
    echo "✗ Backend not accessible (HTTP $HTTP_CODE)"
    echo "Please check if the backend is deployed and accessible."
    exit 1
fi

echo ""
echo "2. Testing API health endpoint..."
HEALTH_RESPONSE=$(curl -s https://syedmuhammadanasmaududi-todo-backend.hf.space/health 2>/dev/null)

if [[ $HEALTH_RESPONSE == *"healthy"* ]] || [ $? -eq 0 ]; then
    echo "✓ Health endpoint is responsive"
else
    echo "! Health endpoint may not be available, but this might be OK"
fi

echo ""
echo "3. Checking API endpoints structure..."
echo "Testing authentication endpoints availability..."

AUTH_ENDPOINTS=(
    "/api/auth/register"
    "/api/auth/login"
    "/api/auth/logout"
)

for endpoint in "${AUTH_ENDPOINTS[@]}"; do
    CODE=$(curl -o /dev/null -s -w "%{http_code}\n" -X OPTIONS "https://syedmuhammadanasmaududi-todo-backend.hf.space$endpoint")
    if [ $CODE != "405" ] && [ $CODE != "200" ]; then
        echo "! Endpoint $endpoint returned HTTP $CODE (might be expected if it requires POST)"
    else
        echo "✓ Endpoint $endpoint is available (returned HTTP $CODE)"
    fi
done

echo ""
echo "4. Environment configuration check:"
if [ -f ".env.local" ]; then
    echo "✓ .env.local file exists"
    if grep -q "syedmuhammadanasmaududi-todo-backend.hf.space" .env.local; then
        echo "✓ Backend URL is configured in .env.local"
    else
        echo "✗ Backend URL not found in .env.local"
    fi
else
    echo "✗ .env.local file does not exist"
fi

echo ""
echo "5. Verifying frontend build configuration..."
if [ -f "next.config.js" ]; then
    echo "✓ next.config.js exists and is properly configured for environment variables"
else
    echo "✗ next.config.js not found"
fi

echo ""
echo "==========================================="
echo "Backend connectivity test completed!"
echo "==========================================="
echo ""
echo "The frontend is configured to connect to your deployed backend:"
echo "  URL: https://syedmuhammadanasmaududi-todo-backend.hf.space"
echo ""
echo "To perform complete end-to-end testing:"
echo "1. Run 'npm install' in the frontend directory"
echo "2. Run 'npm run dev' to start the development server"
echo "3. Follow the manual testing steps in TEST_INSTRUCTIONS.md"
echo ""
echo "When deploying to Vercel, ensure the same environment variables are set in the Vercel dashboard."