import { useParams } from "react-router";
import { useGetHostelById, useCreateBooking, useGetUserBookings } from "@/action/hostel";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useNavigate } from "react-router";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Building2, MapPin, Users, Utensils, User2, BedDouble, AlertCircle, Bath } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useState, useEffect } from "react";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp";
import { api } from "@/action/user";
import { toast } from "sonner";
import { ScrollArea } from "@/components/ui/scroll-area";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

interface BookingResponse {
    booking_id?: string;
    message?: string;
    data?: string
}

export default function HostelDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [showConfirmDialog, setShowConfirmDialog] = useState(false);
    const [showOTPDialog, setShowOTPDialog] = useState(false);
    const [otp, setOtp] = useState("");
    const [bookingId, setBookingId] = useState<string | null>(null);
    const [isVerifyingOTP, setIsVerifyingOTP] = useState(false);
    const [selectedFoodType, setSelectedFoodType] = useState<"veg" | "non_veg">("veg");

    const { data: hostel, isLoading: isLoadingHostel } = useGetHostelById(id || "");
    const { data: userBookings } = useGetUserBookings();

    // Set default food type based on available options
    useEffect(() => {
        if (hostel) {
            // If both options are available, default to veg
            if (hostel.is_veg && hostel.is_non_veg) {
                setSelectedFoodType("veg");
            } else if (hostel.is_veg) {
                setSelectedFoodType("veg");
            } else if (hostel.is_non_veg) {
                setSelectedFoodType("non_veg");
            }
        }
    }, [hostel]);

    // Calculate the price based on the selected food type
    const getPrice = () => {
        if (!hostel?.amount) return "N/A";
        return selectedFoodType === "veg" 
            ? hostel.amount.Mgmt_veg || "N/A" 
            : hostel.amount.Mgmt_non_veg || "N/A";
    };

    const formatDate = (dateString: string) => {
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            return 'Invalid Date';
        }
    };

    const hasActiveBooking = userBookings?.some(booking =>
        booking.status === 'otp_pending' ||
        booking.status === 'payment_pending' ||
        booking.status === 'confirmed'
        // ||
        // booking.status === 'cancelled'
        // ||
        // booking.status == 'payment_not_done'
    );

    const { mutate: createBooking, isPending: isCreatingBooking } = useCreateBooking((response) => {
        try {
            const bookingResponse = response.data as BookingResponse;
            if (bookingResponse.booking_id) {
                setBookingId(bookingResponse.booking_id);
                setShowConfirmDialog(false);
                setShowOTPDialog(true);
                toast.success("OTP sent to your email!");
            } else if (response.data === "You have already booked a hostel") {
                toast.error("You already have an active booking!");
                if (bookingResponse.booking_id) {
                    navigate(`/bookings/${bookingResponse.booking_id}`);
                } else {
                    navigate('/bookings');
                }
            }
        } catch (error) {
            console.error("Error parsing booking response:", error);
            alert(error)
        }
    });

    const handleBooking = () => {
        setShowConfirmDialog(true);
    };

    const confirmBooking = () => {
        if (!id) return;
        console.log(selectedFoodType)
        createBooking({
            hostel: parseInt(id),
            food_type: selectedFoodType
        });
    };

    const handleOTPVerification = async () => {
        if (!bookingId || !otp) return;

        setIsVerifyingOTP(true);
        try {
            const response = await api.post('/hostel/verify_otp/', {
                booking_id: bookingId,
                otp_code: otp
            });

            if (response.status === 200) {
                const { payment_link, payment_instructions, expires_at } = response.data;
                toast.success("OTP verified successfully!");
                setShowOTPDialog(false);

                // Show payment instructions in a success toast
                toast.success(
                    <div className="space-y-2">
                        <p className="font-medium">Payment Instructions:</p>
                        <p>{payment_instructions}</p>
                        <p className="text-sm text-muted">Payment link has been sent to your email.</p>
                        <p className="text-sm text-yellow-600">Complete payment before: {formatDate(expires_at)}</p>
                    </div>,
                    {
                        duration: 10000, // Show for 10 seconds
                    }
                );

                navigate(`/bookings/${bookingId}`);
            }
        } catch (error: any) {
            const errorMessage = error.response?.data?.message || "Invalid/OTP Expired";
            toast.error(errorMessage);

            // If OTP is expired, close the dialog and redirect to bookings
            if (errorMessage.includes("expired")) {
                setShowOTPDialog(false);
                navigate('/bookings');
            }
        } finally {
            setIsVerifyingOTP(false);
        }
    };

    if (isLoadingHostel) {
        return (
            <div className="container mx-auto px-4 py-8">
                <Card className="overflow-hidden">
                    <Skeleton className="h-[500px] w-full" />
                    <CardHeader className="space-y-4">
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
            <Card className="overflow-hidden">
                <CardHeader className="space-y-6">
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div className="relative">
                            <CardTitle className="text-4xl font-bold text-foreground">{hostel?.name}</CardTitle>
                            <div className="flex items-center gap-2 text-muted-foreground mt-2">
                                <MapPin className="h-5 w-5" />
                                <span className="text-lg">{hostel?.location}</span>
                                <Badge variant="secondary" className="bg-muted/50 backdrop-blur-sm text-xs px-4 py-1">
                                    {hostel?.room_type}
                                </Badge>
                                <Badge variant="secondary" className="bg-muted/50 backdrop-blur-sm text-xs px-4 py-1">
                                    {hostel?.is_veg && hostel?.is_non_veg ? "Veg & Non-veg" : 
                                     hostel?.is_veg ? "Veg" : 
                                     hostel?.is_non_veg ? "Non-veg" : "No food"}
                                </Badge>
                            </div>
                        </div>
                        <div className="bg-muted/50 p-4 rounded-lg">
                            <p className="text-3xl font-bold text-primary">₹{getPrice()}</p>
                            <p className="text-sm text-muted-foreground">{selectedFoodType} option</p>
                        </div>
                    </div>
                </CardHeader>

                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="space-y-8">
                            <div>
                                <h3 className="text-2xl font-semibold text-foreground mb-4">Description</h3>
                                <p className="text-muted-foreground text-lg leading-relaxed">{hostel?.room_description}</p>
                            </div>

                            <Separator className="my-6" />

                            <div>
                                <h3 className="text-2xl font-semibold text-foreground mb-6">Details</h3>
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <BedDouble className="h-4 w-4" />
                                            <span className="text-sm">Room Type</span>
                                        </div>
                                        <p className="font-medium text-lg">{hostel?.room_type}</p>
                                    </div>
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <Utensils className="h-4 w-4" />
                                            <span className="text-sm">Food Options</span>
                                        </div>
                                        <p className="font-medium text-lg">
                                            {hostel?.is_veg && hostel?.is_non_veg ? "Veg & Non-veg" : 
                                             hostel?.is_veg ? "Veg only" : 
                                             hostel?.is_non_veg ? "Non-veg only" : "No food"}
                                        </p>
                                    </div>
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <User2 className="h-4 w-4" />
                                            <span className="text-sm">Gender</span>
                                        </div>
                                        <p className="font-medium text-lg">{hostel?.gender === 'M' ? 'Male' : 'Female'}</p>
                                    </div>
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <Bath className="h-4 w-4" />
                                            <span className="text-sm">Restroom</span>
                                        </div>
                                        <p className="font-medium text-lg">{hostel?.bathroom_type}</p>
                                    </div>
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <Users className="h-4 w-4" />
                                            <span className="text-sm">Persons per Room</span>
                                        </div>
                                        <p className="font-medium text-lg">{hostel?.person_per_room}</p>
                                    </div>
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <Building2 className="h-4 w-4" />
                                            <span className="text-sm">Total Rooms</span>
                                        </div>
                                        <p className="font-medium text-lg">{hostel?.no_of_rooms}</p>
                                    </div>
                                    <div className="bg-muted/50 p-4 rounded-lg">
                                        <div className="flex items-center gap-2 text-muted-foreground mb-2">
                                            <Users className="h-4 w-4" />
                                            <span className="text-sm">Total Capacity</span>
                                        </div>
                                        <p className="font-medium text-lg">{hostel?.total_capacity}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="bg-muted/50 p-6 rounded-lg">
                            <h3 className="text-2xl font-semibold text-foreground mb-6">Book Now</h3>
                            <div className="space-y-6">
                                {/* Food Type Selection */}
                                {(hostel?.is_veg || hostel?.is_non_veg) && (
                                    <div className="mb-6">
                                        <h4 className="text-lg font-medium mb-3">Select Food Type</h4>
                                        <RadioGroup 
                                            value={selectedFoodType} 
                                            onValueChange={(value) => setSelectedFoodType(value as "veg" | "non_veg")}
                                            className="space-y-3"
                                        >
                                            {hostel?.is_veg && (
                                                <div className="flex items-center space-x-2">
                                                    <RadioGroupItem value="veg" id="veg" disabled={!hostel?.is_veg} />
                                                    <Label htmlFor="veg" className="cursor-pointer">
                                                        Vegetarian (₹{hostel?.amount?.Mgmt_veg || "N/A"})
                                                    </Label>
                                                </div>
                                            )}
                                            {hostel?.is_non_veg && (
                                                <div className="flex items-center space-x-2">
                                                    <RadioGroupItem value="non_veg" id="nonveg" disabled={!hostel?.is_non_veg} />
                                                    <Label htmlFor="nonveg" className="cursor-pointer">
                                                        Non-Vegetarian (₹{hostel?.amount?.Mgmt_non_veg || "N/A"})
                                                    </Label>
                                                </div>
                                            )}
                                        </RadioGroup>
                                    </div>
                                )}

                                <div>
                                    <p className="text-muted-foreground mb-2">Total Fees</p>
                                    <p className="text-3xl font-bold text-primary">₹{getPrice()}</p>
                                </div>
                                <div>
                                    <p className="text-muted-foreground mb-2">Available</p>
                                    <p className="text-2xl font-semibold text-foreground">{(hostel?.available_rooms || 0)}</p>
                                </div>
                                <div className="flex flex-col md:flex-row gap-4 items-center justify-between mt-8">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <AlertCircle className="h-5 w-5" />
                                        <p className="text-sm">
                                            {hasActiveBooking
                                                ? "You already have an active booking."
                                                : "Book now to secure your room. Limited slots available!"}
                                        </p>
                                    </div>
                                    <Button
                                        size="lg"
                                        onClick={handleBooking}
                                        disabled={hasActiveBooking || !hostel?.available_rooms || isCreatingBooking}
                                    >
                                        {isCreatingBooking ? "Processing..." : "Book Now"}
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Confirmation Dialog */}
            <Dialog open={showConfirmDialog} onOpenChange={setShowConfirmDialog}>
                <DialogContent className="sm:max-w-[425px] max-h-[90vh]">
                    <ScrollArea className="h-full max-h-[80vh]">
                        <DialogHeader>
                            <DialogTitle className="text-2xl font-bold text-primary">Confirm Booking</DialogTitle>
                            <DialogDescription className="text-base">
                                Please review the booking details and important notes before proceeding.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="py-4">
                            <div className="space-y-4">
                                <div className="bg-muted/50 p-4 rounded-lg space-y-2">
                                    <p className="font-medium">Hostel: {hostel?.name}</p>
                                    <p className="font-medium">Room Type: {hostel?.room_type}</p>
                                    <p className="font-medium">Food Type: {selectedFoodType}</p>
                                    <p className="font-medium text-primary text-xl">Total Fees: ₹{getPrice()}</p>
                                </div>

                                <div className="space-y-3">
                                    <p className="font-semibold">Important Notes:</p>
                                    <div className="bg-yellow-50 p-4 rounded-lg space-y-2 text-sm text-yellow-800">
                                        <p>1. An OTP will be sent to your email for verification.</p>
                                        <p>2. The OTP is valid for 10 minutes only.</p>
                                        <p>3. After OTP verification, you must complete the payment within 5 days.</p>
                                        <p>4. If failed to pay within given deadline, booking will be cancelled and a Rs.10,000 penalty will be added.</p>
                                        <p>5. The Fees shown is for the entire academic year.</p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-2 text-blue-600 bg-blue-50 p-3 rounded-lg">
                                    <AlertCircle className="h-5 w-5" />
                                    <p className="text-sm">Make sure you have access to your email before proceeding.</p>
                                </div>
                            </div>
                        </div>
                    </ScrollArea>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setShowConfirmDialog(false)}>
                            Cancel
                        </Button>
                        <Button
                            onClick={confirmBooking}
                            disabled={isCreatingBooking}
                            className="bg-primary hover:bg-primary/90"
                        >
                            {isCreatingBooking ? "Processing..." : "Proceed with Booking"}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

            {/* OTP Dialog */}
            <Dialog open={showOTPDialog} onOpenChange={setShowOTPDialog}>
                <DialogContent className="sm:max-w-[425px] max-h-[90vh]">
                    <ScrollArea className="h-full max-h-[80vh]">
                        <DialogHeader>
                            <DialogTitle className="text-2xl font-bold text-primary">Verify OTP</DialogTitle>
                            <DialogDescription className="text-base">
                                Please enter the 6-digit OTP sent to your email address to confirm your booking.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="py-4">
                            <div className="space-y-4">
                                <div className="bg-muted/50 p-4 rounded-lg space-y-2">
                                    <p className="font-medium">Hostel: {hostel?.name}</p>
                                    <p className="font-medium">Room Type: {hostel?.room_type}</p>
                                    <p className="font-medium">Food Type: {selectedFoodType}</p>
                                    <p className="font-medium text-primary text-xl">Total Fees: ₹{getPrice()}</p>
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
                                    <p className="text-sm">The OTP will expire in 10 minutes. Please complete the payment within 5 Days after verification.</p>
                                </div>
                            </div>
                        </div>
                    </ScrollArea>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setShowOTPDialog(false)}>
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
        </div>
    );
} 