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
            <div className="container mx-auto px-4 py-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3, 4, 5, 6].map((i) => (
                        <Card key={i} className="overflow-hidden">
                            <Skeleton className="h-48 w-full" />
                            <CardHeader>
                                <Skeleton className="h-6 w-3/4" />
                                <Skeleton className="h-4 w-1/2 mt-2" />
                            </CardHeader>
                            <CardContent>
                                <Skeleton className="h-4 w-full mb-2" />
                                <Skeleton className="h-4 w-2/3" />
                            </CardContent>
                            <CardFooter>
                                <Skeleton className="h-10 w-full" />
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        );
    }

    if (!hostels?.length) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="text-center">
                    <h1 className="text-3xl font-bold text-foreground mb-4">No Hostels Available</h1>
                    <p className="text-muted-foreground">
                        There are currently no hostels available for {currentUser?.gender === 'M' ? 'male' : 'female'} students.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold text-foreground">Available Hostels</h1>
                <p className="text-muted-foreground">
                    {hostels.length} {hostels.length === 1 ? 'hostel' : 'hostels'} available for {currentUser?.gender === 'M' ? 'male' : 'female'} students
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {hostels.map((hostel) => (
                    <Card key={hostel.id} className="overflow-hidden hover:shadow-lg transition-shadow duration-200">
                        <div className="relative">
                            <img
                                src={hostel.image || "https://placehold.co/600x400"}
                                alt={hostel.name}
                                className="w-full h-48 object-cover"
                            />
                            <div className="absolute top-4 right-4 flex gap-2">
                                <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm">
                                    {hostel.room_type}
                                </Badge>
                                <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm">
                                    {hostel.food_type}
                                </Badge>
                            </div>
                        </div>
                        <CardHeader>
                            <CardTitle className="text-xl">{hostel.name}</CardTitle>
                            <div className="flex items-center gap-2 text-muted-foreground">
                                <MapPin className="h-4 w-4" />
                                <span className="text-sm">{hostel.location}</span>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <Users className="h-4 w-4" />
                                        <span className="text-sm">Available Students</span>
                                    </div>
                                    <span className="font-medium">{hostel.available_rooms * hostel.person_per_room}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2 text-muted-foreground">
                                        <IndianRupee className="h-4 w-4" />
                                        <span className="text-sm">Annual Price</span>
                                    </div>
                                    <span className="font-medium">₹{hostel.amount * 12}</span>
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Link to={`/hostels/${hostel.id}`} className="w-full">
                                <Button className="w-full" variant="default">
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