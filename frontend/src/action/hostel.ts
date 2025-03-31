import { useQueryData } from "@/hooks/useQueryData";
import { useMutationData } from "@/hooks/useMutationData";
import { Hostel, Room, Booking, HostelResponse, RoomResponse, BookingResponse, ApiResponse } from "@/types/index.types";
import { api } from "./user";
import { useCurrentUser } from "./user";
import axios from "axios";

// Get all hostels
export const useGetHostels = () => {
    const { data: currentUser } = useCurrentUser();

    return useQueryData<Hostel[]>(
        ['hostels'],
        async () => {
            const response = await api.get<HostelResponse>('/hostel/');
            // Filter hostels based on user's gender
            return response.data.data.filter(hostel => hostel.gender === currentUser?.gender);
        }
    );
};

// Get hostel by ID (filter from the list of all hostels)
export const useGetHostelById = (id: string) => {
    return useQueryData<Hostel>(
        ['hostel', id],
        async () => {
            const response = await api.get<HostelResponse>('/hostel/');
            const hostel = response.data.data.find(h => h.id === parseInt(id));
            if (!hostel) {
                throw new Error('Hostel not found');
            }
            return hostel;
        }
    );
};

// Get rooms by hostel ID (filter from the hostel data)
export const useGetRoomsByHostel = (hostelId: string) => {
    return useQueryData<Room[]>(
        ['rooms', hostelId],
        async () => {
            const response = await api.get<HostelResponse>('/hostel/');
            const hostel = response.data.data.find(h => h.id === parseInt(hostelId));
            if (!hostel) {
                throw new Error('Hostel not found');
            }
            // Since the backend doesn't have a separate rooms endpoint,
            // we'll create a room object from the hostel data
            return [{
                id: hostel.id,
                hostel: hostel.id,
                room_number: '1', // Default room number since we don't have room numbers
                floor: 1, // Default floor since we don't have floor information
                capacity: hostel.person_per_room,
                occupied: 0, // We don't have this information
                price: hostel.amount,
                is_available: hostel.available_rooms > 0,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
            }];
        }
    );
};

// Create booking
export const useCreateBooking = (onSuccess?: (response: ApiResponse<{ booking_id?: string; message?: string }>) => void) => {
    return useMutationData<{ booking_id?: string; message?: string }, { hostel: number }>(
        ['createBooking'],
        async (data: { hostel: number }): Promise<ApiResponse<{ booking_id?: string; message?: string }>> => {
            try {
                const response = await api.post<{ booking_id?: string; message?: string }>(`/hostel/book/${data.hostel}/`, data);
                return {
                    status: response.status,
                    data: response.data,
                    code: 'booking_success'
                };
            } catch (error) {
                if (axios.isAxiosError(error) && error.response) {
                    const errorData = error.response.data;
                    return {
                        status: error.response.status,
                        data: errorData.detail || 'Booking failed',
                        code: errorData.code || 'booking_failed'
                    };
                }
                return {
                    status: 500,
                    data: 'An unexpected error occurred during booking.',
                    code: 'server_error'
                };
            }
        },
        'bookings',
        onSuccess
    );
};

// Get user's bookings
export const useGetUserBookings = () => {
    return useQueryData<Booking[]>(
        ['userBookings'],
        async () => {
            const response = await api.get<BookingResponse>('/hostel/bookings/');
            return response.data.data;
        }
    );
};

// Cancel booking
export const useCancelBooking = (onSuccess?: () => void) => {
    return useMutationData<Booking, string>(
        ['cancelBooking'],
        async (bookingId: string): Promise<ApiResponse<Booking>> => {
            try {
                const response = await api.delete<Booking>('/hostel/booking/', {
                    data: { booking_id: bookingId }
                });
                return {
                    status: response.status,
                    data: response.data,
                    code: 'cancel_success'
                };
            } catch (error) {
                if (axios.isAxiosError(error) && error.response) {
                    const errorData = error.response.data;
                    return {
                        status: error.response.status,
                        data: errorData.detail || 'Cancellation failed',
                        code: errorData.code || 'cancel_failed'
                    };
                }
                return {
                    status: 500,
                    data: 'An unexpected error occurred during cancellation.',
                    code: 'server_error'
                };
            }
        },
        'userBookings',
        onSuccess
    );
}; 