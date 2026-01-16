import { useState, useEffect } from 'react';
import AuthUtils from '@/lib/auth';

interface User {
  id: string;
  email: string;
}

interface UseAuthReturn {
  user: User | null;
  loading: boolean;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Get user info from token
    const userInfo = AuthUtils.getUserFromToken();
    setUser(userInfo);
    setLoading(false);

    // Listen for storage events to update auth status across tabs
    const handleStorageChange = () => {
      const updatedUserInfo = AuthUtils.getUserFromToken();
      setUser(updatedUserInfo);
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return { user, loading };
};

export default useAuth;
//helllooo