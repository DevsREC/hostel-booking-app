import { useGetProfile } from "@/action/user";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useGetUserBookings } from "@/action/hostel";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useNavigate, Link } from "react-router";
import { Separator } from "@/components/ui/separator";

export default function ProfilePage() {
    const { data: user, isLoading } = useGetProfile();
    const { data: bookings, isLoading: isLoadingBookings } = useGetUserBookings();
    const navigate = useNavigate();

    const hasActiveBooking = bookings?.some(booking =>
        booking.status === 'otp_pending' ||
        booking.status === 'payment_pending'
    );

    if (isLoading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <Card>
                    <CardHeader>
                        <Skeleton className="h-8 w-1/3" />
                        <Skeleton className="h-4 w-1/4" />
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="space-y-4">
                                <Skeleton className="h-4 w-full" />
                                <Skeleton className="h-4 w-2/3" />
                            </div>
                            <div className="space-y-4">
                                <Skeleton className="h-4 w-full" />
                                <Skeleton className="h-4 w-2/3" />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Profile Information */}
                <div className="lg:col-span-2 space-y-8">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-2xl">Personal Information</CardTitle>
                            <CardDescription>Your basic details and contact information</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Full Name</p>
                                    <p className="font-medium">{user?.first_name} {user?.last_name}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Email</p>
                                    <p className="font-medium">{user?.email}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Gender</p>
                                    <p className="font-medium">{user?.gender === 'M' ? 'Male' : 'Female'}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Phone Number</p>
                                    <p className="font-medium">{user?.phone_number}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Parent's Phone Number</p>
                                    <p className="font-medium">{user?.parent_phone_number}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-2xl">Academic Information</CardTitle>
                            <CardDescription>Your academic details and enrollment information</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Roll Number</p>
                                    <p className="font-medium">{user?.roll_no}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Department</p>
                                    <p className="font-medium">{user?.dept}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Year</p>
                                    <p className="font-medium">{user?.year}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-2xl">Account Status</CardTitle>
                            <CardDescription>Your account details and activity information</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Account Status</p>
                                    <Badge variant={user?.is_active ? "secondary" : "destructive"}>
                                        {user?.is_active ? "Active" : "Inactive"}
                                    </Badge>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Account Type</p>
                                    <Badge variant="outline">
                                        {user?.is_superuser ? "Admin" : user?.is_staff ? "Staff" : "Student"}
                                    </Badge>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Member Since</p>
                                    <p className="font-medium">{new Date(user?.date_joined || "").toLocaleDateString()}</p>
                                </div>
                                <div className="space-y-2">
                                    <p className="text-sm text-gray-500">Last Login</p>
                                    <p className="font-medium">{new Date(user?.last_login || "").toLocaleString()}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Bookings Section */}
                <div className="lg:col-span-1">
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-2xl">Your Bookings</CardTitle>
                            <CardDescription>View and manage your hostel bookings</CardDescription>
                            <Button
                                className="mt-4"
                                onClick={() => navigate("/hostels")}
                                disabled={hasActiveBooking}
                            >
                                {hasActiveBooking ? "Booking in Progress" : "Book a New Room"}
                            </Button>
                        </CardHeader>
                        <CardContent>
                            {isLoadingBookings ? (
                                <div className="space-y-4">
                                    <Skeleton className="h-24 w-full" />
                                    <Skeleton className="h-24 w-full" />
                                </div>
                            ) : bookings?.length === 0 ? (
                                <div className="text-center py-8 space-y-4">
                                    <div className="text-gray-400">
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                                        </svg>
                                    </div>
                                    <div>
                                        <p className="text-lg font-medium text-gray-900">No Bookings Yet</p>
                                        <p className="text-gray-500 mt-1">You haven't made any hostel bookings yet.</p>
                                        <p className="text-gray-500">Browse our available hostels and make your first booking!</p>
                                    </div>
                                    <Button
                                        variant="outline"
                                        onClick={() => navigate("/hostels")}
                                        className="mt-4"
                                    >
                                        Browse Hostels
                                    </Button>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {bookings?.map((booking) => (
                                        <Link
                                            key={booking.id}
                                            to={`/bookings/${booking.id}`}
                                            className="block border rounded-lg p-4 space-y-2 hover:bg-muted/50 transition-colors"
                                        >
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <h4 className="font-semibold">{booking.hostel.name}</h4>
                                                    <p className="text-sm text-gray-500">{booking.hostel.location}</p>
                                                </div>
                                                <Badge variant={
                                                    booking.status === 'otp_pending' ? 'outline' :
                                                        booking.status === 'payment_pending' ? 'secondary' :
                                                            booking.status === 'confirmed' ? 'default' :
                                                                'destructive'
                                                }>
                                                    {booking.status}
                                                </Badge>
                                            </div>
                                            <Separator />
                                            <div className="grid grid-cols-2 gap-2 text-sm">
                                                <div>
                                                    <p className="text-gray-500">Room Type</p>
                                                    <p className="font-medium">{booking.hostel.room_type}</p>
                                                </div>
                                                <div>
                                                    <p className="text-gray-500">Food Type</p>
                                                    <p className="font-medium">{booking.hostel.food_type}</p>
                                                </div>
                                                <div>
                                                    <p className="text-gray-500">Amount</p>
                                                    <p className="font-medium">₹{booking.hostel.amount}</p>
                                                </div>
                                                <div>
                                                    <p className="text-gray-500">Booked On</p>
                                                    <p className="font-medium">{new Date(booking.booked_at).toLocaleDateString()}</p>
                                                </div>
                                            </div>
                                        </Link>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}