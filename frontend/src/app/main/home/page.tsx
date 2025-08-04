import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { useGetProfile } from '@/action/user';
import { useGetLongDistanceRoutes, Route } from '@/action/hostel';
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { InfoIcon, Bus, MapPin, Users, IndianRupee, Utensils, ChevronDown, ChevronUp, CheckCircle, ArrowRight } from 'lucide-react';
import { Link } from 'react-router';
import { useGetHostels } from '@/action/hostel';

const HomePage = () => {
  const navigate = useNavigate();
  const { data: user, isLoading: userLoading } = useGetProfile();
  const { data: routes, isLoading: routesLoading } = useGetLongDistanceRoutes();
  const { data: hostels, isLoading: hostelsLoading } = useGetHostels();
  const [isExpanded, setIsExpanded] = useState(false);
  const [hasClickedYes, setHasClickedYes] = useState(false);

  useEffect(() => {
    if (user?.is_long_distance_student || user?.has_booking) {
      navigate('/hostels');
    }
  }, [user, navigate]);

  if (userLoading) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="space-y-8">
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-64 w-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Long Distance Announcement - Accordion Style */}
      {user && !user.is_long_distance_student && !user.has_booking && !hasClickedYes && (
        <Card className="mb-8 border-2 border-primary/20 shadow-lg bg-gradient-to-br from-background to-muted/30">
          <CardHeader className="pb-4">
            <div 
              className="flex items-center justify-between cursor-pointer"
              onClick={() => setIsExpanded(!isExpanded)}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary/10 rounded-full">
                  <Bus className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <CardTitle className="text-xl font-bold text-foreground">Free Hostel Accommodation for Long Distance Students</CardTitle>
                  <CardDescription className="text-muted-foreground">
                    Check if you're eligible for free hostel accommodation
                  </CardDescription>
                </div>
              </div>
              <Button variant="ghost" size="sm" className="p-2">
                {isExpanded ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
              </Button>
            </div>
          </CardHeader>
          
          {isExpanded && (
            <CardContent className="pt-0 space-y-6">
              {/* Step-by-step instructions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-foreground">How to Avail Free Hostel Accommodation:</h3>
                <div className="space-y-3">
                  <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">
                      1
                    </div>
                    <div>
                      <p className="font-medium text-foreground">Check Your Route Eligibility</p>
                      <p className="text-sm text-muted-foreground">Verify if your bus route is listed in the available long distance routes below.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">
                      2
                    </div>
                    <div>
                      <p className="font-medium text-foreground">Submit Route Application</p>
                      <p className="text-sm text-muted-foreground">Click "Yes, I'm from Long Distance" and select your specific route from the form.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">
                      3
                    </div>
                    <div>
                      <p className="font-medium text-foreground">Select Preferred Hostel & Verify</p>
                      <p className="text-sm text-muted-foreground">After choosing "Yes", select your preferred hostel and verify your selection with OTP.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">
                      4
                    </div>
                    <div>
                      <p className="font-medium text-foreground">Contact SAO Office</p>
                      <p className="text-sm text-muted-foreground">After route confirmation and hostel verification, visit the SAO - Senior Administrative Officer for hostel allocation and further instructions.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">
                      5
                    </div>
                    <div>
                      <p className="font-medium text-foreground">Complete Documentation</p>
                      <p className="text-sm text-muted-foreground">Submit required documents and complete the hostel booking process as directed by SAO.</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Available Routes */}
              <div className="space-y-3">
                <h3 className="text-lg font-semibold text-foreground">Available Long Distance Routes:</h3>
                {routesLoading ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {[1, 2, 3, 4, 5, 6].map((i) => (
                      <Skeleton key={i} className="h-16 w-full" />
                    ))}
                  </div>
                ) : routes && routes.length > 0 ? (
                  <ScrollArea className="h-64 border rounded-lg p-4 bg-background">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {routes.map(route => (
                        <div key={route.id} className="p-3 bg-muted/50 border border-border rounded-lg hover:bg-muted transition-colors">
                          <div className="flex items-center gap-2 mb-1">
                            <Badge variant="secondary" className="bg-primary/10 text-primary text-xs">
                              Route {route.bus_route_no}
                            </Badge>
                          </div>
                          <div className="text-sm font-medium text-foreground">{route.bus_route_name}</div>
                        </div>
                      ))}
                    </div>
                  </ScrollArea>
                ) : (
                  <div className="text-center text-muted-foreground py-8">
                    <Bus className="h-12 w-12 mx-auto mb-3 opacity-50" />
                    <p>No routes available at the moment.</p>
                  </div>
                )}
              </div>

              {/* Important Information */}
              <Alert className="border-primary/20 bg-primary/5">
                <InfoIcon className="h-5 w-5 text-primary" />
                <AlertDescription className="text-foreground">
                  <strong>Important:</strong> Free hostel accommodation is provided to eligible long distance students. 
                  After route confirmation, you must contact the SAO for hostel allocation and complete the required documentation process.
                </AlertDescription>
              </Alert>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                <Button 
                  onClick={() => {
                    setHasClickedYes(true);
                    navigate("/special-form");
                  }}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3 text-lg"
                  size="lg"
                >
                  <CheckCircle className="h-5 w-5 mr-2" />
                  Yes, I'm from Long Distance
                </Button>
                <Button 
                  onClick={() => setHasClickedYes(true)}
                  variant="outline"
                  className="border-border text-foreground hover:bg-muted px-8 py-3 text-lg"
                  size="lg"
                >
                  <ArrowRight className="h-5 w-5 mr-2" />
                  No, Show Me Hostels
                </Button>
              </div>
            </CardContent>
          )}
        </Card>
      )}

      {/* Quick Hostel Preview */}
      {!hostelsLoading && hostels && hostels.length > 0 && (
        <div className="space-y-6">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-foreground mb-2">Available Hostels</h2>
            <p className="text-lg text-muted-foreground">
              {hostels.length} {hostels.length === 1 ? 'hostel' : 'hostels'} available for {user?.gender === 'M' ? 'male' : 'female'} students
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {hostels.slice(0, 3).map((hostel) => (
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
                      <IndianRupee className="h-4 w-4" />
                      <span className="text-sm">Starting From</span>
                    </div>
                    <span className="font-semibold text-card-foreground">
                      ₹{(() => {
                        if (!hostel.amount || Object.values(hostel.amount).length === 0) return 0;
                        const validAmounts = Object.values(hostel.amount).filter(val => val > 0);
                        return validAmounts.length > 0 ? Math.min(...validAmounts) : 0;
                      })()}
                    </span>
                  </div>
                </CardContent>
                <CardContent className="pt-0">
                  <Link to={`/hostels/${hostel.id}`} className="w-full">
                    <Button className="w-full h-10 text-sm font-medium" variant="default">
                      View Details
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>

          {hostels.length > 3 && (
            <div className="text-center">
              <Link to="/hostels">
                <Button variant="outline" size="lg" className="px-8 py-3">
                  View All {hostels.length} Hostels
                </Button>
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default HomePage; 