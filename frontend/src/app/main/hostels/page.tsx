import { useGetHostels } from "@/action/hostel";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { MapPin, Users, IndianRupee, Utensils } from "lucide-react";
import { Link } from "react-router";
import { useCurrentUser } from "@/action/user";

export default function HostelsPage() {
    const { data: hostels, isLoading } = useGetHostels();
    const { data: currentUser } = useCurrentUser();

    if (isLoading) {
        return (
            <div className="container mx-auto px-4 py-12">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {[1, 2, 3, 4, 5, 6].map((i) => (
                        <Card key={i} className="overflow-hidden border-0 shadow-lg">
                            <CardHeader className="space-y-3">
                                <Skeleton className="h-7 w-3/4" />
                                <Skeleton className="h-5 w-1/2" />
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <Skeleton className="h-5 w-full" />
                                <Skeleton className="h-5 w-2/3" />
                            </CardContent>
                            <CardFooter>
                                <Skeleton className="h-11 w-full rounded-lg" />
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        );
    }

    if (!hostels?.length) {
        return (
            <div className="container mx-auto px-4 py-16">
                <div className="text-center space-y-4">
                    <h1 className="text-4xl font-bold text-foreground">No Hostels Available</h1>
                    <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                        There are currently no hostels available for {currentUser?.gender === 'M' ? 'male' : 'female'} students.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-12">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-12">
                <div>
                    <h1 className="text-4xl font-bold text-foreground mb-2">Available Hostels</h1>
                    <p className="text-lg text-muted-foreground">
                        {hostels.length} {hostels.length === 1 ? 'hostel' : 'hostels'} available for {currentUser?.gender === 'M' ? 'male' : 'female'} students
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {hostels.map((hostel) => (
                    <Card
                        key={hostel.id}
                        className="overflow-hidden border border-border shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 bg-card"
                    >
                        <CardHeader className="relative pt-6 pb-4">
                            <div className="flex justify-between items-start mb-2">
                                <CardTitle className="text-xl font-semibold text-card-foreground">{hostel.name}</CardTitle>
                                <div className="flex gap-1.5">
                                    <Badge variant="default" className="bg-primary text-primary-foreground px-2 py-0.5 text-xs">
                                        {hostel.room_type}
                                    </Badge>
                                </div>
                            </div>
                            <div className="flex items-center gap-2 text-muted-foreground">
                                <MapPin className="h-4 w-4 shrink-0" />
                                <span className="text-sm">{hostel.location}</span>
                            </div>
                            <Badge variant="outline" className="mt-2 bg-background/90 px-2 py-0.5 text-xs border-primary/50 text-primary">
                                {hostel.is_veg && hostel.is_non_veg ? "Veg & Non-veg" : 
                                 hostel.is_veg ? "Veg" : 
                                 hostel.is_non_veg ? "Non-veg" : "No food"}
                            </Badge>
                        </CardHeader>
                        <CardContent className="space-y-4 pt-0">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Users className="h-4 w-4" />
                                    <span className="text-sm">Available</span>
                                </div>
                                <span className="font-semibold text-card-foreground">{hostel.available_rooms}</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Utensils className="h-4 w-4" />
                                    <span className="text-sm">Food Options</span>
                                </div>
                                <span className="font-semibold text-card-foreground">
                                    {hostel.is_veg && hostel.is_non_veg ? "Veg & Non-veg" : 
                                     hostel.is_veg ? "Veg only" : 
                                     hostel.is_non_veg ? "Non-veg only" : "No food"}
                                </span>
                            </div>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <IndianRupee className="h-4 w-4" />
                                    <span className="text-sm">Starting From</span>
                                </div>
                                <span className="font-semibold text-card-foreground">
                                    ₹{hostel.amount && Object.values(hostel.amount).length > 0 
                                        ? Math.min(...Object.values(hostel.amount).filter(val => val > 0)) || "N/A" 
                                        : "N/A"}
                                </span>
                            </div>
                        </CardContent>
                        <CardFooter className="pt-2 pb-6">
                            <Link to={`/hostels/${hostel.id}`} className="w-full">
                                <Button className="w-full h-10 text-sm font-medium" variant="default">
                                    View Details
                                </Button>
                            </Link>
                        </CardFooter>
                    </Card>
                ))}
            </div>
        </div>
    );
} 