from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authentication.authentication import IsAuthenticated
from .serializers import *

from .models import *
from authentication.models import BlockedStudents

# Create your views here.
class InitiateBookingAPI(generics.CreateAPIView):
    authentication_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, hostel_id):
        try:
            hostel = get_object_or_404(Hostel, id=hostel_id, enable=True)
            user = User.objects.filter(email=request.user).first()
            food_type = request.data.get('food_type')

            if not food_type or food_type.lower() not in ['veg', 'non_veg']:
                return Response(
                    {
                        'detail': "Invalid food type",
                        'code': 'wrong_food_type'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            food_type = 'Veg' if food_type.lower() == 'veg' else 'Non_veg'

            is_blocked = BlockedStudents.objects.filter(email=user.email).exists()
            if is_blocked:
                return Response({
                    'detail': 'No account found with this email. If you think it\'s a mistake, please contact the admin.',
                    'code': 'user_not_found'
                }, status=status.HTTP_401_UNAUTHORIZED)
            print("Bookings")
            print(RoomBooking.objects.filter(user=user).exclude(status__in=['payment_not_done', 'cancelled']))
            if RoomBooking.objects.filter(
                user = user,
            ).exclude(status__in=['payment_not_done', 'cancelled']).exists():
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
            print("Food Type: ", food_type)
            booking = RoomBooking.objects.create(
                user = request.user,
                hostel = hostel,
                food_type = food_type
            )
            booking.generate_otp()
            return Response(
                {
                    "message": "OTP sent to your email",
                    "booking_id": booking.id
                },
                status=status.HTTP_201_CREATED
            )

        except IntegrityError as e:
            return Response(
                {
                    "message": "An failed booking for the hostel has been found, cancel that booking book this again"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print(e)
            return Response(
                {
                    "message": "Something went wrong, try again later!"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetBookingAPI(generics.CreateAPIView):
    authentication_classes=[IsAuthenticated]
    permission_classes=[permissions.IsAuthenticated]    
    serializer_class = RoomBookingSerializer

    def get(self, request):
        try:
            user = User.objects.get(email = request.user)
            bookings = RoomBooking.objects.filter(user=user)
            serializer = self.serializer_class(bookings, many=True, context={"year": user.year, "quota": user.student_type})
            return Response(
                {
                    "message": "Success!",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except RoomBooking.DoesNotExist:
            return Response(
                {
                    "message": "No bookings found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            print(e)
            return Response(
                {
                    "message": "An error occurred while cancelling the booking"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CancelBookingAPI(generics.CreateAPIView):
    authentication_classes=[IsAuthenticated]
    permission_classes=[permissions.IsAuthenticated]

    def delete(self, request):
        try:
            booking_id = request.data.get('booking_id')
            if booking_id:
                booking = RoomBooking.objects.get(id=booking_id, user=request.user)
                if booking.status in ['confirmed', 'payment_pending', 'payment_not_done', 'cancelled']:
                    return Response(
                        {
                            "message": "Booking can't be cancelled"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                booking.delete()
                return Response(
                    {
                        "message": "Booking cancelled successfully"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "Booking ID is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except RoomBooking.DoesNotExist:
            return Response(
                {
                    "message": "No bookings found or payment has been confirmed"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:  
            print(e)
            return Response(
                {
                    "message": "An error occurred while cancelling the booking"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyOTPApi(generics.CreateAPIView):
    authentication_classes=[IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user)
        otp_code = request.data.get('otp_code')

        print("OTP Code:", otp_code)
        # print("")
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
    # queryset = Hostel.objects.filter(enable=True)

    def get_queryset(self):
        user = self.request.user
        queryset = Hostel.objects.filter(enable=True, gender__in=[user.gender])

        return queryset

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        is_blocked = BlockedStudents.objects.filter(email=user.email).exists()
        if is_blocked:
            return Response({
                'detail': 'No account found with this email. If you think it\'s a mistake, please contact the admin.',
                'code': 'user_not_found'
            }, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={"year": user.year, "quota": user.student_type})
        print(serializer.data)
        return Response({
            "message": "Fetched data successfully",
            "data": serializer.data
        })