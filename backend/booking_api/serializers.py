from rest_framework import serializers
from .models import User, Hostel, BookingOTP, Booking
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'year', 'dept', 
                  'roll_number', 'email', 'phone_number', 'parent_phone_number', 
                  'role', 'gender', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'

class BookingOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingOTP
        fields = '__all__'
        read_only_fields = ['is_expired', 'is_validated', 'created_at', 'expires_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booked_at', 'payment_verified_by']
