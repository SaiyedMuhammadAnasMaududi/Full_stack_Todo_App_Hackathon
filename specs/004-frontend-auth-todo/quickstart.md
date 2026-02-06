# Quickstart Guide: Frontend Authentication and Todo Application

## Prerequisites

- Node.js 18+ installed
- Access to the backend API (FastAPI server running)
- BETTER_AUTH_SECRET from the backend environment

## Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.local.example .env.local
```

4. Update `.env.local` with the required environment variables:
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your_backend_secret_here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Development

1. Start the development server:
```bash
npm run dev
```

2. Open http://localhost:3000 in your browser

## Key Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## Environment Variables

- `NEXT_PUBLIC_BETTER_AUTH_URL` - Backend URL for Better Auth API
- `BETTER_AUTH_SECRET` - Secret used to verify JWT tokens (must match backend)
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API endpoints

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── login/             # Login page
│   ├── signup/            # Signup page
│   └── tasks/             # Tasks dashboard
├── components/            # Reusable React components
├── lib/                   # Utilities (API client, auth helpers)
├── styles/                # Global styles
└── types/                 # TypeScript type definitions
```

## Authentication Flow

1. User visits `/signup` to create an account
2. User receives JWT token on successful registration
3. Token is stored in localStorage
4. User is redirected to `/tasks` dashboard
5. All subsequent API requests include the JWT token in the Authorization header

## API Integration

The frontend communicates with the backend via REST API endpoints:
- `/api/{user_id}/tasks` - Task management endpoints
- Better Auth endpoints for authentication

All API requests automatically include the JWT token via the centralized API client.