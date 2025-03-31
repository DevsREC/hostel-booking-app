import {
    MutationFunction,
    MutationKey,
    useMutation,
    useMutationState,
    useQueryClient,
} from '@tanstack/react-query'
import { toast } from 'sonner'
import { ApiResponse } from "@/types/index.types"

export const useMutationData = <TData = any, TVariables = any>(
    queryKey: string[],
    mutationFn: (variables: TVariables) => Promise<ApiResponse<TData>>,
    invalidateKey?: string,
    onSuccess?: (response: ApiResponse<TData>) => void
) => {
    const queryClient = useQueryClient()

    return useMutation({
        mutationFn,
        onSuccess: (response) => {
            if (invalidateKey) {
                queryClient.invalidateQueries({ queryKey: [invalidateKey] })
            }
            onSuccess?.(response)
        },
    })
}

export const useMutationDataState = (mutationKey: MutationKey) => {
    const data = useMutationState({
        filters: { mutationKey },
        select: (mutation) => {
            return {
                variables: mutation.state.variables as any,
                status: mutation.state.status,
            }
        },
    })

    const latestVariables = data[data.length - 1]
    return { latestVariables }
}