'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import AuthGuard from '@/components/AuthGuard/AuthGuard';
import Header from '@/components/Header/Header';
import TaskList, { TaskListHandle } from '@/components/TaskList/TaskList';
import TaskForm from '@/components/TaskForm/TaskForm';
import PageTransition from '@/components/PageTransition/PageTransition';
import TaskStatistics from '@/components/TaskStatistics/TaskStatistics';
import TaskChart from '@/components/TaskChart/TaskChart';
import ChatBot from '@/components/ChatBot/ChatBot';
import { Task } from '@/types';
import AuthUtils from '@/lib/auth';

export default function TasksPage() {
  const [userId, setUserId] = useState<string | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const router = useRouter();
  const taskListRef = useRef<TaskListHandle>(null);

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

  const handleTaskCreated = (task: Task) => {
    // Refresh the TaskList to show the new task
    if (taskListRef.current) {
      taskListRef.current.refresh();
    }
    console.log('Task created:', task);
  };

  // Function to update tasks for statistics
  const updateTasksForStats = (updatedTasks: Task[]) => {
    setTasks(updatedTasks);
  };

  if (!userId) {
    // Show loading state while checking auth
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full border-blue-500 border-t-transparent"></div>
          <p className="mt-2 text-gray-600">Loading tasks...</p>
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
              <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
              <p className="mt-2 text-sm text-gray-600">
                Manage your personal tasks securely
              </p>
            </div>

            <TaskForm userId={userId} onTaskCreated={handleTaskCreated} />

            <TaskStatistics userId={userId} tasks={tasks} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 card animate-fadeIn">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>
                <TaskList ref={taskListRef} userId={userId} onTasksUpdate={setTasks} />
              </div>

              <div className="animate-fadeIn">
                <TaskChart tasks={tasks} />
              </div>

              <div className="lg:col-span-3 animate-fadeIn mt-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">AI Assistant</h2>
                <div className="h-[500px]">
                  <ChatBot />
                </div>
              </div>
            </div>
          </div>
        </div>
      </AuthGuard>
    </PageTransition>
  );
}