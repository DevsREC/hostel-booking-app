export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  year: number;
  dept: string;
  roll_no: string;
  phone_number: string;
  parent_phone_number: string;
  gender: 'M' | 'F';
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  date_joined: string;
  last_login: string | null;
}

// Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface PasswordResetRequest {
  email: string;
  password: string;
}

export interface ResetPasswordRequest {
  email: string;
  token: string;
}

export interface ApiResponse<T = any> {
  status: number;
  data: T | string;
  code?: string;
  user?: User;
}

export interface LoginResponse {
  id: number;
  first_name: string;
  last_name: string;
  gender: string;
  email: string;
  year: string;
  dept: string;
  roll_no: string;
  phone: string;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  date_joined: string;
  last_login: string;
  user?: User;
}

export interface Hostel {
  id: number;
  name: string;
  location: string;
  room_type: 'AC' | 'NON-AC';
  bathroom_type: 'Attached' | 'Common';
  food_type: 'Veg' | 'Non-veg';
  gender: 'M' | 'F';
  person_per_room: number;
  no_of_rooms: number;
  total_capacity: number;
  room_description: string;
  amount: number;
  image: string;
  available_rooms: number;
}

export interface Room {
  id: number;
  hostel: number;
  room_number: string;
  floor: number;
  capacity: number;
  occupied: number;
  price: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface Booking {
  id: string;
  user: User;
  hostel: Hostel;
  status: 'otp_pending' | 'payment_pending' | 'confirmed' | 'cancelled';
  booked_at: string;
  otp_verified_at: string | null;
  payment_completed_at: string | null;
  payment_link: string | null;
  payment_reference: string | null;
  otp_code: string | null;
  otp_expiry: string | null;
  payment_expiry: string | null;
  admin_notes: string | null;
  verified_by: User | null;
}

export interface HostelResponse {
  status: number;
  data: Hostel[];
}

export interface RoomResponse {
  status: number;
  data: Room[];
}

export interface BookingResponse {
  status: number;
  data: Booking[];
}
