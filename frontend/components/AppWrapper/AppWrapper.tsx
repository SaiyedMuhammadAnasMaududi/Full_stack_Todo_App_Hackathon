'use client';

import { useState, useEffect } from 'react';
import SplashScreen from '../SplashScreen/SplashScreen';

interface AppWrapperProps {
  children: React.ReactNode;
}

export default function AppWrapper({ children }: AppWrapperProps) {
  const [showSplash, setShowSplash] = useState(true);

  const handleSplashComplete = () => {
    setShowSplash(false);
  };

  return (
    <>
      {showSplash ? (
        <SplashScreen onSplashComplete={handleSplashComplete} />
      ) : (
        <>{children}</>
      )}
    </>
  );
}