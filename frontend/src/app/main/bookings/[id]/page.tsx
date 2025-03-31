import { useParams, Link } from "react-router";
import { useGetUserBookings } from "@/action/hostel";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Building2, Calendar, IndianRupee, Clock, User } from "lucide-react";

export default function BookingDetail() {
    const { id } = useParams();
    const { data: bookings, isLoading } = useGetUserBookings();

    if (isLoading) {
        return (
            <div className="container mx-auto px-4 py-8">
                <Card>
                    <CardHeader>
                        <Skeleton className="h-8 w-1/3" />
                        <Skeleton className="h-4 w-1/4 mt-2" />
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div>
                            <Skeleton className="h-4 w-1/4 mb-2" />
                            <Skeleton className="h-4 w-1/2" />
                        </div>
                        <div>
                            <Skeleton className="h-4 w-1/4 mb-2" />
                            <Skeleton className="h-4 w-1/2" />
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    const booking = bookings?.find((b) => b.id.toString() === id);

    if (!booking) {
        return (
            <div className="container mx-auto px-4 py-8">
                <Card>
                    <CardHeader>
                        <CardTitle>Booking Not Found</CardTitle>
                        <CardDescription>
                            The booking you're looking for doesn't exist or you don't have access to it.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Link to="/bookings" className="text-primary hover:underline">
                            Back to Bookings
                        </Link>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex items-center gap-4 mb-6">
                <Link
                    to="/bookings"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                >
                    ← Back to Bookings
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex justify-between items-start">
                        <div>
                            <CardTitle className="text-2xl">Booking Details</CardTitle>
                            <CardDescription className="mt-2">
                                Booking ID: {booking.id}
                            </CardDescription>
                        </div>
                        <Badge
                            variant={
                                booking.status === 'otp_pending' ? 'outline' :
                                    booking.status === 'payment_pending' ? 'secondary' :
                                        booking.status === 'confirmed' ? 'default' :
                                            'destructive'
                            }
                            className="capitalize"
                        >
                            {booking.status}
                        </Badge>
                    </div>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Hostel Information */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold">Hostel Information</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Building2 className="h-4 w-4" />
                                    <span className="text-sm">Hostel Name</span>
                                </div>
                                <p className="font-medium">{booking.hostel.name}</p>
                            </div>
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Building2 className="h-4 w-4" />
                                    <span className="text-sm">Location</span>
                                </div>
                                <p className="font-medium">{booking.hostel.location}</p>
                            </div>
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Building2 className="h-4 w-4" />
                                    <span className="text-sm">Room Type</span>
                                </div>
                                <p className="font-medium">{booking.hostel.room_type}</p>
                            </div>
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Building2 className="h-4 w-4" />
                                    <span className="text-sm">Food Type</span>
                                </div>
                                <p className="font-medium">{booking.hostel.food_type}</p>
                            </div>
                        </div>
                    </div>

                    <Separator />

                    {/* Payment Information */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold">Payment Information</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <IndianRupee className="h-4 w-4" />
                                    <span className="text-sm">Annual Amount</span>
                                </div>
                                <p className="font-medium text-xl text-primary">₹{booking.hostel.amount * 12}</p>
                            </div>
                            {booking.payment_link && booking.status === 'payment_pending' && (
                                <div className="space-y-2">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <IndianRupee className="h-4 w-4" />
                                        <span className="text-sm">Payment Link</span>
                                    </div>
                                    <div className="space-y-2">
                                        <a
                                            href={booking.payment_link}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-blue-500 hover:underline inline-block"
                                        >
                                            Click here to pay
                                        </a>
                                        {booking.payment_expiry && (
                                            <p className="text-sm text-yellow-600">
                                                Complete payment before: {new Date(booking.payment_expiry).toLocaleString()}
                                            </p>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    <Separator />

                    {/* Booking Timeline */}
                    <div className="space-y-4">
                        <h3 className="text-lg font-semibold">Booking Timeline</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Clock className="h-4 w-4" />
                                    <span className="text-sm">Booked On</span>
                                </div>
                                <p className="font-medium">
                                    {new Date(booking.booked_at).toLocaleString()}
                                </p>
                            </div>
                            {booking.otp_verified_at && (
                                <div className="space-y-2">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <User className="h-4 w-4" />
                                        <span className="text-sm">OTP Verified</span>
                                    </div>
                                    <p className="font-medium">
                                        {new Date(booking.otp_verified_at).toLocaleString()}
                                    </p>
                                </div>
                            )}
                            {booking.payment_completed_at && (
                                <div className="space-y-2">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <IndianRupee className="h-4 w-4" />
                                        <span className="text-sm">Payment Completed</span>
                                    </div>
                                    <p className="font-medium">
                                        {new Date(booking.payment_completed_at).toLocaleString()}
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="flex justify-end mt-6">
                        <Link
                            to={`/hostels/${booking.hostel.id}`}
                            className="text-primary hover:underline"
                        >
                            View Hostel Details
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
} 