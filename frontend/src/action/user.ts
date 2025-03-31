import { useQueryData } from "@/hooks/useQueryData";
import { useMutationData } from "@/hooks/useMutationData";
import axios from "axios";
import { LoginRequest, PasswordResetRequest, ResetPasswordRequest, LoginResponse, ApiResponse, User } from "@/types/index.types";

const API_URL = 'http://localhost:8000';  // Update to match your Django backend URL

// Create axios instance with default config
export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Login user
export const useLoginUser = (onSuccess?: () => void) => {
  return useMutationData<LoginResponse, LoginRequest>(
    ['login'],
    async (data: LoginRequest): Promise<ApiResponse<LoginResponse>> => {
      try {
        const response = await api.post<LoginResponse>('/authenticate/login/', data);

        // Store user info
        localStorage.setItem('user', JSON.stringify({
          id: Number(response.data.id),
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          gender: response.data.gender,
          email: response.data.email,
          year: response.data.year,
          dept: response.data.dept,
          roll_no: response.data.roll_no,
          phone_number: response.data.phone,
          parent_phone_number: response.data.phone, // Using same phone as parent phone for now
          is_active: response.data.is_active,
          is_staff: response.data.is_staff,
          is_superuser: response.data.is_superuser,
          date_joined: response.data.date_joined,
          last_login: response.data.last_login,
        }));

        return {
          status: response.status,
          data: response.data,
          user: {
            id: Number(response.data.id),
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            gender: response.data.gender,
            email: response.data.email,
            year: response.data.year,
            dept: response.data.dept,
            roll_no: response.data.roll_no,
            phone_number: response.data.phone,
            parent_phone_number: response.data.phone, // Using same phone as parent phone for now
            is_active: response.data.is_active,
            is_staff: response.data.is_staff,
            is_superuser: response.data.is_superuser,
            date_joined: response.data.date_joined,
            last_login: response.data.last_login,
          },
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          return {
            status: error.response.status,
            data: error.response.data.detail || 'Login failed',
            user: undefined,
          };
        }
        throw error;
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
        const response = await api.post('/authenticate/forgot_password/', data);
        return {
          status: response.status,
          data: response.data.detail || 'Password reset instructions sent successfully',
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          return {
            status: error.response.status,
            data: error.response.data.detail || 'Password reset request failed',
          };
        }
        throw error;
      }
    },
    undefined,
    onSuccess
  );
};

// Reset password
export const useResetPassword = (token: string, onSuccess?: () => void) => {
  return useMutationData<string, ResetPasswordRequest>(
    ['resetPassword', token],
    async (data: ResetPasswordRequest): Promise<ApiResponse<string>> => {
      try {
        const response = await api.get(`/authenticate/forgot_password/?email=${data.email}&token=${token}`);
        return {
          status: response.status,
          data: response.data.detail || 'Password reset successful',
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          return {
            status: error.response.status,
            data: error.response.data.detail || 'Password reset failed',
          };
        }
        throw error;
      }
    },
    undefined,
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
    async (): Promise<ApiResponse> => {
      try {
        const response = await api.post('/authenticate/logout/');

        // Clear localStorage
        localStorage.removeItem('user');

        return {
          status: response.status,
          data: response.data.detail,
        };
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          return {
            status: error.response.status,
            data: error.response.data.detail || 'Logout failed',
          };
        }
        throw error;
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
