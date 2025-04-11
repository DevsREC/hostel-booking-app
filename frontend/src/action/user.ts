import { useQueryData } from "@/hooks/useQueryData";
import { useMutationData } from "@/hooks/useMutationData";
import axios from "axios";
import { LoginRequest, PasswordResetRequest, ResetPasswordRequest, LoginResponse, ApiResponse, User } from "@/types/index.types";
import { QueryClient } from "@tanstack/react-query";

const API_URL = 'http://localhost:8000';

// Create a new instance of QueryClient
const queryClient = new QueryClient();

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Login user
export const useLoginUser = (onSuccess?: () => void) => {
  return useMutationData<LoginResponse | string, LoginRequest>(
    ['login'],
    async (data: LoginRequest): Promise<ApiResponse<LoginResponse | string>> => {
      try {
        const response = await api.post<LoginResponse>('/authenticate/login/', data);
        return {
          status: response.status,
          data: response.data,
          user: response.data.user,
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          const errorData = error.response.data;
          return {
            status: error.response.status,
            data: errorData.detail || 'Login failed',
            code: errorData.code,
            user: undefined,
          };
        }
        return {
          status: 500,
          data: 'An unexpected error occurred. Please try again.',
          code: 'server_error',
          user: undefined,
        };
      }
    },
    'currentUser',
    onSuccess
  );
};

// Request password reset
export const useRequestPasswordReset = (onSuccess?: () => void) => {
  return useMutationData<string, PasswordResetRequest>(
    ['requestPasswordReset'],
    async (data: PasswordResetRequest): Promise<ApiResponse<string>> => {
      try {
        const response = await api.post('/authenticate/forgot_password/', {
          email: data.email,
          password: data.password
        });
        return {
          status: response.status,
          data: response.data.detail || 'Password reset instructions sent successfully',
          code: response.data.code,
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          const errorData = error.response.data;
          return {
            status: error.response.status,
            data: errorData.detail || 'Password reset request failed',
            code: errorData.code,
          };
        }
        return {
          status: 500,
          data: 'An unexpected error occurred. Please try again.',
          code: 'server_error',
        };
      }
    },
    undefined,
    onSuccess
  );
};

// Reset password
export const useResetPassword = (onSuccess?: () => void) => {
  return useMutationData<string, ResetPasswordRequest>(
    ['resetPassword'],
    async (data: ResetPasswordRequest): Promise<ApiResponse<string>> => {
      try {
        const response = await api.get(`/authenticate/forgot_password/?email=${data.email}&token=${data.token}`);
        return {
          status: response.status,
          data: response.data.detail || 'Password reset successful',
          code: response.data.code,
          user: response.data.user,
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          const errorData = error.response.data;
          return {
            status: error.response.status,
            data: errorData.detail || 'Password reset failed',
            code: errorData.code,
          };
        }
        return {
          status: 500,
          data: 'An unexpected error occurred. Please try again.',
          code: 'server_error',
        };
      }
    },
    'currentUser',
    onSuccess
  );
};

// Check if user is logged in
export const useCurrentUser = () => {
  return useQueryData<User>(
    ['currentUser'],
    async () => {
      try {
        const response = await api.get('/authenticate/profile/');
        return response.data.data.user; // Extract user data from the new response structure
      } catch (error) {
        localStorage.removeItem('user');
        return null;
      }
    },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: false,
    }
  );
};

// Logout user
export const useLogout = (onSuccess?: () => void) => {
  return useMutationData<void, void>(
    ['logout'],
    async (): Promise<ApiResponse<void>> => {
      try {
        const response = await api.post('/authenticate/logout/');

        // Clear localStorage
        localStorage.removeItem('user');

        // Clear all query cache
        queryClient.clear();

        // Force reload to clear any remaining state
        window.location.href = '/auth/login';

        return {
          status: response.status,
          data: response.data.detail || 'Logged out successfully',
          code: 'logout_success'
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          const errorData = error.response.data;
          return {
            status: error.response.status,
            data: errorData.detail || 'Logout failed',
            code: errorData.code || 'logout_failed'
          };
        }
        return {
          status: 500,
          data: 'An unexpected error occurred during logout.',
          code: 'server_error'
        };
      }
    },
    'currentUser',
    onSuccess
  );
};

// Get user profile
export const useGetProfile = () => {
  return useQueryData<User | null>(
    ['profile'],
    async () => {
      try {
        const response = await api.get('/authenticate/profile/');
        return response.data.data.user; // Extract user data from the new response structure
      } catch (error) {
        // If unauthorized, clear auth data and return null
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          localStorage.removeItem('user');
          return null;
        }
        throw error;
      }
    },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: false,
    }
  );
};
