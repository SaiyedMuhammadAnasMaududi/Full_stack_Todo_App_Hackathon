import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import AuthUtils from './auth';

// Define TypeScript interfaces for our API entities
export interface User {
  id: string;
  email: string;
  password?: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
  priority?: string; // low, medium, high
  tags?: string; // JSON string of tags array
  due_at?: string; // ISO date string
  reminder_at?: string; // ISO date string
  recurrence_rule?: string; // RRULE string for recurrence
  is_recurring?: boolean;
  parent_task_id?: string; // ID of parent task for recurring instances
  completed_at?: string; // Completion timestamp
}

// Create the base API instance
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include JWT token
    this.client.interceptors.request.use(
      (config) => {
        const token = AuthUtils.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle 401 errors and automatic logout
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Log unauthorized access attempts for security monitoring
          console.warn('Unauthorized access attempt detected', {
            url: error.config?.url,
            method: error.config?.method,
            timestamp: new Date().toISOString(),
          });

          // Clear token from both ApiClient and AuthUtils
          AuthUtils.removeTokens(); // Clear tokens from localStorage
        }
        return Promise.reject(error);
      }
    );
  }

  // Enhanced methods for JWT token handling
  async ensureTokenValid(): Promise<boolean> {
    const token = AuthUtils.getToken();
    if (!token) {
      return false;
    }

    // Check if token is expired
    try {
      const payload = this.decodeToken(token);
      if (!payload) return false;

      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp > currentTime;
    } catch (error) {
      console.error('Error validating token:', error);
      return false;
    }
  }

  // Decode JWT token
  private decodeToken(token: string): { exp: number } | null {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );

      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  }

  // Set the JWT token for API requests
  setToken(token: string): void {
    // Token is managed by AuthUtils, so we don't need to store it locally
    // The interceptor will pick it up from AuthUtils.getToken()
  }

  // Retry mechanism with exponential backoff for network failures
  async retryWithBackoff<T>(
    operation: () => Promise<T>,
    maxRetries: number = 3,
    baseDelay: number = 1000
  ): Promise<T> {
    let lastError: any;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error: any) {
        lastError = error;

        // If it's a 401 error, don't retry, just clear token
        if (error.response?.status === 401) {
          AuthUtils.removeTokens(); // Clear tokens from localStorage
          throw error;
        }

        // If it's the last attempt, throw the error
        if (attempt === maxRetries) {
          break;
        }

        // Calculate delay with exponential backoff and jitter
        const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;

        console.warn(`Request failed, retrying in ${delay}ms... (attempt ${attempt + 1}/${maxRetries + 1})`, error);

        // Wait for the calculated delay
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    // Throw the last error if all retries failed
    throw lastError;
  }

  // Wrapper methods that include retry logic
  async getTasksWithRetry(userId: string): Promise<Task[]> {
    return this.retryWithBackoff(async () => {
      const response = await this.client.get(`/api/${userId}/tasks`);
      return response.data;
    });
  }

  async createTaskWithRetry(userId: string, title: string, description?: string): Promise<Task> {
    return this.retryWithBackoff(async () => {
      const response = await this.client.post(`/api/${userId}/tasks`, { title, description });
      return response.data;
    });
  }

  async updateTaskWithRetry(userId: string, taskId: string, updates: Partial<Task>): Promise<Task> {
    return this.retryWithBackoff(async () => {
      const response = await this.client.put(`/api/${userId}/tasks/${taskId}`, updates);
      return response.data;
    });
  }

  async deleteTaskWithRetry(userId: string, taskId: string): Promise<void> {
    return this.retryWithBackoff(async () => {
      await this.client.delete(`/api/${userId}/tasks/${taskId}`);
    });
  }

  async toggleTaskCompletionWithRetry(userId: string, taskId: string, completed: boolean): Promise<Task> {
    return this.retryWithBackoff(async () => {
      const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/complete`, {
        completed: completed
      });
      return response.data;
    });
  }

  // Authentication endpoints
  async signup(email: string, password: string): Promise<{ token: string; refreshToken?: string }> {
    const response = await this.client.post('/api/auth/register', { email, password });
    return {
      token: response.data.access_token,
      refreshToken: undefined // Backend doesn't return refresh token currently
    };
  }

  async login(email: string, password: string): Promise<{ token: string; refreshToken?: string }> {
    const response = await this.client.post('/api/auth/login', { email, password });
    return {
      token: response.data.access_token,
      refreshToken: undefined // Backend doesn't return refresh token currently
    };
  }


  // Task endpoints
  async getTasks(userId: string): Promise<Task[]> {
    const response = await this.client.get(`/api/${userId}/tasks`);
    return response.data;
  }

  // Create task with advanced features
  async createTask(userId: string, taskData: {
    title: string;
    description?: string;
    priority?: string;
    tags?: string[];
    due_at?: string;
    reminder_at?: string;
    recurrence_rule?: string;
    is_recurring?: boolean
  }): Promise<Task> {
    const response = await this.client.post(`/api/${userId}/tasks`, taskData);
    return response.data;
  }

  // Update task with all advanced features
  async updateTaskExtended(userId: string, taskId: string, updates: Partial<Task>): Promise<Task> {
    const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/update`, updates);
    return response.data;
  }

  // Legacy updateTask method (to maintain backward compatibility)
  async updateTask(userId: string, taskId: string, updates: Partial<Task>): Promise<Task> {
    const response = await this.client.put(`/api/${userId}/tasks/${taskId}`, updates);
    return response.data;
  }

  async deleteTask(userId: string, taskId: string): Promise<void> {
    await this.client.delete(`/api/${userId}/tasks/${taskId}`);
  }

  async toggleTaskCompletion(userId: string, taskId: string, completed: boolean): Promise<Task> {
    const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/complete`, {
      completed: completed
    });
    return response.data;
  }

  // Advanced feature methods
  async searchTasks(userId: string, query: string, limit: number = 20): Promise<Task[]> {
    const response = await this.client.post(`/api/${userId}/tasks/search`, {
      query,
      limit
    });
    return response.data;
  }

  async filterTasks(userId: string, filters: {
    priority?: string;
    completed?: boolean;
    due_after?: string;
    due_before?: string;
    tags?: string[];
    limit?: number
  }): Promise<Task[]> {
    const response = await this.client.post(`/api/${userId}/tasks/filter`, filters);
    return response.data;
  }

  async sortTasks(userId: string, sortField: string = "created_at", sortOrder: string = "asc", limit: number = 20): Promise<Task[]> {
    const response = await this.client.post(`/api/${userId}/tasks/sort`, {
      sort_field: sortField,
      sort_order: sortOrder,
      limit
    });
    return response.data;
  }

  async setTaskPriority(userId: string, taskId: string, priority: string): Promise<Task> {
    const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/update`, {
      priority
    });
    return response.data;
  }

  async setTaskDueDate(userId: string, taskId: string, dueDate: string): Promise<Task> {
    const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/update`, {
      due_at: dueDate
    });
    return response.data;
  }

  async setTaskReminder(userId: string, taskId: string, reminderTime: string): Promise<Task> {
    const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/update`, {
      reminder_at: reminderTime
    });
    return response.data;
  }

  async setTaskRecurrence(userId: string, taskId: string, recurrenceRule: string, isRecurring: boolean): Promise<Task> {
    const response = await this.client.patch(`/api/${userId}/tasks/${taskId}/update`, {
      recurrence_rule: recurrenceRule,
      is_recurring: isRecurring
    });
    return response.data;
  }

  // Chat endpoints
  async getConversations(userId: string): Promise<any> {
    const response = await this.client.get(`/api/${userId}/conversations`);
    return response.data;
  }

  async getConversation(userId: string, conversationId: number): Promise<any> {
    const response = await this.client.get(`/api/${userId}/conversations/${conversationId}`);
    return response.data;
  }

  async sendChatMessage(userId: string, message: string, conversationId?: number): Promise<any> {
    const requestBody: any = { message };
    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }
    const response = await this.client.post(`/api/${userId}/chat`, requestBody);
    return response.data;
  }

  // Generic request method for flexibility
  async request<T>(config: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.request<T>(config);
  }
}

// Create a singleton instance
export const apiClient = new ApiClient();

// Export for use in components
export default apiClient;