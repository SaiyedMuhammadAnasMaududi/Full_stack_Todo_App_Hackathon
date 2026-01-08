import { jwtDecode } from 'jwt-decode';
import { User } from '../types';

// Define JWT token interface
interface JwtPayload {
  userId: string;
  email: string;
  exp: number;
  iat: number;
}

// Password validation utilities
class PasswordValidator {
  static validatePassword(password: string): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Check minimum length
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters');
    }

    // Check for uppercase letter
    if (!/(?=.*[A-Z])/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }

    // Check for lowercase letter
    if (!/(?=.*[a-z])/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }

    // Check for number
    if (!/(?=.*\d)/.test(password)) {
      errors.push('Password must contain at least one number');
    }

    // Check for special character
    if (!/(?=.*[@$!%*?&])/.test(password)) {
      errors.push('Password must contain at least one special character (@$!%*?&)');
    }

    return {
      isValid: errors.length === 0,
      errors,
    };
  }
}

// Authentication utilities class
class AuthUtils {
  private static readonly TOKEN_KEY = 'auth_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private static readonly TOKEN_EXPIRY_THRESHOLD = 5 * 60 * 1000; // 5 minutes in milliseconds

  // Store JWT token in localStorage
  static storeToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.TOKEN_KEY, token);
    }
  }

  // Store refresh token in localStorage
  static storeRefreshToken(refreshToken: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
    }
  }

  // Retrieve JWT token from localStorage
  static getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.TOKEN_KEY);
    }
    return null;
  }

  // Retrieve refresh token from localStorage
  static getRefreshToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(this.REFRESH_TOKEN_KEY);
    }
    return null;
  }

  // Remove tokens from localStorage
  static removeTokens(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(this.TOKEN_KEY);
      localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    }
  }

  // Decode JWT token to get user info
  static decodeToken(token: string): JwtPayload | null {
    try {
      return jwtDecode<JwtPayload>(token);
    } catch (error) {
      console.error('Error decoding JWT token:', error);
      return null;
    }
  }

  // Check if token is expired
  static isTokenExpired(token: string): boolean {
    const decoded = this.decodeToken(token);
    if (!decoded) return true;

    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
  }

  // Check if token expires within the threshold (5 minutes)
  static isTokenExpiringSoon(token: string): boolean {
    const decoded = this.decodeToken(token);
    if (!decoded) return true;

    const currentTime = Date.now() / 1000;
    const timeUntilExpiry = (decoded.exp - currentTime) * 1000; // Convert to milliseconds
    return timeUntilExpiry < this.TOKEN_EXPIRY_THRESHOLD;
  }

  // Get user info from token
  static getUserFromToken(): User | null {
    const token = this.getToken();
    if (!token || this.isTokenExpired(token)) {
      return null;
    }

    const decoded = this.decodeToken(token);
    if (!decoded) {
      return null;
    }

    return {
      id: decoded.userId,
      email: decoded.email,
    };
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    const token = this.getToken();
    return token !== null && !this.isTokenExpired(token);
  }

  // Proactively refresh JWT token before expiration
  static async refreshTokenIfNeeded(): Promise<boolean> {
    const token = this.getToken();
    if (!token) {
      return false;
    }

    if (this.isTokenExpiringSoon(token)) {
      // In a real implementation, you would call the backend to refresh the token
      // For now, we'll just return false to indicate that a refresh is needed
      console.log('Token needs to be refreshed');
      return false;
    }

    return true;
  }

  // Synchronize token across browser tabs
  static setupTokenSync(): void {
    if (typeof window !== 'undefined') {
      // Listen for storage events to sync logout across tabs
      window.addEventListener('storage', (event) => {
        if (event.key === this.TOKEN_KEY && event.newValue === null) {
          // Token was removed in another tab, logout this tab too
          window.location.href = '/login';
        }
      });
    }
  }

  // Log unauthorized access attempts for security monitoring
  static logUnauthorizedAccess(url: string, method: string): void {
    console.warn('Unauthorized access attempt detected', {
      url,
      method,
      timestamp: new Date().toISOString(),
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'unknown',
    });
  }

  // Initialize auth utilities
  static initialize(): void {
    this.setupTokenSync();
  }
}

// Initialize auth utilities when module loads
AuthUtils.initialize();

export default AuthUtils;
export { PasswordValidator };