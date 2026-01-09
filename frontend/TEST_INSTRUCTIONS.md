# Frontend Testing Instructions

This document outlines the manual testing procedures to verify that the frontend works correctly with your deployed backend.

## Prerequisites

1. Ensure your backend is deployed and accessible at: `https://syedmuhammadanasmaududi-todo-backend.hf.space`
2. Make sure you have the `.env.local` file configured with:
   ```
   NEXT_PUBLIC_BETTER_AUTH_URL=https://syedmuhammadanasmaududi-todo-backend.hf.space
   BETTER_AUTH_SECRET=fd5dee830896cab655b4aea325843c70b709564adec9149bbf5c7e1df4b1c174
   NEXT_PUBLIC_API_BASE_URL=https://syedmuhammadanasmaududi-todo-backend.hf.space
   ```

## Test Flow 1: New User Registration

### Step 1: Start the Development Server
```bash
cd /mnt/e/Full_stack_Todo_App_Hackathon/frontend
npm install
npm run dev
```

### Step 2: Navigate to Signup Page
1. Open your browser and go to `http://localhost:3000/signup`
2. You should see the signup form with fields for email, password, and confirm password

### Step 3: Register a New User
1. Fill in the form with:
   - Email: `testuser@example.com` (or any valid email)
   - Password: `TestPass123!` (must meet requirements: 8+ chars, uppercase, lowercase, number, special char)
   - Confirm Password: `TestPass123!`
2. Click "Sign up"
3. **Expected Result**:
   - Account created successfully message
   - Automatically redirected to `/tasks` page
   - User should be authenticated

### Step 4: Verify Registration
1. Check that you're on the `/tasks` page
2. The header should show logged-in state
3. The "My Tasks" page should load without errors

## Test Flow 2: Login with Existing User

### Step 1: Logout (if currently logged in)
1. If you're still on the tasks page from the previous test, clear your browser's localStorage to simulate a fresh session
2. Or close the browser tab and open a new one

### Step 2: Navigate to Login Page
1. Go to `http://localhost:3000/login`
2. You should see the login form with email and password fields

### Step 3: Login with Registered User
1. Fill in the form with:
   - Email: `testuser@example.com` (the email you registered with)
   - Password: `TestPass123!` (the password you registered with)
2. Click "Sign in"
3. **Expected Result**:
   - Successful login (no error messages)
   - Automatically redirected to `/tasks` page
   - User should be authenticated

## Test Flow 3: Task Operations

### Step 1: Create a New Task
1. On the `/tasks` page, find the "Create New Task" form
2. Fill in:
   - Title: "Test Task"
   - Description: "This is a test task to verify functionality"
3. Click "Create Task"
4. **Expected Result**:
   - Task should appear in the task list
   - No error messages

### Step 2: Update a Task
1. Find the task you just created
2. Click the edit icon (pencil button)
3. Modify the title or description
4. Click "Save"
5. **Expected Result**:
   - Task should update without errors
   - Changes should be reflected in the list

### Step 3: Toggle Task Completion
1. Find any task in the list
2. Check the checkbox to mark it as complete
3. **Expected Result**:
   - Task should be visually marked as completed (strikethrough)
   - Status should be saved to the backend

### Step 4: Delete a Task
1. Find a task you want to delete
2. Click the delete icon (trash button)
3. Confirm the deletion when prompted
4. **Expected Result**:
   - Task should be removed from the list
   - No error messages

## Test Flow 4: Session Persistence

### Step 1: Refresh the Page
1. With tasks visible, refresh the browser page (F5 or Ctrl+R)
2. **Expected Result**:
   - User remains logged in
   - Tasks reload from the backend
   - No redirect to login page

### Step 2: Close and Reopen Browser
1. Close the browser completely
2. Reopen and navigate to `http://localhost:3000/tasks`
3. **Expected Result**:
   - If using JWT tokens properly: Should redirect to login page
   - If using persistent storage: May remain logged in depending on token expiry

## Troubleshooting

### Common Issues:

1. **Network Errors**:
   - Check that your backend is accessible at the configured URL
   - Verify CORS settings on your backend
   - Ensure the API endpoints are responding

2. **Authentication Failures**:
   - Verify that the `BETTER_AUTH_SECRET` matches between frontend and backend
   - Check that the authentication endpoints are properly configured

3. **Task Operations Failing**:
   - Ensure user authentication is working correctly
   - Verify that user IDs are being passed correctly in API calls

4. **Environment Variable Issues**:
   - Make sure `.env.local` is properly configured
   - Restart the development server after changing environment variables

## Verification Checklist

- [ ] User can successfully register via signup page
- [ ] User can successfully login via login page
- [ ] User can create new tasks
- [ ] User can view their tasks
- [ ] User can update existing tasks
- [ ] User can mark tasks as complete/incomplete
- [ ] User can delete tasks
- [ ] Session persists appropriately between page refreshes
- [ ] Proper error handling occurs for invalid inputs
- [ ] Proper error handling occurs for network failures

Once all these tests pass, the frontend is ready for deployment to Vercel with confidence that it will work correctly with your deployed backend.