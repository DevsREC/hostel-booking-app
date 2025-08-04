from import_export import resources, fields
from .models import *
from unfold.admin import ModelAdmin

class RoomBookingResource(resources.ModelResource):
    amount = fields.Field(column_name='Amount', attribute='amount')
    
    class Meta:
        model = RoomBooking
        import_id_fields = ['user__roll_no']
        fields = ['user__roll_no', 'user__email', 'user__first_name', 'user__last_name', 
                'user__gender', 'food_type', 'hostel__name', 'status', 'booked_at', 
                'otp_verified_at', 'otp_code', 'otp_expiry', 'amount', 
                'is_payment_link_sent', 'payment_expiry', 'verified_by']
        skip_unchanged = True

    def dehydrate_amount(self, obj):
        return obj.get_amount()

    def get_instance(self, instance_loader, row):
        """Override to find only payment_pending bookings"""
        try:
            user = User.objects.get(roll_no=row.get('user__roll_no'))
            # Find only payment_pending bookings for this user
            return RoomBooking.objects.filter(
                user=user,
                status='payment_pending'
            ).first()  # Get the first matching pending booking
        except (User.DoesNotExist, RoomBooking.DoesNotExist):
            return None

    def before_import_row(self, row, **kwargs):
        """Mark instance as being imported"""
        row['_importing'] = True
        # Normalize status
        if 'status' in row:
            row['status'] = row['status'].strip().lower()

    def before_save_instance(self, instance, row=None, **kwargs):
        """
        Ensure we only process valid imports
        Note: Changed signature to match what django-import-export actually passes
        """
        if getattr(instance, '_importing', False):
            instance._importing = True
            # Only allow status change from payment_pending to confirmed
            if instance.status != 'payment_pending':
                raise ValueError("Can only confirm payment_pending bookings")
   
class HostelResource(resources.ModelResource):
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'room_type', 'food_type', 'gender', 'person_per_room', 'no_of_rooms', 'total_capacity', 'room_description', 'enable', 'bathroom_type', 'first_year_fee_mgmt_veg', 'first_year_fee_mgmt_non_veg', 'first_year_fee_govt_veg', 'first_year_fee_govt_non_veg', 'second_year_fee_mgmt_veg', 'second_year_fee_mgmt_non_veg', 'second_year_fee_govt_veg', 'second_year_fee_govt_non_veg','third_year_fee_mgmt_veg','third_year_fee_mgmt_non_veg',
        'third_year_fee_govt_veg','third_year_fee_govt_non_veg', 'fourth_year_fee_mgmt_veg','fourth_year_fee_mgmt_non_veg', 'fourth_year_fee_govt_veg', 'fourth_year_fee_govt_non_veg']
        
        
class LongDistanceRoutesResources(resources.ModelResource):
    class Meta:
        model = LongDistanceRoutes
        fields = ['bus_route_no', 'bus_route_name']
        import_id_fields = ['bus_route_no']