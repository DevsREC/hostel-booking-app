from import_export import resources, fields
from .models import *
from unfold.admin import ModelAdmin

class RoomBookingResource(resources.ModelResource):
    amount = fields.Field(column_name='Amount', attribute='amount')
    class Meta:
        model = RoomBooking
        fields = ['user', 'user__email', 'user__first_name', 'user__last_name', 'hostel', 'hostel__name', 'status', 'booked_at', 'otp_verified_at', 'otp_code', 'otp_expiry', 'amount', 'is_payment_link_sent', 'payment_expiry', 'verified_by']

    def dehydrate_amount(self, obj):
        return obj.get_amount()

class HostelResource(resources.ModelResource):
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'room_type', 'food_type', 'gender', 'person_per_room', 'no_of_rooms', 'total_capacity', 'room_description', 'enable', 'bathroom_type', 'first_year_fee_mgmt', 'first_year_fee_govt', 'second_year_fee_mgmt', 'second_year_fee_govt', 'third_year_fee_mgmt', 'third_year_fee_govt', 'fourth_year_fee_mgmt', 'fourth_year_fee_govt']