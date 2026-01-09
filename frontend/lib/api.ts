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

  async createTask(userId: string, title: string, description?: string): Promise<Task> {
    const response = await this.client.post(`/api/${userId}/tasks`, { title, description });
    return response.data;
  }

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

  // Generic request method for flexibility
  async request<T>(config: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.request<T>(config);
  }
}

// Create a singleton instance
export const apiClient = new ApiClient();

// Export for use in components
export default apiClient;