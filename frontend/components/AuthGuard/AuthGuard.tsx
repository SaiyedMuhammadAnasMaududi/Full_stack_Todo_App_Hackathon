'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AuthUtils from '@/lib/auth';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean; // If true, requires authentication; if false, redirects away if authenticated
}

export default function AuthGuard({ children, requireAuth = true }: AuthGuardProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null); // null = checking
  const router = useRouter();

  useEffect(() => {
    const checkAuthStatus = async () => {
      const authenticated = AuthUtils.isAuthenticated();

      if (requireAuth && !authenticated) {
        // User needs to be authenticated but is not, redirect to login
        router.push('/login');
      } else if (!requireAuth && authenticated) {
        // User should not be authenticated but is, redirect to tasks
        router.push('/tasks');
      } else {
        // Auth status is as expected
        setIsAuthenticated(authenticated);
      }
    };

    // Check auth status after component mounts
    checkAuthStatus();
  }, [requireAuth, router]);

  // While checking auth status, show loading state
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full border-blue-500 border-t-transparent"></div>
          <p className="mt-2 text-gray-600">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // If auth status is as expected, render children
  return <>{children}</>;
}