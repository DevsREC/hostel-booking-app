from django.contrib import admin
from authentication.utils import send_email
from .models import *
from column_toggle.admin import ColumnToggleModelAdmin

# Register your models here.
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'location', 'room_type', 'food_type','person_per_room', 'no_of_rooms', 'total_capacity', 'gender')
    list_filter = ('location', 'gender', 'room_type', 'food_type')

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hostel', 'status', 'booked_at', 'verified_by')
    readonly_fields = ('verified_by',)
    list_filter = ('status', 'hostel',)
    actions = ['confirm_payment', 'cancel_booking']

    def save_model(self, request, obj, form, change):
        if change:
            original_obj = self.model.objects.get(pk=obj.pk)
            
            if original_obj.status != obj.status:
                obj.verified_by = request.user
                
        super().save_model(request, obj, form, change)
    def confirm_payment(self, request, queryset):
        queryset.filter(status='payment_verified').update(status='confirmed')
        self.message_user(request, "Selected bookings confirmed")
    confirm_payment.short_description = "Confirm payment for selected bookings"
    
    def cancel_booking(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, "Selected bookings cancelled")
    cancel_booking.short_description = "Cancel selected bookings"

class RoomStats(Hostel):
    class Meta:
        proxy = True

@admin.register(RoomStats)
class RoomBookingStats(ColumnToggleModelAdmin):
    list_display = ['name', 'location', 'gender', 'room_type', 'food_type', 'person_per_room', 'total_capacity', 'rooms_booked', 'rooms_available']
    default_selected_columns=list_display
    search_fields = ['name']
    list_filter = ['name', 'location', 'gender', 'room_type', 'food_type']

    def has_view_permission(self, request, obj = ...):
        return True
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj = ...):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False
    
    def booking_count(self, hostel):
        return RoomBooking.objects.filter(hostel=hostel, status__in=['confirmed', 'payment_verified']).count()
    
    def rooms_booked(self, hostel: Hostel):
        no_of_rooms_booked = self.booking_count(hostel)
        return str(no_of_rooms_booked)
    
    def rooms_available(self, hostel: Hostel):
        booked_room_count = self.booking_count(hostel)
        remaining_capacity = hostel.total_capacity - booked_room_count
        return remaining_capacity