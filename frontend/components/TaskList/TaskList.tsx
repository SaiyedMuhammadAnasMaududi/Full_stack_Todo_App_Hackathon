'use client';

import { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { Task } from '@/types';
import DraggableTaskItem from '../DraggableTaskItem/DraggableTaskItem';
import apiClient from '@/lib/api';
import AuthUtils from '@/lib/auth';

interface TaskListProps {
  userId: string;
  onTasksUpdate?: (tasks: Task[]) => void;
}

export interface TaskListHandle {
  refresh: () => void;
}

const TaskList = forwardRef<TaskListHandle, TaskListProps>(({ userId }, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [userId]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTasks = await apiClient.getTasks(userId);
      setTasks(fetchedTasks);

      // Notify parent of task updates for statistics
      if (onTasksUpdate) {
        onTasksUpdate(fetchedTasks);
      }
    } catch (err: any) {
      console.error('Error fetching tasks:', err);
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  // Expose refresh function to parent components
  useImperativeHandle(ref, () => ({
    refresh: fetchTasks
  }));

  const handleTaskUpdate = (updatedTask: Task) => {
    const newTasks = tasks.map(task => task.id === updatedTask.id ? updatedTask : task);
    setTasks(newTasks);

    // Notify parent of task updates for statistics
    if (onTasksUpdate) {
      onTasksUpdate(newTasks);
    }
  };

  const handleTaskDelete = (deletedTaskId: string) => {
    const newTasks = tasks.filter(task => task.id !== deletedTaskId);
    setTasks(newTasks);

    // Notify parent of task updates for statistics
    if (onTasksUpdate) {
      onTasksUpdate(newTasks);
    }
  };

  // Drag and drop functionality
  const [draggedTaskId, setDraggedTaskId] = useState<string | null>(null);
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null);

  const handleDragStart = (e: React.DragEvent<HTMLLIElement>, taskId: string) => {
    setDraggedTaskId(taskId);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', taskId);
  };

  const handleDragOver = (e: React.DragEvent<HTMLLIElement>, index: number) => {
    e.preventDefault();
    setDragOverIndex(index);
  };

  const handleDragLeave = () => {
    setDragOverIndex(null);
  };

  const handleDrop = (e: React.DragEvent<HTMLLIElement>, targetIndex: number) => {
    e.preventDefault();
    setDragOverIndex(null);

    if (!draggedTaskId) return;

    const draggedIndex = tasks.findIndex(task => task.id === draggedTaskId);
    if (draggedIndex === -1 || draggedIndex === targetIndex) {
      setDraggedTaskId(null);
      return;
    }

    const newTasks = [...tasks];
    const [draggedTask] = newTasks.splice(draggedIndex, 1);
    newTasks.splice(targetIndex, 0, draggedTask);

    setTasks(newTasks);
    setDraggedTaskId(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">
              {error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md animate-fadeIn">
      <ul className="divide-y divide-gray-200">
        {tasks.map((task, index) => (
          <DraggableTaskItem
            key={task.id}
            userId={userId}
            task={task}
            onUpdate={handleTaskUpdate}
            onDelete={handleTaskDelete}
            onDragStart={handleDragStart}
            onDragOver={(e) => handleDragOver(e, index)}
            onDrop={(e) => handleDrop(e, index)}
            isDragging={draggedTaskId === task.id}
          />
        ))}
      </ul>
    </div>
  );
});

export default TaskList;