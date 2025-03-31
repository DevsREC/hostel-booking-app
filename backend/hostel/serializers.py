from rest_framework import serializers
from .models import *
from authentication.serializers import UserSerializer

class HostelSerializer(serializers.ModelSerializer):
    available_rooms = serializers.SerializerMethodField()

    class Meta:
        model = Hostel
        fields =  ['id', 'name', 'location', 'room_type', 'food_type', 'gender', 
                  'person_per_room', 'no_of_rooms', 'total_capacity', 
                  'room_description', 'amount', 'image', 'available_rooms']
    
    def get_available_rooms(self, obj):
        return obj.available_rooms()
    
class RoomBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hostel = HostelSerializer(read_only=True)

    class Meta:
        model = RoomBooking
        fields = ['id', 'user', 'hostel', 'status', 'payment_expiry']