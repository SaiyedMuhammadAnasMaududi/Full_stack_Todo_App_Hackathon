'use client';

import { useState, useEffect } from 'react';

interface SplashScreenProps {
  onSplashComplete: () => void;
}

export default function SplashScreen({ onSplashComplete }: SplashScreenProps) {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Show splash screen for 2 seconds then fade out
    const timer = setTimeout(() => {
      setIsVisible(false);
      // Allow time for fade-out animation before calling callback
      setTimeout(() => {
        onSplashComplete();
      }, 500);
    }, 2000);

    return () => clearTimeout(timer);
  }, [onSplashComplete]);

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 flex items-center justify-center z-50 animate-fadeIn">
      <div className="text-center">
        <div className="mx-auto mb-6 flex justify-center">
          <div className="relative">
            <div className="w-24 h-24 bg-white bg-opacity-20 rounded-full flex items-center justify-center backdrop-blur-sm animate-pulse">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-12 w-12 text-white animate-bounce"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
                />
              </svg>
            </div>
            <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full flex items-center justify-center animate-ping">
              <span className="text-xs font-bold text-white">✓</span>
            </div>
          </div>
        </div>
        <h1 className="text-4xl font-bold text-white mb-2 animate-slideUp">
          SecureTask Manager
        </h1>
        <p className="text-blue-100 text-lg animate-slideUp" style={{ animationDelay: '0.2s' }}>
          Professional Task Management Solution
        </p>
        <div className="mt-8 animate-pulse">
          <div className="w-24 h-1 bg-white bg-opacity-30 rounded-full mx-auto">
            <div className="w-1/2 h-1 bg-white rounded-full animate-progress"></div>
          </div>
        </div>
      </div>
    </div>
  );
}