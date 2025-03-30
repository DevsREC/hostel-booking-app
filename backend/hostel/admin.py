from django.contrib import admin
from authentication.utils import send_email
from .models import *

# Register your models here.
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'location', 'room_type', 'food_type','person_per_room', 'no_of_rooms', 'total_capacity', 'gender')
    list_filter = ('location', 'gender', 'room_type', 'food_type')

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostel', 'status', 'booked_at')
    list_filter = ('status', 'hostel',)
    actions = ['confirm_payment', 'cancel_booking']

    def confirm_payment(self, request, queryset):
        queryset.filter(status='payment_verified').update(status='confirmed')
        self.message_user(request, "Selected bookings confirmed")
    confirm_payment.short_description = "Confirm payment for selected bookings"
    
    def cancel_booking(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, "Selected bookings cancelled")
    cancel_booking.short_description = "Cancel selected bookings"