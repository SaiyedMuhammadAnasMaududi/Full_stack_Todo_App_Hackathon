// User interface definition
export interface User {
  id: string;
  email: string;
  password?: string;
}

// Task interface definition
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

// Authentication response interface
export interface AuthResponse {
  user: User;
  token: string;
  refreshToken?: string;
}

// API error interface
export interface ApiError {
  message: string;
  status?: number;
  code?: string;
}

// Form validation errors interface
export interface FormErrors {
  [key: string]: string;
}

// Application state interface
export interface AppState {
  user: User | null;
  isAuthenticated: boolean;
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

// Password validation requirements
export interface PasswordRequirements {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecialChars: boolean;
}

// JWT token payload interface
export interface JwtPayload {
  userId: string;
  email: string;
  exp: number;
  iat: number;
}

// Task state interface for UI
export interface TaskState {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  editing: boolean;
  loading: boolean;
  error?: string;
}

// API configuration interface
export interface ApiConfig {
  baseUrl: string;
  timeout: number;
  headers: Record<string, string>;
}

// Response types for different API operations
export type GetTasksResponse = Task[];
export type CreateTaskResponse = Task;
export type UpdateTaskResponse = Task;
export type DeleteTaskResponse = void;
export type ToggleTaskCompletionResponse = Task;