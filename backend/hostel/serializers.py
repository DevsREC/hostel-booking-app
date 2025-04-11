from rest_framework import serializers
from .models import *
from authentication.serializers import UserSerializer

class HostelSerializer(serializers.ModelSerializer):
    available_rooms = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Hostel
        fields =  ['id', 'name', 'location', 'room_type', 'food_type', 'gender', 
                  'person_per_room', 'no_of_rooms', 'total_capacity', 
                  'room_description', 'image', 'available_rooms', 'amount', 'bathroom_type']
    
    def get_amount(self, obj):
        year = self.context.get('year')
        
        if year == 1:
            return obj.first_year_fee
        elif year == 2:
            return obj.second_year_fee
        elif year == 3:
            return obj.third_year_fee
        elif year == 4:
            return obj.fourth_year_fee
        
        return obj.first_year_fee

    def get_available_rooms(self, obj):
        return obj.available_rooms()
    
class RoomBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hostel = HostelSerializer(read_only=True)

    class Meta:
        model = RoomBooking
        fields = ['id', 'user', 'hostel', 'status', 'payment_expiry', "booked_at"]