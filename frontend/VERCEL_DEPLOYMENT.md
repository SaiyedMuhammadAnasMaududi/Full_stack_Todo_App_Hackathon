# Deploying to Vercel

To deploy this frontend to Vercel with connection to your deployed backend, follow these steps:

## Prerequisites
- Your backend should be deployed and accessible at: `https://syedmuhammadanasmaududi-todo-backend.hf.space`

## Environment Variables Setup
Before deploying to Vercel, you need to set the following environment variables in your Vercel dashboard:

### Required Environment Variables:
- `NEXT_PUBLIC_BETTER_AUTH_URL`: `https://syedmuhammadanasmaududi-todo-backend.hf.space`
- `BETTER_AUTH_SECRET`: Your secret key (same as used in the backend)
- `NEXT_PUBLIC_API_BASE_URL`: `https://syedmuhammadanasmaududi-todo-backend.hf.space`

## Deployment Steps

1. Fork or clone this repository
2. Go to [Vercel](https://vercel.com/) and sign in
3. Click "New Project" and import your forked/cloned repository
4. During project setup, add the environment variables listed above
5. Click "Deploy" and Vercel will automatically build and deploy your application

## Important Notes
- The application uses the environment variables to connect to your deployed backend
- Make sure your backend is accessible and the CORS settings allow requests from your Vercel deployment URL
- The frontend is built with Next.js 14 and uses the App Router
- Authentication and API calls will be directed to your deployed backend

## Troubleshooting
- If API calls fail, verify that your backend URL is correct and accessible
- Check that the BETTER_AUTH_SECRET matches between frontend and backend
- Ensure CORS headers in your backend allow requests from your frontend domain