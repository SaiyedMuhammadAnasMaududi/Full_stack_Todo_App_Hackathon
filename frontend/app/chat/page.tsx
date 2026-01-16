'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import AuthGuard from '@/components/AuthGuard/AuthGuard';
import Header from '@/components/Header/Header';
import ChatBot from '@/components/ChatBot/ChatBot';
import PageTransition from '@/components/PageTransition/PageTransition';
import AuthUtils from '@/lib/auth';

export default function ChatPage() {
  const [userId, setUserId] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    // Get user info from token
    const user = AuthUtils.getUserFromToken();
    if (user) {
      setUserId(user.id);
    } else {
      // If no user is authenticated, redirect to login
      router.push('/login');
    }
  }, [router]);

  if (!userId) {
    // Show loading state while checking auth
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full border-blue-500 border-t-transparent"></div>
          <p className="mt-2 text-gray-600">Loading chat...</p>
        </div>
      </div>
    );
  }

  return (
    <PageTransition>
      <AuthGuard requireAuth={true}>
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
          <Header />

          <div className="container mx-auto py-6 px-4">
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
              <p className="mt-2 text-sm text-gray-600">
                Chat with your AI assistant to manage tasks
              </p>
            </div>

            <div className="h-[calc(100vh-200px)]">
              <ChatBot />
            </div>
          </div>
        </div>
      </AuthGuard>
    </PageTransition>
  );
}