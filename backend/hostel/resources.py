from import_export import resources
from .models import *
from unfold.admin import ModelAdmin

class RoomBookingResource(resources.ModelResource):
    class Meta:
        model = RoomBooking
        fields = ['user', 'hostel', 'status', 'booked_at', 'otp_verified_at', 'payment_completed_at', 'payment_link', 'payment_reference', 'otp_code', 'otp_expiry', 'payment_expiry', 'admin_notes', 'verified_by']

class HostelResource(resources.ModelResource):
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'room_type', 'food_type', 'gender', 'person_per_room', 'no_of_rooms', 'total_capacity', 'room_description', 'enable', 'bathroom_type', 'first_year_fee_mgmt', 'first_year_fee_govt', 'second_year_fee_mgmt', 'second_year_fee_govt', 'third_year_fee_mgmt', 'third_year_fee_govt', 'fourth_year_fee_mgmt', 'fourth_year_fee_govt']