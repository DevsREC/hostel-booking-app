import { QueryKey, useQuery, UseQueryOptions } from '@tanstack/react-query'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
})

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export const useQueryData = <TData = any>(
    queryKey: QueryKey,
    queryFn: () => Promise<TData | null>,
    options?: Omit<UseQueryOptions<TData | null, Error>, 'queryKey' | 'queryFn'>
) => {
    return useQuery<TData | null, Error>({
        queryKey,
        queryFn,
        ...options,
    })
}