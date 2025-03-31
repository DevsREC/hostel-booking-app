import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useNavigate } from "react-router";
import { useLogout, useCurrentUser } from "@/action/user";

import { Skeleton } from "@/components/ui/skeleton";

interface HeaderProps {
  toggleSidebar: () => void;
}

export function Header({ toggleSidebar }: HeaderProps) {
  const { mutate } = useLogout();
  const navigate = useNavigate();
  const { data: user, isLoading } = useCurrentUser();

  const handleLogout = () => {
    mutate(undefined);
    navigate("/auth/login");
  };

  const getInitials = (firstName: string | undefined | null, lastName: string | undefined | null) => {
    if (!firstName && !lastName) return "U";
    return `${firstName?.[0] || ''}${lastName?.[0] || ''}`.toUpperCase() || "U";
  };

  if (isLoading) {
    return (
      <div className="h-16 border-b flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <Skeleton className="h-8 w-32" />
        </div>
        <div className="flex items-center gap-4">
          <Skeleton className="h-8 w-24" />
        </div>
      </div>
    );
  }

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background">
      <div className="px-10 flex h-16 items-center justify-between py-4">
        <div className="flex items-center gap-2">
          <Link to="/" className="flex items-center gap-2">
            <img
              src="/images/images.jpeg"
              alt="REC Hostel Logo"
              className="h-8 w-8 object-contain"
            />
            <span className="text-xl font-bold">REC Hostel</span>
          </Link>
        </div>

        <div className="flex items-center gap-4">
          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="" alt="Avatar" />
                    <AvatarFallback>
                      {getInitials(user.first_name, user.last_name)}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {`${user.first_name} ${user.last_name}`}
                    </p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {user.email}
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => navigate("/bookings")}>
                  Bookings
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => navigate("/profile")}>
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => navigate("/setting")}>
                  Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout}>
                  Log out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button variant="default" onClick={() => navigate("/login")}>
              Sign In
            </Button>
          )}
        </div>
      </div>
    </header>
  );
} 