from import_export import resources, fields
from .models import *
from unfold.admin import ModelAdmin

class RoomBookingResource(resources.ModelResource):
    amount = fields.Field(column_name='Amount', attribute='amount')
    class Meta:
        model = RoomBooking
        fields = ['user__roll_no', 'user__email', 'user__first_name', 'user__last_name', 'user__gender','food_type', 'hostel__name', 'status', 'booked_at', 'otp_verified_at', 'otp_code', 'otp_expiry', 'amount', 'is_payment_link_sent', 'payment_expiry', 'verified_by']

    def dehydrate_amount(self, obj):
        return obj.get_amount()

class HostelResource(resources.ModelResource):
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'room_type', 'food_type', 'gender', 'person_per_room', 'no_of_rooms', 'total_capacity', 'room_description', 'enable', 'bathroom_type', 'first_year_fee_mgmt_veg', 'first_year_fee_mgmt_non_veg', 'first_year_fee_govt_veg', 'first_year_fee_govt_non_veg', 'second_year_fee_mgmt_veg', 'second_year_fee_mgmt_non_veg', 'second_year_fee_govt_veg', 'second_year_fee_govt_non_veg','third_year_fee_mgmt_veg','third_year_fee_mgmt_non_veg',
        'third_year_fee_govt_veg','third_year_fee_govt_non_veg', 'fourth_year_fee_mgmt_veg','fourth_year_fee_mgmt_non_veg', 'fourth_year_fee_govt_veg', 'fourth_year_fee_govt_non_veg']