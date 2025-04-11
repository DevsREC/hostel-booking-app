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

const resetPasswordSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(6, "Password must be at least 6 characters")
});

type RequestResetFormValues = z.infer<typeof requestResetSchema>;
type ResetPasswordFormValues = z.infer<typeof resetPasswordSchema>;

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

    // Setup react-query mutations
    const passwordResetMutation = useRequestPasswordReset(() => {
        toast.success(
            <div className="space-y-2">
                <p>Password reset instructions sent!</p>
                <p className="text-sm text-muted-foreground">
                    Please check your email for verification code.
                </p>
            </div>,
            { duration: 6000 }
        );
    });

    const resetPasswordMutation = useResetPassword(() => {
        toast.success("Password reset successful!");
        
        // Redirect to login after successful reset
        setTimeout(() => {
            navigate('/auth/login');
        }, 2000);
    });

    useEffect(() => {
        // If token and email are in URL, we're in the reset confirmation mode
        if (token && email) {
            setIsTokenMode(true);
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

    // Form for requesting password reset
    const requestForm = useForm<RequestResetFormValues>({
        resolver: zodResolver(requestResetSchema)
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
        // Pass both email and password as per backend requirements
        passwordResetMutation.mutate({
            email: data.email,
            password: data.password
        });
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
                            src="/images/images.jpeg"
                            alt="REC Hostel Logo"
                            className="w-24 h-24 mx-auto object-contain"
                        />
                        <div className="space-y-2">
                            <CardTitle className="text-2xl font-bold">
                                {isTokenMode ? "Reset Password" : "Forgot Password"}
                            </CardTitle>
                            <CardDescription className="text-base">
                                {isTokenMode 
                                    ? "Enter your new password to complete the reset process" 
                                    : "Enter your email address and we'll send you instructions to reset your password"
                                }
                            </CardDescription>
                        </div>
                    </CardHeader>
                    
                    {isTokenMode ? (
                        // Reset password form with token
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
                    ) : (
                        // Request reset form
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