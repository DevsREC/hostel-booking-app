import { useGetHostels } from "@/action/hostel";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { MapPin, Users, IndianRupee } from "lucide-react";
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
                            <Skeleton className="h-56 w-full" />
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
                        className="overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
                    >
                        <div className="relative group">
                            <img
                                src={hostel.image || "https://placehold.co/600x400"}
                                alt={hostel.name}
                                className="w-full h-56 object-cover transition-transform duration-300 group-hover:scale-105"
                            />
                            <div className="absolute top-4 right-4 flex gap-2">
                                <Badge variant="secondary" className="bg-background/90 backdrop-blur-sm px-3 py-1">
                                    {hostel.room_type}
                                </Badge>
                                <Badge variant="secondary" className="bg-background/90 backdrop-blur-sm px-3 py-1">
                                    {hostel.food_type}
                                </Badge>
                            </div>
                        </div>
                        <CardHeader className="space-y-3">
                            <CardTitle className="text-2xl font-semibold">{hostel.name}</CardTitle>
                            <div className="flex items-center gap-2 text-muted-foreground">
                                <MapPin className="h-5 w-5" />
                                <span className="text-base">{hostel.location}</span>
                            </div>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <Users className="h-5 w-5" />
                                    <span className="text-base">Available</span>
                                </div>
                                <span className="font-semibold text-lg">{hostel.available_rooms}</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 text-muted-foreground">
                                    <IndianRupee className="h-5 w-5" />
                                    <span className="text-base">Annual Price</span>
                                </div>
                                <span className="font-semibold text-lg">₹{hostel.amount * 12}</span>
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Link to={`/hostels/${hostel.id}`} className="w-full">
                                <Button className="w-full h-11 text-base font-medium" variant="default">
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