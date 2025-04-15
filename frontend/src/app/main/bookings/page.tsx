import { useGetUserBookings } from "@/action/hostel";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useNavigate, Link } from "react-router";
import { Badge } from "@/components/ui/badge";
import { Building2, IndianRupee } from "lucide-react";

export default function BookingsPage() {
  const navigate = useNavigate();
  const { data: bookings, isLoading } = useGetUserBookings();
  console.log(bookings)

  const hasActiveBooking = bookings?.some(
    (booking) =>
      booking.status === "otp_pending" || booking.status === "payment_pending"
  );

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

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-10 w-32" />
        </div>
        <div className="space-y-6">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="overflow-hidden">
              <CardHeader>
                <Skeleton className="h-6 w-1/3" />
                <Skeleton className="h-4 w-1/4 mt-2" />
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-2/3" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-foreground">Your Bookings</h1>
        <Button
          onClick={() => navigate("/")}
          disabled={hasActiveBooking}
          className="bg-primary text-primary-foreground hover:bg-primary/90"
        >
          {hasActiveBooking ? "Booking in Progress" : "Book a New Room"}
        </Button>
      </div>

      {!bookings || bookings.length === 0 ? (
        <Card className="p-8 bg-card">
          <div className="flex flex-col items-center justify-center text-center space-y-4">
            <Building2 className="h-12 w-12 text-muted-foreground" />
            <h2 className="text-2xl font-semibold text-card-foreground">
              No Bookings Found
            </h2>
            <p className="text-muted-foreground max-w-sm">
              You haven't made any bookings yet. Browse our available hostels
              and find the perfect room for you.
            </p>
            <div className="flex gap-4 mt-4">
              <Button
                onClick={() => navigate("/")}
                disabled={hasActiveBooking}
                className="bg-primary text-primary-foreground hover:bg-primary/90"
              >
                Browse Hostels
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate("/profile")}
                disabled={hasActiveBooking}
                className="border-input hover:bg-accent hover:text-accent-foreground"
              >
                View Profile
              </Button>
            </div>
          </div>
        </Card>
      ) : (
        <div className="space-y-6">
          {bookings.map((booking) => (
            <Card key={booking.id} className="w-full bg-card">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-card-foreground">
                      Booking #{booking.id}
                    </CardTitle>
                    <CardDescription className="text-muted-foreground">
                      Booked on {formatDate(booking.booked_at)}
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
              <CardContent>
                <div className="grid gap-4">
                  <div className="flex items-center gap-4">
                    <Building2 className="h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-card-foreground">
                        {booking.hostel.name}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {booking.hostel.location}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <IndianRupee className="h-5 w-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium text-card-foreground">
                        ₹{booking.food_type === "Veg" 
                          ? booking.hostel.amount.Mgmt_veg 
                          : booking.hostel.amount.Mgmt_non_veg}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Total Fees ({booking.food_type === "Veg" ? "Vegetarian" : "Non-Vegetarian"})
                      </p>
                    </div>
                  </div>
                  {booking.status === "payment_pending" && booking.payment_expiry && (
                    <div className="flex items-center gap-4">
                      <div>
                        <p className="font-medium text-card-foreground">
                          Payment Due: {formatDate(booking.payment_expiry)}
                        </p>
                        <p className="text-sm text-muted-foreground">
                          Complete payment before expiry
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
              <CardFooter className="flex justify-between items-center">
                <div className="flex gap-4">
                  <Link
                    to={`/hostels/${booking.hostel.id}`}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    View Hostel
                  </Link>
                  <Link
                    to={`/bookings/${booking.id}`}
                    className="text-sm text-primary hover:text-primary/80 transition-colors"
                  >
                    View Booking Details →
                  </Link>
                </div>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
