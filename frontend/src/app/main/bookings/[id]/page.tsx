import { useParams, Link, useNavigate } from "react-router";
import { useGetUserBookings, useCancelBooking } from "@/action/hostel";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Building2,
  IndianRupee,
  Clock,
  User,
  XCircle,
  VerifiedIcon,
  AlertCircle,
  MapPin,
  BedDouble,
  Utensils,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useState } from "react";
import { toast } from "sonner";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";
import { api } from "@/action/user";

export default function BookingDetail() {
  const { id } = useParams();
  const { data: bookings, isLoading } = useGetUserBookings();
  const { mutate: cancelBooking } = useCancelBooking();
  const [showCancelDialog, setShowCancelDialog] = useState(false);
  const [showOTPDialog, setShowOTPDialog] = useState(false);
  const [otp, setOtp] = useState("");
  const [isVerifyingOTP, setIsVerifyingOTP] = useState(false);
  const navigate = useNavigate();
  console.log(bookings)
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch (error) {
      return "Invalid Date";
    }
  };
  const handleOTPVerification = async () => {
    if (!id || !otp) return;

    setIsVerifyingOTP(true);
    try {
      const response = await api.post("/hostel/verify_otp/", {
        booking_id: id,
        otp_code: otp,
      });

      if (response.status === 200) {
        const { payment_link, payment_instructions, expires_at } =
          response.data;
        toast.success("OTP verified successfully!");
        setShowOTPDialog(false);

        // Show payment instructions in a success toast
        toast.success(
          <div className="space-y-2">
            <p className="font-medium">Payment Instructions:</p>
            <p>{payment_instructions}</p>
            <p className="text-sm text-muted">
              Payment link has been sent to your email.
            </p>
            <p className="text-sm text-yellow-600">
              Complete payment before: {formatDate(expires_at)}
            </p>
          </div>,
          {
            duration: 10000, // Show for 10 seconds
          }
        );

        // navigate(`/bookings/${bookingId}`);
      }
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.message || "Invalid/OTP Expired";
      toast.error(errorMessage);

      // If OTP is expired, close the dialog and redirect to bookings
      if (errorMessage.includes("expired")) {
        setShowOTPDialog(false);
        navigate("/bookings");
      }
    } finally {
      setIsVerifyingOTP(false);
    }
  };

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
              The booking you're looking for doesn't exist or you don't have
              access to it.
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

  const handleCancelBooking = () => {
    setShowCancelDialog(true);
  };

  const confirmCancelBooking = () => {
    if (!id) return;
    cancelBooking(id, {
      onSuccess: () => {
        toast.success("Booking cancelled successfully");
        setShowCancelDialog(false);
      },
      onError: (error) => {
        toast.error(error.message || "Failed to cancel booking");
      },
    });
  };

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
                booking.status === "otp_pending"
                  ? "outline"
                  : booking.status === "payment_pending"
                    ? "secondary"
                    : booking.status === "confirmed"
                      ? "default"
                      : "destructive"
              }
              className="capitalize"
            >
              {booking.status === "otp_pending"
                ? "OTP Verification Pending"
                : booking.status === "payment_pending"
                  ? "Payment Pending"
                  : booking.status === "confirmed"
                    ? "Confirmed"
                    : booking.status === "payment_not_done"
                      ? "Payment Not Done"
                      : "Canceled"}
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
                  <MapPin className="h-4 w-4" />
                  <span className="text-sm">Location</span>
                </div>
                <p className="font-medium">{booking.hostel.location}</p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <BedDouble className="h-4 w-4" />
                  <span className="text-sm">Room Type</span>
                </div>
                <p className="font-medium">{booking.hostel.room_type}</p>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Utensils className="h-4 w-4" />
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
                  <span className="text-sm">Total Fees</span>
                </div>
                <p className="font-medium text-xl text-primary">
                  ₹{booking.hostel.amount}
                </p>
              </div>
              {booking.payment_link && booking.status === "payment_pending" && (
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
                        Complete payment before:{" "}
                        {new Date(booking.payment_expiry).toLocaleString()}
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
                  <span className="text-sm">Booked At</span>
                </div>
                <p className="font-medium">{formatDate(booking.booked_at)}</p>
              </div>
              {booking.payment_expiry && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Clock className="h-4 w-4" />
                    <span className="text-sm">Payment Due By</span>
                  </div>
                  <p className="font-medium">{formatDate(booking.payment_expiry)}</p>
                </div>
              )}
              {booking.payment_completed_at && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <VerifiedIcon className="h-4 w-4" />
                    <span className="text-sm">Payment Completed At</span>
                  </div>
                  <p className="font-medium">{formatDate(booking.payment_completed_at)}</p>
                </div>
              )}
            </div>
          </div>

          <div className="flex justify-between items-center mt-6">
            <Link
              to={`/hostels/${booking.hostel.id}`}
              className="text-primary hover:underline"
            >
              View Hostel Details
            </Link>
            {booking.status === "otp_pending" ? (
              <div className="flex justify-end gap-2 flex-wrap">
                <Dialog open={showOTPDialog} onOpenChange={setShowOTPDialog}>
                  <DialogTrigger>
                    <Button
                      variant="default"
                      className="flex items-center gap-2"
                    >
                      <VerifiedIcon className="h-4 w-4" />
                      Verify OTP
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-primary">
                        Verify OTP
                      </DialogTitle>
                      <DialogDescription className="text-base">
                        Please enter the 6-digit OTP sent to your email address
                        to confirm your booking.
                      </DialogDescription>
                    </DialogHeader>
                    <div className="py-4">
                      <div className="space-y-4">
                        <div className="bg-muted/50 p-4 rounded-lg space-y-2">
                          <p className="font-medium">
                            Hostel: {booking.hostel?.name}
                          </p>
                          <p className="font-medium">
                            Room Type: {booking.hostel?.room_type}
                          </p>
                          <p className="font-medium text-primary text-xl">
                            Total Fees: ₹{booking.hostel?.amount || 0}
                          </p>
                        </div>
                        <InputOTP
                          maxLength={6}
                          value={otp}
                          onChange={(value) => setOtp(value)}
                        >
                          <InputOTPGroup>
                            <InputOTPSlot index={0} />
                            <InputOTPSlot index={1} />
                            <InputOTPSlot index={2} />
                            <InputOTPSlot index={3} />
                            <InputOTPSlot index={4} />
                            <InputOTPSlot index={5} />
                          </InputOTPGroup>
                        </InputOTP>
                        <div className="flex items-center gap-2 text-yellow-600 bg-yellow-50 p-3 rounded-lg">
                          <AlertCircle className="h-5 w-5" />
                          <p className="text-sm">
                            The OTP will expire in 10 minutes. Please complete
                            the payment within 5 Days after verification.
                          </p>
                        </div>
                      </div>
                    </div>
                    <DialogFooter>
                      <Button
                        variant="outline"
                        onClick={() => setShowOTPDialog(false)}
                      >
                        Cancel
                      </Button>
                      <Button
                        onClick={handleOTPVerification}
                        disabled={isVerifyingOTP || otp.length !== 6}
                        className="bg-primary hover:bg-primary/90"
                      >
                        {isVerifyingOTP ? "Verifying..." : "Verify OTP"}
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
                <Button
                  variant="destructive"
                  onClick={handleCancelBooking}
                  className="flex items-center gap-2"
                >
                  <XCircle className="h-4 w-4" />
                  Cancel Booking
                </Button>
              </div>
            ) : booking.status === "payment_pending" ? (
              <></>
            ) : booking.status === "payment_not_done" ? (
              <></>
            ) : (
              <></>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Cancel Confirmation Dialog */}
      <Dialog open={showCancelDialog} onOpenChange={setShowCancelDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Cancel Booking</DialogTitle>
            <DialogDescription>
              Are you sure you want to cancel this booking? This action cannot
              be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowCancelDialog(false)}
            >
              No, Keep Booking
            </Button>
            <Button variant="destructive" onClick={confirmCancelBooking}>
              Yes, Cancel Booking
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
