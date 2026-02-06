import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Perform any necessary health checks here
    // For a basic health check, we can just return a success response

    return NextResponse.json({
      status: 'healthy',
      service: 'todo-frontend-app',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        service: 'todo-frontend-app',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}