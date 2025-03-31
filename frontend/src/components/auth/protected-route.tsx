import { Navigate, useLocation } from 'react-router';
import { useGetProfile } from '@/action/user';
import { Skeleton } from '@/components/ui/skeleton';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const { data: user, isLoading } = useGetProfile();
    const location = useLocation();

    if (isLoading) {
        return (
            <div className="p-4">
                <Skeleton className="h-8 w-1/3 mb-4" />
                <Skeleton className="h-4 w-1/4" />
            </div>
        );
    }

    if (!user) {
        // Redirect to login page but save the attempted location
        return <Navigate to="/auth/login" state={{ from: location }} replace />;
    }

    return <>{children}</>;
};

export const PublicOnlyRoute = ({ children }: ProtectedRouteProps) => {
    const { data: user, isLoading } = useGetProfile();
    const location = useLocation();

    if (isLoading) {
        return (
            <div className="p-4">
                <Skeleton className="h-8 w-1/3 mb-4" />
                <Skeleton className="h-4 w-1/4" />
            </div>
        );
    }

    if (user) {
        // Redirect to dashboard if user is already logged in
        return <Navigate to="/" replace />;
    }

    return <>{children}</>;
}; 