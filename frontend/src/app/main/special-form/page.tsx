import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { useGetProfile } from '@/action/user';
import { useGetLongDistanceRoutes, useCreateLongDistanceStudent } from '@/action/hostel';
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { toast } from 'sonner';
import { InfoIcon, Bus, CheckCircle, ArrowLeft, Loader2, Shield, MapPin, Users } from 'lucide-react';

const SpecialFormPage = () => {
  const navigate = useNavigate();
  const { data: user, isLoading: userLoading } = useGetProfile();
  const [showForm, setShowForm] = useState(false);
  const [selectedRoute, setSelectedRoute] = useState<string>('');

  const { data: routes, isLoading: routesLoading } = useGetLongDistanceRoutes();
  const submitMutation = useCreateLongDistanceStudent(() => {
    toast.success('Route submitted successfully! You can now select your preferred hostel.');
    navigate('/');
  });

  useEffect(() => {
    if (user?.is_long_distance_student || user?.has_booking) {
      navigate('/');
    }
  }, [user, navigate]);

  if (userLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
        <Card className="w-full max-w-md shadow-lg bg-background/80 backdrop-blur-sm border-border/50">
          <CardContent className="p-6">
            <div className="space-y-4">
              <Skeleton className="h-8 w-3/4 mx-auto" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
              <Skeleton className="h-12 w-full" />
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (user && !user.is_long_distance_student && !user.has_booking) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
        <Card className="w-full max-w-lg shadow-xl bg-background/95 backdrop-blur-sm border-border/50">
          <CardHeader className="text-center space-y-4 pb-6">
            <div className="flex items-center justify-center gap-3 mb-2">
              <div className="p-3 bg-primary/10 rounded-full">
                <Bus className="h-8 w-8 text-primary" />
              </div>
              <div>
                <CardTitle className="text-2xl font-bold text-foreground">Long Distance Route Application</CardTitle>
                <CardDescription className="text-base text-muted-foreground">
                  Step 2: Confirm your eligibility
                </CardDescription>
              </div>
            </div>
            
            {/* Progress Indicator */}
            <div className="flex items-center justify-center gap-2">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <span className="text-sm font-medium text-primary">Route Selection</span>
              </div>
              <div className="w-8 h-1 bg-muted rounded-full"></div>
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-muted text-muted-foreground rounded-full flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <span className="text-sm font-medium text-muted-foreground">Hostel Selection</span>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {!showForm && (
              <div className="space-y-6">
                {/* Eligibility Check */}
                <div className="p-4 bg-muted/50 rounded-lg border border-border/50">
                  <div className="flex items-start gap-3">
                    <Shield className="h-5 w-5 text-primary mt-0.5" />
                    <div>
                      <h3 className="font-semibold text-foreground mb-1">Eligibility Check</h3>
                      <p className="text-sm text-muted-foreground">
                        You are eligible for free hostel accommodation as a long distance student.
                      </p>
                    </div>
                  </div>
                </div>

                {/* Important Information */}
                <Alert className="border-primary/20 bg-primary/5">
                  <InfoIcon className="h-5 w-5 text-primary" />
                  <AlertDescription className="text-foreground">
                    <strong>Free Hostel Accommodation:</strong> You will be provided free hostel accommodation. 
                    After route confirmation, you'll be able to select your preferred hostel and verify with OTP.
                  </AlertDescription>
                </Alert>

                                 {/* Available Routes */}
                 {routesLoading ? (
                   <div className="space-y-3">
                     <h3 className="text-lg font-semibold text-foreground">Available Routes</h3>
                     <div className="space-y-2">
                       <Skeleton className="h-12 w-full" />
                       <Skeleton className="h-12 w-full" />
                       <Skeleton className="h-12 w-full" />
                       <Skeleton className="h-12 w-full" />
                       <Skeleton className="h-12 w-full" />
                     </div>
                   </div>
                 ) : routes && routes.length > 0 ? (
                   <div className="space-y-3">
                     <h3 className="text-lg font-semibold text-foreground">Available Routes ({routes.length})</h3>
                     <ScrollArea className="h-64 border rounded-lg p-3 bg-muted/30">
                       <div className="space-y-2">
                         {routes.map(route => (
                           <div key={route.id} className="flex items-center gap-3 p-3 bg-background rounded-md border border-border/50 hover:bg-muted/50 transition-colors">
                             <div className="w-8 h-8 bg-primary/10 text-primary rounded-full flex items-center justify-center text-sm font-bold">
                               {route.bus_route_no}
                             </div>
                             <span className="text-sm font-medium text-foreground">{route.bus_route_name}</span>
                           </div>
                         ))}
                       </div>
                     </ScrollArea>
                   </div>
                 ) : (
                   <div className="text-center text-muted-foreground py-4">
                     <Bus className="h-12 w-12 mx-auto mb-3 opacity-50" />
                     <p>No routes available at the moment.</p>
                   </div>
                 )}

                {/* Action Buttons */}
                <div className="flex gap-4 justify-center pt-4">
                  <Button 
                    onClick={() => setShowForm(true)}
                    className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-3"
                    size="lg"
                  >
                    <CheckCircle className="h-5 w-5 mr-2" />
                    Continue to Route Selection
                  </Button>
                  <Button 
                    onClick={() => navigate('/')} 
                    variant="outline" 
                    className="px-8 py-3"
                    size="lg"
                  >
                    <ArrowLeft className="h-5 w-5 mr-2" />
                    Go Back
                  </Button>
                </div>
              </div>
            )}
            
            {showForm && (
              <form
                onSubmit={e => {
                  e.preventDefault();
                  if (selectedRoute) {
                    submitMutation.mutate({ route: Number(selectedRoute) });
                  } else {
                    toast.error('Please select a route');
                  }
                }}
                className="space-y-6"
              >
                {/* Form Header */}
                <div className="text-center space-y-2">
                  <h3 className="text-xl font-semibold text-foreground">Select Your Route</h3>
                  <p className="text-sm text-muted-foreground">
                    Choose the bus route that you use to travel to college
                  </p>
                </div>

                {/* Route Selection */}
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-foreground">Bus Route</label>
                    <Select value={selectedRoute} onValueChange={setSelectedRoute}>
                      <SelectTrigger className="w-full h-12 text-base border-2 focus:border-primary">
                        <SelectValue placeholder="Select your bus route" />
                      </SelectTrigger>
                      <SelectContent>
                        <ScrollArea className="h-64">
                          {routes && routes.map(route => (
                            <SelectItem key={route.id} value={route.id.toString()}>
                              <div className="flex items-center gap-3">
                                <div className="w-6 h-6 bg-primary/10 text-primary rounded-full flex items-center justify-center text-xs font-bold">
                                  {route.bus_route_no}
                                </div>
                                <span>{route.bus_route_name}</span>
                              </div>
                            </SelectItem>
                          ))}
                        </ScrollArea>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Next Steps Preview */}
                <div className="p-4 bg-muted/50 rounded-lg border border-border/50">
                  <h4 className="font-semibold text-foreground mb-2">Next Steps:</h4>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      <span>Select your preferred hostel</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Shield className="h-4 w-4" />
                      <span>Verify selection with OTP</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4" />
                      <span>Contact SAO for final allocation</span>
                    </div>
                  </div>
                </div>
                
                <CardFooter className="flex flex-col space-y-4 pt-4">
                  <Button
                    type="submit"
                    className="w-full h-12 text-base font-medium"
                    disabled={submitMutation.isPending || !selectedRoute}
                  >
                    {submitMutation.isPending ? (
                      <>
                        <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                        Submitting...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="h-5 w-5 mr-2" />
                        Confirm Route & Continue
                      </>
                    )}
                  </Button>
                  
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowForm(false)}
                    className="w-full h-10"
                  >
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Back to Overview
                  </Button>
                </CardFooter>
              </form>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  return null;
};

export default SpecialFormPage;