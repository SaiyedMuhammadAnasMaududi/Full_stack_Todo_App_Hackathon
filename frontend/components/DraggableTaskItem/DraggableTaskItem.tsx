'use client';

import { useState, useRef } from 'react';
import { Task } from '@/types';
import apiClient from '@/lib/api';

interface DraggableTaskItemProps {
  userId: string;
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: string) => void;
  onDragStart: (e: React.DragEvent<HTMLLIElement>, taskId: string) => void;
  onDragOver: (e: React.DragEvent<HTMLLIElement>) => void;
  onDrop: (e: React.DragEvent<HTMLLIElement>) => void;
  isDragging?: boolean;
}

export default function DraggableTaskItem({
  userId,
  task,
  onUpdate,
  onDelete,
  onDragStart,
  onDragOver,
  onDrop,
  isDragging = false
}: DraggableTaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editingTitle, setEditingTitle] = useState(task.title);
  const [editingDescription, setEditingDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleToggleComplete = async () => {
    try {
      setLoading(true);
      const updatedTask = await apiClient.toggleTaskCompletion(userId, task.id, !task.completed);

      // Add a small animation effect when completing a task
      if (!task.completed) {
        // Add a temporary checkmark animation
        const checkbox = document.getElementById(`task-complete-${task.id}`) as HTMLInputElement;
        if (checkbox) {
          checkbox.style.transform = 'scale(1.2)';
          setTimeout(() => {
            if (checkbox) checkbox.style.transform = 'scale(1)';
          }, 200);
        }
      }

      onUpdate(updatedTask);
    } catch (err: any) {
      console.error('Error toggling task completion:', err);
      setError('Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async () => {
    try {
      setLoading(true);
      const updatedTask = await apiClient.updateTask(userId, task.id, {
        title: editingTitle,
        description: editingDescription,
      });
      onUpdate(updatedTask);
      setIsEditing(false);
      setError(null);
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        setLoading(true);
        await apiClient.deleteTask(userId, task.id);
        onDelete(task.id);
      } catch (err: any) {
        console.error('Error deleting task:', err);
        setError(err.message || 'Failed to delete task');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditingTitle(task.title);
    setEditingDescription(task.description || '');
    setError(null);
  };

  return (
    <li
      draggable
      onDragStart={(e) => onDragStart(e, task.id)}
      onDragOver={onDragOver}
      onDrop={onDrop}
      className={`task-item ${task.completed ? 'completed' : ''} transition-all duration-300 ${
        task.completed ? 'opacity-75' : 'opacity-100'
      } ${isDragging ? 'opacity-50 transform scale-95' : 'opacity-100'}`}
      aria-labelledby={`task-title-${task.id}`}
      role="listitem"
    >
      {isEditing ? (
        <div className="w-full">
          {error && (
            <div className="mb-2 text-sm text-red-600" role="alert" aria-live="polite">
              {error}
            </div>
          )}
          <label htmlFor={`task-title-edit-${task.id}`} className="sr-only">
            Task Title
          </label>
          <input
            ref={inputRef}
            type="text"
            id={`task-title-edit-${task.id}`}
            value={editingTitle}
            onChange={(e) => setEditingTitle(e.target.value)}
            className="form-control w-full mb-2"
            placeholder="Task title"
            aria-label="Edit task title"
            disabled={loading}
          />
          <label htmlFor={`task-desc-edit-${task.id}`} className="sr-only">
            Task Description
          </label>
          <textarea
            id={`task-desc-edit-${task.id}`}
            value={editingDescription}
            onChange={(e) => setEditingDescription(e.target.value)}
            className="form-control w-full mb-2"
            placeholder="Task description (optional)"
            rows={2}
            aria-label="Edit task description"
            disabled={loading}
          />
          <div className="flex space-x-2">
            <button
              onClick={handleEdit}
              disabled={loading}
              className={`btn btn-success ${loading ? 'opacity-75' : ''}`}
              aria-label="Save task changes"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={loading}
              className={`btn btn-secondary ${loading ? 'opacity-75' : ''}`}
              aria-label="Cancel editing"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex-1">
          <div className="flex items-center">
            <input
              type="checkbox"
              id={`task-complete-${task.id}`}
              checked={task.completed}
              onChange={handleToggleComplete}
              disabled={loading}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded cursor-pointer"
              aria-describedby={`task-desc-${task.id}`}
              aria-label={`Mark task ${task.title} as ${task.completed ? 'incomplete' : 'complete'}`}
            />
            <label
              htmlFor={`task-complete-${task.id}`}
              id={`task-title-${task.id}`}
              className={`ml-3 block truncate ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'} flex-grow cursor-pointer`}
            >
              {task.title}
            </label>
            <div className="cursor-move opacity-40 hover:opacity-100 transition-opacity">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
              </svg>
            </div>
          </div>
          {task.description && (
            <p id={`task-desc-${task.id}`} className="ml-7 text-sm text-gray-500 mt-1">
              {task.description}
            </p>
          )}
          <p className="ml-7 text-xs text-gray-400 mt-1" aria-label={`Created on ${new Date(task.createdAt).toLocaleString()}`}>
            Created: {new Date(task.createdAt).toLocaleString()}
          </p>
        </div>
      )}

      {!isEditing && (
        <div className="flex space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className={`p-2 rounded-md text-gray-500 hover:text-gray-700 focus:outline-none ${loading ? 'opacity-50' : ''}`}
            aria-label={`Edit task: ${task.title}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
          <button
            onClick={handleDelete}
            disabled={loading}
            className={`p-2 rounded-md text-red-500 hover:text-red-700 focus:outline-none ${loading ? 'opacity-50' : ''}`}
            aria-label={`Delete task: ${task.title}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      )}
    </li>
  );
}