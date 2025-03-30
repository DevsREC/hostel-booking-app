from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authentication.authentication import IsAuthenticated
from .serializers import HostelSerializer

from .models import *

# Create your views here.
class InitiateBookingAPI(generics.CreateAPIView):
    authentication_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, hostel_id):
        hostel = get_object_or_404(Hostel, id=hostel_id, enable=True)
        print(request.user.id)
        if RoomBooking.objects.filter(
            user = request.user,
            status__in = ['otp_pending', 'payment_pending', 'confirmed']
        ).exists():
            booking = RoomBooking.objects.get(user=request.user)
            return Response(
                {
                    "message": "You have already booked a hostel",
                    "data": {
                        "booking_id": booking.id
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not hostel.is_available():
            return Response(
                {
                    "message": "No rooms available"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking = RoomBooking.objects.create(
            user = request.user,
            hostel = hostel
        )

        booking.generate_otp()

        return Response(
            {
                "message": "OTP sent to your email",
                "booking_id": booking.id
            },
            status=status.HTTP_201_CREATED
        )
    
class VerifyOTPApi(generics.CreateAPIView):
    authentication_classes=[IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)
        otp_code = request.data.get('otp_code')

        if not otp_code:
            return Response(
                {
                    "message": "OTP code is missing"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.verify_otp(otp_code):
            return Response(
                {
                    "message": "OTP Verified",
                    "payment_instructions": "Check your email for payment details",
                    "payment_link": booking.payment_link,
                    "expires_at": booking.payment_expiry
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Invalid/OTP Expired"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class GetHostelDataAPI(generics.CreateAPIView):
    authentication_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HostelSerializer
    queryset = Hostel.objects.filter(enable=True)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Fetched data successfully",
            "data": serializer.data
        })