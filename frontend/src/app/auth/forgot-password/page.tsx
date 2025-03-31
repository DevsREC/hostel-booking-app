import { useState } from "react";
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

export default function ForgotPassword() {
    const [isSubmitting, setIsSubmitting] = useState(false);

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
        <div className="flex justify-center items-center h-full">
            <Card className="w-2/3">
                <CardHeader>
                    <CardTitle className="text-2xl">Forgot Password</CardTitle>
                    <CardDescription>
                        Enter your email address and we'll send you instructions to reset your password
                    </CardDescription>
                </CardHeader>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="email">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="your.email@example.com"
                                {...register("email")}
                            />
                            {errors.email && (
                                <p className="text-sm text-destructive">{errors.email.message}</p>
                            )}
                        </div>
                    </CardContent>
                    <CardFooter className="flex flex-col space-y-4 mt-4">
                        <Button type="submit" className="w-full" disabled={isSubmitting}>
                            {isSubmitting ? "Sending Instructions..." : "Send Reset Instructions"}
                        </Button>
                        <div className="flex justify-center gap-1 text-sm">
                            <span className="text-muted-foreground">Remember your password?</span>
                            <Link to="/auth/login" className="text-primary hover:underline">
                                Sign in
                            </Link>
                        </div>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
} 