# Frontend Todo Application

This is the frontend for a secure multi-user todo application built with Next.js 16+ and TypeScript.

## Features

- User registration and login with secure authentication
- JWT-based authorization for API requests
- Todo management: create, read, update, delete, and mark tasks as complete
- Responsive design for mobile and desktop
- Secure session management across browser tabs
- Network failure handling with retry mechanism

## Tech Stack

- Next.js 16+ (App Router)
- TypeScript
- React 19+
- Tailwind CSS for styling
- Axios for API requests
- Better Auth for authentication

## Getting Started

### Prerequisites

- Node.js 18+
- Access to the backend API (FastAPI server running)

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create environment file:
   ```bash
   cp .env.local.example .env.local
   ```
5. Update `.env.local` with your environment variables

### Environment Variables

- `NEXT_PUBLIC_BETTER_AUTH_URL` - Backend URL for Better Auth API
- `BETTER_AUTH_SECRET` - Secret used to verify JWT tokens (must match backend)
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API endpoints

### Development

1. Start the development server:
   ```bash
   npm run dev
   ```
2. Open http://localhost:3000 in your browser

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## Security Features

- Passwords must meet security requirements (min 8 chars, mixed case, numbers, special chars)
- JWT tokens are stored securely in localStorage with proper expiration checks
- Proactive token refresh 5 minutes before expiration
- Unauthorized access attempts are logged for security monitoring
- Shared session state across browser tabs (logout in one tab logs out all tabs)

## Architecture

The application follows a component-based architecture with:

- **Pages**: Located in `app/` directory using Next.js App Router
- **Components**: Reusable UI components in `components/` directory
- **Libraries**: Utility functions and API clients in `lib/` directory
- **Types**: TypeScript type definitions in `types/` directory
- **Styles**: Global styles in `styles/` directory

## API Integration

The frontend communicates with the backend via REST API endpoints:

- `/api/{user_id}/tasks` - Task management endpoints
- Better Auth endpoints for authentication

All API requests automatically include the JWT token via the centralized API client.

## Authentication Flow

1. User visits `/signup` to create an account
2. User receives JWT token on successful registration
3. Token is stored in localStorage
4. User is redirected to `/tasks` dashboard
5. All subsequent API requests include the JWT token in the Authorization header

## Error Handling

- Network failures are handled with exponential backoff retry mechanism
- 401 errors trigger automatic logout and redirect to login
- User-friendly error messages are displayed for various failure scenarios
- Loading states provide feedback during API requests