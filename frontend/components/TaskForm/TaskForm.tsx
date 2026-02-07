'use client';

import { useState } from 'react';
import { Task } from '@/types';
import apiClient from '@/lib/api';
import PrioritySelector from '@/components/PrioritySelector/PrioritySelector';
import TagsInput from '@/components/TagsInput/TagsInput';
import DatePicker from '@/components/DatePicker/DatePicker';
import ReminderPicker from '@/components/ReminderPicker/ReminderPicker';
import RecurrenceControls from '@/components/RecurrenceControls/RecurrenceControls';

interface TaskFormProps {
  userId: string;
  onTaskCreated?: (task: Task) => void; // Optional callback for when task is created
  onTaskChange?: () => void; // Callback to notify parent when tasks change
  initialTask?: Partial<Task>; // Optional initial task data for editing
}

export default function TaskForm({ userId, onTaskCreated, onTaskChange, initialTask }: TaskFormProps) {
  const [title, setTitle] = useState(initialTask?.title || '');
  const [description, setDescription] = useState(initialTask?.description || '');
  const [priority, setPriority] = useState(initialTask?.priority || 'medium');
  const [tags, setTags] = useState<string[]>(initialTask?.tags ? JSON.parse(initialTask.tags || '[]') : []);
  const [dueAt, setDueAt] = useState<Date | undefined>(initialTask?.due_at ? new Date(initialTask.due_at) : undefined);
  const [reminderAt, setReminderAt] = useState<Date | undefined>(initialTask?.reminder_at ? new Date(initialTask.reminder_at) : undefined);
  const [isRecurring, setIsRecurring] = useState(initialTask?.is_recurring || false);
  const [recurrenceRule, setRecurrenceRule] = useState(initialTask?.recurrence_rule || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      if (initialTask?.id) {
        // Update existing task
        const updatedTask = await apiClient.updateTaskExtended(userId, initialTask.id, {
          title,
          description,
          priority,
          tags: tags.length > 0 ? JSON.stringify(tags) : undefined,
          due_at: dueAt ? dueAt.toISOString() : undefined,
          reminder_at: reminderAt ? reminderAt.toISOString() : undefined,
          recurrence_rule: isRecurring ? recurrenceRule : undefined,
          is_recurring: isRecurring
        });

        if (onTaskCreated) {
          onTaskCreated(updatedTask);
        }
      } else {
        // Create new task
        const newTask = await apiClient.createTask(userId, {
          title,
          description,
          priority,
          tags: tags,
          due_at: dueAt ? dueAt.toISOString() : undefined,
          reminder_at: reminderAt ? reminderAt.toISOString() : undefined,
          recurrence_rule: isRecurring ? recurrenceRule : undefined,
          is_recurring: isRecurring
        });

        // Add a subtle success animation
        const form = document.querySelector('form');
        if (form) {
          form.classList.add('animate-pop');
          setTimeout(() => {
            if (form) form.classList.remove('animate-pop');
          }, 300);
        }

        // Call the optional callback
        if (onTaskCreated) {
          onTaskCreated(newTask);
        }
      }

      // Notify parent that tasks have changed
      if (onTaskChange) {
        onTaskChange();
      }

      // Reset form if creating new task (don't reset if editing)
      if (!initialTask?.id) {
        setTitle('');
        setDescription('');
        setPriority('medium');
        setTags([]);
        setDueAt(undefined);
        setReminderAt(undefined);
        setIsRecurring(false);
        setRecurrenceRule('');
      }
    } catch (err: any) {
      console.error('Error creating/updating task:', err);
      setError(err.message || 'Failed to create/update task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="card p-6 mb-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        {initialTask?.id ? 'Edit Task' : 'Create New Task'}
      </h3>

      {error && (
        <div className="mb-4 bg-red-50 border-l-4 border-red-500 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 10-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="md:col-span-2">
          <label htmlFor="title" className="form-label">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="form-control"
            placeholder="What needs to be done?"
            disabled={loading}
          />
        </div>

        <div className="md:col-span-2">
          <label htmlFor="description" className="form-label">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="form-control"
            placeholder="Add details..."
            rows={2}
            disabled={loading}
          />
        </div>

        {/* Priority */}
        <div>
          <label className="form-label">Priority</label>
          <PrioritySelector
            value={priority}
            onChange={setPriority}
            disabled={loading}
          />
        </div>

        {/* Tags */}
        <div>
          <label className="form-label">Tags</label>
          <TagsInput
            value={tags}
            onChange={setTags}
            placeholder="Add tags..."
            disabled={loading}
          />
        </div>

        {/* Due Date */}
        <div>
          <DatePicker
            label="Due Date"
            value={dueAt}
            onChange={(d) => setDueAt(d || undefined)}
            disabled={loading}
          />
        </div>

        {/* Reminder */}
        <div>
          <ReminderPicker
            label="Reminder Time"
            value={reminderAt}
            onChange={(d) => setReminderAt(d || undefined)}
            disabled={loading}
          />
        </div>

        {/* Recurrence Controls */}
        <div className="md:col-span-2">
          <RecurrenceControls
            isRecurring={isRecurring}
            recurrenceRule={recurrenceRule}
            onRecurringChange={setIsRecurring}
            onRuleChange={setRecurrenceRule}
            disabled={loading}
          />
        </div>
      </div>

      <div className="pt-4">
        <button
          type="submit"
          disabled={loading}
          className={`btn ${loading ? 'opacity-75 cursor-not-allowed' : ''}`}
        >
          {loading ? (
            <>
              <span className="spinner mr-2"></span>
              {initialTask?.id ? 'Updating Task...' : 'Creating Task...'}
            </>
          ) : (
            initialTask?.id ? 'Update Task' : 'Create Task'
          )}
        </button>
      </div>
    </form>
  );
}