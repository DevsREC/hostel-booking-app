from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Hostel, BookingOTP, Booking
from .serializers import UserSerializer, HostelSerializer, BookingOTPSerializer, BookingSerializer
import random
from datetime import datetime, timedelta
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    
    @action(detail=False, methods=['get'])
    def by_gender(self, request):
        gender = request.query_params.get('gender', None)
        if gender:
            hostels = Hostel.objects.filter(gender=gender)
            serializer = self.get_serializer(hostels, many=True)
            return Response(serializer.data)
        return Response([])

class BookingOTPViewSet(viewsets.ModelViewSet):
    queryset = BookingOTP.objects.all()
    serializer_class = BookingOTPSerializer
    
    @action(detail=False, methods=['post'])
    def generate_otp(self, request):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            BookingOTP.objects.filter(user=user, is_expired=False).update(is_expired=True)
            
            otp = str(random.randint(100000, 999999))
            expires_at = timezone.now() + timedelta(minutes=30)
            
            otp_obj = BookingOTP.objects.create(
                user=user,
                otp=otp,
                expires_at=expires_at
            )
            print(f"OTP for {user.email}: {otp}")
            
            return Response({
                'message': 'OTP generated successfully',
                'otp_id': otp_obj.id
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def validate_otp(self, request):
        otp_id = request.data.get('otp_id')
        otp_code = request.data.get('otp')
        
        try:
            otp_obj = BookingOTP.objects.get(pk=otp_id, is_expired=False)
            
            if otp_obj.expires_at < timezone.now():
                otp_obj.is_expired = True
                otp_obj.save()
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
                
            if otp_obj.otp == otp_code:
                otp_obj.is_validated = True
                otp_obj.save()
                return Response({'message': 'OTP validated successfully'})
            
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except BookingOTP.DoesNotExist:
            return Response({'error': 'Invalid OTP ID or OTP has expired'}, status=status.HTTP_404_NOT_FOUND)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        has_valid_otp = BookingOTP.objects.filter(
            user_id=user_id,
            is_validated=True,
            is_expired=False
        ).exists()
        
        if not has_valid_otp:
            return Response(
                {'error': 'You must validate an OTP before booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.data['payment_deadline'] = (timezone.now() + timedelta(hours=24)).isoformat()
        
        return super().create(request, *args, **kwargs)