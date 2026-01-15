'use client';

import { useEffect, useState } from 'react';
import { Task } from '@/types';

interface TaskStatisticsProps {
  userId: string;
  tasks: Task[];
}

interface TaskStats {
  total: number;
  completed: number;
  pending: number;
  overdue: number;
  completionRate: number;
}

export default function TaskStatistics({ userId, tasks }: TaskStatisticsProps) {
  const [stats, setStats] = useState<TaskStats>({
    total: 0,
    completed: 0,
    pending: 0,
    overdue: 0,
    completionRate: 0
  });

  useEffect(() => {
    if (tasks && tasks.length > 0) {
      const total = tasks.length;
      const completed = tasks.filter(task => task.completed).length;
      const pending = tasks.filter(task => !task.completed).length;

      // For simplicity, we'll consider tasks older than 7 days as overdue if not completed
      const overdue = tasks.filter(task => {
        const taskDate = new Date(task.createdAt);
        const today = new Date();
        const diffDays = Math.floor((today.getTime() - taskDate.getTime()) / (1000 * 60 * 60 * 24));
        return !task.completed && diffDays > 7;
      }).length;

      const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

      setStats({
        total,
        completed,
        pending,
        overdue,
        completionRate
      });
    } else {
      setStats({
        total: 0,
        completed: 0,
        pending: 0,
        overdue: 0,
        completionRate: 0
      });
    }
  }, [tasks]);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 transform transition-all duration-300 hover:scale-105">
        <div className="text-sm font-medium text-gray-500">Total Tasks</div>
        <div className="mt-1 text-3xl font-semibold text-gray-900">{stats.total}</div>
        <div className="mt-2 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <span className="ml-1 text-sm text-gray-500">All tasks</span>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 transform transition-all duration-300 hover:scale-105">
        <div className="text-sm font-medium text-gray-500">Completed</div>
        <div className="mt-1 text-3xl font-semibold text-green-600">{stats.completed}</div>
        <div className="mt-2 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="ml-1 text-sm text-green-600">Done</span>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 transform transition-all duration-300 hover:scale-105">
        <div className="text-sm font-medium text-gray-500">Pending</div>
        <div className="mt-1 text-3xl font-semibold text-yellow-600">{stats.pending}</div>
        <div className="mt-2 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="ml-1 text-sm text-yellow-600">To do</span>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border border-gray-200 transform transition-all duration-300 hover:scale-105">
        <div className="text-sm font-medium text-gray-500">Completion</div>
        <div className="mt-1 text-3xl font-semibold text-blue-600">{stats.completionRate}%</div>
        <div className="mt-2">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
              style={{ width: `${stats.completionRate}%` }}
            ></div>
          </div>
          <span className="text-sm text-blue-600 mt-1">Progress</span>
        </div>
      </div>
    </div>
  );
}