import { useState, useEffect } from "react";
import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { api } from "@/action/user";
import { toast } from "sonner";

// Define the forgot password schema with Zod
const forgotPasswordSchema = z.object({
    email: z.string().email("Please enter a valid email address"),
});

type ForgotPasswordFormValues = z.infer<typeof forgotPasswordSchema>;

const carouselImages = [
    "/images/banner-1.jpg",
    "/images/images.jpeg",
    "/images/images (1).jpeg",
    "/images/1551372417phpw6JY3j.jpeg"
];

export default function ForgotPassword() {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentImageIndex((prevIndex) =>
                prevIndex === carouselImages.length - 1 ? 0 : prevIndex + 1
            );
        }, 5000); // Change image every 5 seconds

        return () => clearInterval(timer);
    }, []);

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm<ForgotPasswordFormValues>({
        resolver: zodResolver(forgotPasswordSchema)
    });

    const onSubmit = async (data: ForgotPasswordFormValues) => {
        setIsSubmitting(true);
        try {
            const response = await api.post('/auth/forgot-password/', data);

            if (response.status === 200) {
                toast.success(
                    <div className="space-y-2">
                        <p>Password reset instructions sent!</p>
                        <p className="text-sm text-muted-foreground">
                            Please check your email for further instructions.
                        </p>
                    </div>,
                    { duration: 6000 }
                );
            }
        } catch (error: any) {
            const errorMessage = error?.response?.data?.message || error?.message;

            if (errorMessage?.toLowerCase().includes('not found')) {
                toast.error("Email address not found. Please check your email or sign up.");
            } else if (errorMessage?.toLowerCase().includes('network')) {
                toast.error("Network error. Please check your internet connection.");
            } else if (errorMessage?.toLowerCase().includes('verify')) {
                toast.error("Please verify your email before resetting password.");
            } else {
                toast.error(errorMessage || "Failed to send reset instructions. Please try again.");
            }
        } finally {
            setIsSubmitting(false);
        }
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
                            src="/images/images.jpeg"
                            alt="REC Hostel Logo"
                            className="w-24 h-24 mx-auto object-contain"
                        />
                        <div className="space-y-2">
                            <CardTitle className="text-2xl font-bold">Forgot Password</CardTitle>
                            <CardDescription className="text-base">
                                Enter your email address and we'll send you instructions to reset your password
                            </CardDescription>
                        </div>
                    </CardHeader>
                    <form onSubmit={handleSubmit(onSubmit)}>
                        <CardContent className="space-y-6">
                            <div className="space-y-2">
                                <Label htmlFor="email" className="text-base">Email</Label>
                                <Input
                                    id="email"
                                    type="email"
                                    placeholder="your.email@example.com"
                                    className="h-11"
                                    {...register("email")}
                                />
                                {errors.email && (
                                    <p className="text-sm text-destructive mt-1">{errors.email.message}</p>
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
                </Card>
            </div>
        </div>
    );
} 