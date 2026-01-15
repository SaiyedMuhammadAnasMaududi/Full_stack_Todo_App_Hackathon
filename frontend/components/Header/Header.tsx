'use client';

import { useEffect, useState, useRef } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import AuthUtils from '@/lib/auth';

export default function Header() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const router = useRouter();

  useEffect(() => {
    // Check authentication status on mount
    const checkAuthStatus = () => {
      const authenticated = AuthUtils.isAuthenticated();
      setIsAuthenticated(authenticated);

      if (authenticated) {
        const user = AuthUtils.getUserFromToken();
        if (user) {
          setUserEmail(user.email);
        }
      }
    };

    checkAuthStatus();

    // Listen for storage events to update auth status across tabs
    const handleStorageChange = () => {
      checkAuthStatus();
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    // Clear tokens
    AuthUtils.removeTokens();

    // Update state
    setIsAuthenticated(false);
    setUserEmail('');

    // Redirect to login
    router.push('/login');
  };

  const [showProfileDropdown, setShowProfileDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Function to generate initial avatar from email
  const getInitials = (email: string) => {
    const names = email.split('@')[0].split('.');
    const initials = names.map(name => name.charAt(0).toUpperCase()).join('');
    return initials.substring(0, 2);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowProfileDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center group">
              <div className="bg-gradient-to-r from-primary-500 to-primary-600 p-2 rounded-lg group-hover:scale-105 transition-transform duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <span className="ml-2 text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                SecureTask Manager
              </span>
            </Link>
            <nav className="ml-10 flex space-x-8">
              {isAuthenticated ? (
                <>
                  <Link
                    href="/tasks"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-primary-600 hover:border-primary-500 transition-colors duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    My Tasks
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/login"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-primary-600 hover:border-primary-500 transition-colors duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    Login
                  </Link>
                  <Link
                    href="/signup"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-gray-500 hover:text-primary-600 hover:border-primary-500 transition-colors duration-200"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    Sign Up
                  </Link>
                </>
              )}
            </nav>
          </div>

          <div className="flex items-center">
            {isAuthenticated ? (
              <div className="flex items-center">
                {/* Profile dropdown */}
                <div className="relative ml-3">
                  <div>
                    <button
                      type="button"
                      className="flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-shadow duration-200"
                      id="user-menu-button"
                      aria-expanded="false"
                      aria-haspopup="true"
                      onClick={() => setShowProfileDropdown(!showProfileDropdown)}
                    >
                      <span className="sr-only">Open user menu</span>
                      <div className="h-9 w-9 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center text-white font-medium shadow-md hover:shadow-lg transition-shadow duration-200">
                        {getInitials(userEmail)}
                      </div>
                    </button>
                  </div>

                  {showProfileDropdown && (
                    <div
                      ref={dropdownRef}
                      className="origin-top-right absolute right-0 mt-2 w-56 rounded-xl shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50 border border-gray-200 transform transition-all duration-200 ease-out"
                      role="menu"
                      aria-orientation="vertical"
                      aria-labelledby="user-menu-button"
                    >
                      <div className="px-4 py-3 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-gray-100 rounded-t-xl">
                        <p className="text-sm font-medium text-gray-900 truncate">{userEmail}</p>
                        <p className="text-xs text-gray-500 flex items-center">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                          Verified Account
                        </p>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gradient-to-r from-red-50 to-red-100 hover:text-red-600 transition-colors duration-200 flex items-center"
                        role="menuitem"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        Sign out
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <Link
                href="/login"
                className="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 inline mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}