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

const TaskList = forwardRef<TaskListHandle, TaskListProps>(({ userId, onTasksUpdate }, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterPriority, setFilterPriority] = useState<string>('');
  const [filterCompleted, setFilterCompleted] = useState<string>('');
  const [sortBy, setSortBy] = useState<'created_at' | 'priority' | 'due_at' | 'title'>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);

      let fetchedTasks: Task[] = [];

      // Check if we need to use API-based search/filter/sort
      if (searchQuery || filterPriority || filterCompleted !== '' || sortBy !== 'created_at' || sortOrder !== 'desc') {
        // Use API-based search/filter/sort
        if (searchQuery) {
          fetchedTasks = await apiClient.searchTasks(userId, searchQuery);
        } else {
          fetchedTasks = await apiClient.getTasks(userId);
        }

        // Apply filters via API if needed
        if (filterPriority || filterCompleted !== '') {
          const filters: any = {};
          if (filterPriority) filters.priority = filterPriority;
          if (filterCompleted !== '') filters.completed = filterCompleted === 'true';
          fetchedTasks = await apiClient.filterTasks(userId, filters);
        }

        // Apply sorting via API if needed
        if (sortBy !== 'created_at' || sortOrder !== 'desc') {
          fetchedTasks = await apiClient.sortTasks(userId, sortBy, sortOrder);
        }
      } else {
        fetchedTasks = await apiClient.getTasks(userId);
      }

      setTasks(fetchedTasks);
      setFilteredTasks(fetchedTasks);

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

  // Refetch tasks when filters/sorting change
  useEffect(() => {
    fetchTasks();
  }, [userId, searchQuery, filterPriority, filterCompleted, sortBy, sortOrder]);

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

  return (
    <div className="animate-fadeIn">
      {/* Filters and Search Controls */}
      <div className="mb-4 p-4 bg-white rounded-lg shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              id="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search tasks..."
              className="form-control w-full"
            />
          </div>

          <div>
            <label htmlFor="priority-filter" className="block text-sm font-medium text-gray-700 mb-1">
              Priority
            </label>
            <select
              id="priority-filter"
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="form-control w-full"
            >
              <option value="">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div>
            <label htmlFor="completed-filter" className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              id="completed-filter"
              value={filterCompleted}
              onChange={(e) => setFilterCompleted(e.target.value)}
              className="form-control w-full"
            >
              <option value="">All Tasks</option>
              <option value="false">Active</option>
              <option value="true">Completed</option>
            </select>
          </div>

          <div>
            <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">
              Sort By
            </label>
            <div className="flex space-x-2">
              <select
                id="sort"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="form-control flex-1"
              >
                <option value="created_at">Date Created</option>
                <option value="priority">Priority</option>
                <option value="due_at">Due Date</option>
                <option value="title">Title</option>
              </select>
              <select
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value as any)}
                className="form-control w-20"
              >
                <option value="asc">A-Z</option>
                <option value="desc">Z-A</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {tasks.length === 0 ? 'Get started by creating a new task.' : 'Try adjusting your filters.'}
          </p>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {filteredTasks.map((task, index) => (
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
      )}
    </div>
  );
});

export default TaskList;