# Registration Test Script

This script tests the registration endpoint with a new email to verify it works properly.

## Step 1: Test with a new email address
Try registering with a completely new email address that has never been used before on your backend.

## Step 2: Check the exact request being sent
1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Attempt to register
4. Look at the request payload for the registration call
5. Verify it matches: {"email": "email@example.com", "password": "your_password"}

## Step 3: Manual API test
Try this curl command with a unique email:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test_user_'$(date +%s)'@example.com", "password":"SimplePass123!"}' \
  https://syedmuhammadanasmaududi-todo-backend.hf.space/api/auth/register
```

## Expected Successful Response Format
The backend should return something like:
```json
{
  "user": {
    "id": "some-user-id",
    "email": "your-email@example.com"
  },
  "token": "jwt-token-string"
}
```

## Common Issues and Solutions
- If getting "Email already registered": Use a different email
- If getting 500 error: The server has an issue processing the request
- If getting 422 error: The request format is invalid

## Verification
- The endpoint exists and is accessible
- The authentication between frontend and backend is configured correctly
- The issue is likely data-related (email already exists or password validation)