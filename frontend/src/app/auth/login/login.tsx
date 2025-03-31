import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useLoginUser } from "@/action/user";
import { toast } from "sonner";

// Define the login schema with Zod
const loginSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(1, "Password is required")
});

type LoginFormValues = z.infer<typeof loginSchema>;

export default function Login() {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema)
  });

  // Use the login mutation
  const { mutate, isPending } = useLoginUser(() => {
    navigate("/dashboard");
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      mutate(data, {
        onSuccess: (result) => {
          if (result?.status === 200) {
            // Store user data in localStorage
            const userData = {
              id: result.user?.id,
              first_name: result.user?.first_name,
              last_name: result.user?.last_name,
              gender: result.user?.gender,
            };
            localStorage.setItem('user', JSON.stringify(userData));
            toast.success("Login successful! Welcome back.");
            navigate("/");
          } else {
            // Handle specific error cases
            const errorMessage = result?.data?.message || result?.data;
            if (typeof errorMessage === 'string') {
              if (errorMessage.toLowerCase().includes('password')) {
                toast.error("Incorrect password. Please try again.");
              } else if (errorMessage.toLowerCase().includes('email')) {
                toast.error("Email not found. Please check your email or sign up.");
              } else if (errorMessage.toLowerCase().includes('verify')) {
                toast.error("Please verify your email before logging in.");
              } else {
                toast.error(errorMessage);
              }
            } else {
              toast.error("Login failed. Please check your credentials.");
            }
          }
        },
        onError: (error: any) => {
          const errorMessage = error?.response?.data?.message || error?.message;
          if (errorMessage?.toLowerCase().includes('network')) {
            toast.error("Network error. Please check your internet connection.");
          } else {
            toast.error(errorMessage || "An error occurred during login. Please try again.");
          }
        }
      });
    } catch (err: any) {
      toast.error(err?.message || "An unexpected error occurred. Please try again.");
    }
  };

  return (
    <div className="flex justify-center items-center h-full">
      <Card className="w-2/3">
        <CardHeader>
          <CardTitle className="text-2xl">Login</CardTitle>
          <CardDescription>
            Enter your email and password to access your account
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
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Password</Label>
                <Link to="/auth/forgot-password" className="text-sm text-primary hover:underline">
                  Forgot password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                {...register("password")}
              />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4 mt-4">
            <Button type="submit" className="w-full" disabled={isPending}>
              {isPending ? "Signing in..." : "Sign in"}
            </Button>
            <p className="text-sm text-muted-foreground text-center">
              Don't have an account?{" "}
              <Link to="/auth/register" className="text-primary hover:underline">
                Sign up
              </Link>
            </p> */}
          </CardFooter>
        </form>
      </Card>
    </div>
  );
} 