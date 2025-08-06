import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router";
import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { api, useRequestPasswordReset, useResetPassword } from "@/action/user";
import { toast } from "sonner";

// Define the forgot password schema with Zod
const requestResetSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(6, "Password must be at least 6 characters")
});

const otpVerificationSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
    otp: z.string().min(4, "OTP must be at least 4 characters")
});

const resetPasswordSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(6, "Password must be at least 6 characters")
});

type RequestResetFormValues = z.infer<typeof requestResetSchema>;
type OtpVerificationFormValues = z.infer<typeof otpVerificationSchema>;
type ResetPasswordFormValues = z.infer<typeof resetPasswordSchema>;

// Constants for localStorage keys
const RESET_STATE_KEY = "password_reset_state";
const RESET_EMAIL_KEY = "password_reset_email";
const RESET_PASSWORD_KEY = "password_reset_password";

const carouselImages = [
    "/images/banner-1.jpg",
    "/images/images.jpeg",
    "/images/images (1).jpeg",
    "/images/1551372417phpw6JY3j.jpeg"
];

export default function ForgotPassword() {
    const navigate = useNavigate();
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const token = searchParams.get('token');
    const email = searchParams.get('email');
    
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [isTokenMode, setIsTokenMode] = useState(false);
    const [isOtpMode, setIsOtpMode] = useState(false);
    const [userEmail, setUserEmail] = useState("");
    const [userPassword, setUserPassword] = useState("");

    // Setup react-query mutations
    const passwordResetMutation = useRequestPasswordReset(() => {
        toast.success(
            <div className="space-y-2">
                <p>Password reset instructions sent!</p>
                <p className="text-sm text-muted-foreground">
                    Please check your email for verification code or enter the OTP below.
                </p>
            </div>,
            { duration: 6000 }
        );
        // Save state to localStorage
        localStorage.setItem(RESET_STATE_KEY, "otp_verification");
        localStorage.setItem(RESET_EMAIL_KEY, userEmail);
        localStorage.setItem(RESET_PASSWORD_KEY, userPassword);
        setIsOtpMode(true);
    });

    const resetPasswordMutation = useResetPassword(() => {
        toast.success("Password reset successful!");
        
        // Clear localStorage when reset is complete
        clearResetState();
        
        // Redirect to login after successful reset
        setTimeout(() => {
            navigate('/auth/login');
        }, 2000);
    });

    // Check localStorage on initial load
    useEffect(() => {
        // If token and email are in URL, we're in the reset confirmation mode
        if (token && email) {
            setIsTokenMode(true);
            setUserEmail(email);
            return;
        }
        
        // Check if we have an ongoing reset process
        const savedState = localStorage.getItem(RESET_STATE_KEY);
        const savedEmail = localStorage.getItem(RESET_EMAIL_KEY);
        const savedPassword = localStorage.getItem(RESET_PASSWORD_KEY);
        
        if (savedState === "otp_verification" && savedEmail) {
            setIsOtpMode(true);
            setUserEmail(savedEmail);
            if (savedPassword) {
                setUserPassword(savedPassword);
            }
            
            // Update the form defaults
            otpForm.reset({ 
                email: savedEmail,
                otp: ""
            });
        }
    }, [token, email]);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentImageIndex((prevIndex) =>
                prevIndex === carouselImages.length - 1 ? 0 : prevIndex + 1
            );
        }, 5000); // Change image every 5 seconds

        return () => clearInterval(timer);
    }, []);

    // Function to clear reset state from localStorage
    const clearResetState = () => {
        localStorage.removeItem(RESET_STATE_KEY);
        localStorage.removeItem(RESET_EMAIL_KEY);
        localStorage.removeItem(RESET_PASSWORD_KEY);
    };

    // Form for requesting password reset
    const requestForm = useForm<RequestResetFormValues>({
        resolver: zodResolver(requestResetSchema)
    });

    // Form for OTP verification
    const otpForm = useForm<OtpVerificationFormValues>({
        resolver: zodResolver(otpVerificationSchema),
        defaultValues: {
            email: userEmail,
            otp: ""
        }
    });

    // Form for setting new password
    const resetForm = useForm<ResetPasswordFormValues>({
        resolver: zodResolver(resetPasswordSchema),
        defaultValues: {
            email: email || ""
        }
    });

    // Handle request password reset
    const onRequestReset = async (data: RequestResetFormValues) => {
        // Save user email and password for OTP verification
        setUserEmail(data.email);
        setUserPassword(data.password);
        
        // Pass both email and password as per backend requirements
        passwordResetMutation.mutate({
            email: data.email,
            password: data.password
        });
    };

    // Handle OTP verification
    const onVerifyOtp = async (data: OtpVerificationFormValues) => {
        try {
            const response = await api.get(`/authenticate/forgot_password/?email=${data.email}&token=${data.otp}`);
            
            if (response.status === 200) {
                toast.success("Password reset successful!");
                
                // Clear localStorage when reset is complete
                clearResetState();
                
                // Redirect to login after successful reset
                setTimeout(() => {
                    navigate('/auth/login');
                }, 2000);
            }
        } catch (error: any) {
            const errorMessage = error?.response?.data?.detail || error?.message;
            toast.error(errorMessage || "Invalid OTP. Please try again.");
        }
    };

    // Handle confirm reset with token
    const onConfirmReset = async (data: ResetPasswordFormValues) => {
        if (!token) {
            toast.error("Reset token is missing. Please try again or request a new reset link.");
            return;
        }
        
        resetPasswordMutation.mutate({
            email: data.email,
            token: token
        });
    };

    const isSubmitting = passwordResetMutation.isPending || resetPasswordMutation.isPending;

    // Reset to request mode and clear persisted state
    const resetForm_back = () => {
        setIsOtpMode(false);
        clearResetState();
    };

    return (
        <div className="flex h-screen relative">
            {/* Carousel Section */}
            <div className="absolute inset-0">
                <div className="absolute inset-0">
                    {carouselImages.map((image, index) => (
                        <div
                            key={image}
                            className={`absolute inset-0 transition-opacity duration-1000 ${index === currentImageIndex ? 'opacity-100' : 'opacity-0'
                                }`}
                            style={{
                                backgroundImage: `url(${image})`,
                                backgroundSize: 'cover',
                                backgroundPosition: 'center',
                            }}
                        >
                            <div className="absolute inset-0 bg-black/40 dark:bg-black/60" />
                        </div>
                    ))}
                </div>
                <div className="relative z-10 flex flex-col justify-center items-center text-white p-8 w-full h-full">
                    <img
                        src="/images/images.jpeg"
                        alt="REC Hostel Logo"
                        className="w-32 h-32 mb-8 object-contain"
                    />
                    <h1 className="text-4xl font-bold mb-4 text-center">Reset Your Password</h1>
                    <p className="text-xl text-center max-w-md">We'll help you get back into your account</p>
                </div>
            </div>

            {/* Form Section */}
            <div className="flex-1 flex items-center justify-center p-4 relative z-20">
                <Card className="w-full max-w-md shadow-lg bg-background/80 backdrop-blur-sm border-border/50">
                    <CardHeader className="text-center space-y-4">
                        <img
                            src="/images/rec_logo.png"
                            alt="REC Hostel Logo"
                            className="w-32 h-32 mx-auto object-contain"
                        />
                        <div className="space-y-2">
                            <CardTitle className="text-2xl font-bold">
                                {isTokenMode ? "Reset Password" : isOtpMode ? "Verify OTP" : "Forgot Password"}
                            </CardTitle>
                            <CardDescription className="text-base">
                                {isTokenMode 
                                    ? "Enter your new password to complete the reset process" 
                                    : isOtpMode
                                    ? "Enter the verification code sent to your email"
                                    : "Enter your email address and new password to start the reset process"
                                }
                            </CardDescription>
                        </div>
                    </CardHeader>
                    
                    {isTokenMode ? (
                        // Reset password form with token from URL
                        <form onSubmit={resetForm.handleSubmit(onConfirmReset)}>
                            <CardContent className="space-y-6">
                                <div className="space-y-2">
                                    <Label htmlFor="reset-email" className="text-base">Email</Label>
                                    <Input
                                        id="reset-email"
                                        type="email"
                                        readOnly={!!email}
                                        placeholder="your.email@example.com"
                                        className="h-11"
                                        {...resetForm.register("email")}
                                    />
                                    {resetForm.formState.errors.email && (
                                        <p className="text-sm text-destructive mt-1">{resetForm.formState.errors.email.message}</p>
                                    )}
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="new-password" className="text-base">New Password</Label>
                                    <Input
                                        id="new-password"
                                        type="password"
                                        placeholder="********"
                                        className="h-11"
                                        {...resetForm.register("password")}
                                    />
                                    {resetForm.formState.errors.password && (
                                        <p className="text-sm text-destructive mt-1">{resetForm.formState.errors.password.message}</p>
                                    )}
                                </div>
                            </CardContent>
                            <CardFooter className="flex flex-col space-y-4 mt-4">
                                <Button type="submit" className="w-full h-11 text-base" disabled={isSubmitting}>
                                    {isSubmitting ? "Resetting Password..." : "Reset Password"}
                                </Button>
                                <p className="text-sm text-muted-foreground text-center">
                                    Remember your password?{" "}
                                    <Link to="/auth/login" className="text-primary hover:underline font-medium">
                                        Sign in
                                    </Link>
                                </p>
                            </CardFooter>
                        </form>
                    ) : isOtpMode ? (
                        // OTP verification form
                        <form onSubmit={otpForm.handleSubmit(onVerifyOtp)}>
                            <CardContent className="space-y-6">
                                <div className="space-y-2">
                                    <Label htmlFor="otp-email" className="text-base">Email</Label>
                                    <Input
                                        id="otp-email"
                                        type="email"
                                        value={userEmail}
                                        readOnly
                                        className="h-11 bg-muted"
                                        {...otpForm.register("email")}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="otp" className="text-base">Verification Code (OTP)</Label>
                                    <Input
                                        id="otp"
                                        type="text"
                                        placeholder="Enter OTP sent to your email"
                                        className="h-11"
                                        {...otpForm.register("otp")}
                                    />
                                    {otpForm.formState.errors.otp && (
                                        <p className="text-sm text-destructive mt-1">{otpForm.formState.errors.otp.message}</p>
                                    )}
                                </div>
                                <p className="text-sm text-muted-foreground">
                                    Please check your email for the verification code. You can navigate away to check and come back.
                                </p>
                            </CardContent>
                            <CardFooter className="flex flex-col space-y-4 mt-4">
                                <Button type="submit" className="w-full h-11 text-base" disabled={isSubmitting}>
                                    {isSubmitting ? "Verifying..." : "Verify OTP"}
                                </Button>
                                <Button 
                                    type="button" 
                                    variant="outline" 
                                    className="w-full h-11 text-base"
                                    onClick={resetForm_back}
                                >
                                    Back
                                </Button>
                                <p className="text-sm text-muted-foreground text-center">
                                    Remember your password?{" "}
                                    <Link to="/auth/login" className="text-primary hover:underline font-medium">
                                        Sign in
                                    </Link>
                                </p>
                            </CardFooter>
                        </form>
                    ) : (
                        // Initial request reset form
                        <form onSubmit={requestForm.handleSubmit(onRequestReset)}>
                            <CardContent className="space-y-6">
                                <div className="space-y-2">
                                    <Label htmlFor="email" className="text-base">Email</Label>
                                    <Input
                                        id="email"
                                        type="email"
                                        placeholder="your.email@example.com"
                                        className="h-11"
                                        {...requestForm.register("email")}
                                    />
                                    {requestForm.formState.errors.email && (
                                        <p className="text-sm text-destructive mt-1">{requestForm.formState.errors.email.message}</p>
                                    )}
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="password" className="text-base">New Password</Label>
                                    <Input
                                        id="password"
                                        type="password"
                                        placeholder="********"
                                        className="h-11"
                                        {...requestForm.register("password")}
                                    />
                                    {requestForm.formState.errors.password && (
                                        <p className="text-sm text-destructive mt-1">{requestForm.formState.errors.password.message}</p>
                                    )}
                                </div>
                            </CardContent>
                            <CardFooter className="flex flex-col space-y-4 mt-4">
                                <Button type="submit" className="w-full h-11 text-base" disabled={isSubmitting}>
                                    {isSubmitting ? "Sending Instructions..." : "Send Reset Instructions"}
                                </Button>
                                <p className="text-sm text-muted-foreground text-center">
                                    Remember your password?{" "}
                                    <Link to="/auth/login" className="text-primary hover:underline font-medium">
                                        Sign in
                                    </Link>
                                </p>
                            </CardFooter>
                        </form>
                    )}
                </Card>
            </div>
        </div>
    );
} 