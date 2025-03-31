from django.contrib import admin
from authentication.utils import send_email
from .models import *
from column_toggle.admin import ColumnToggleModelAdmin
from import_export.admin import ExportActionModelAdmin
from .models import RoomBooking
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .resources import *

INTERNAL_RESERVATION_PERCENT = 25

# Register your models here.
@admin.register(Hostel)
class HostelAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'enable', 'location', 'room_type', 'food_type','person_per_room', 'no_of_rooms', 'total_capacity', 'gender')
    list_filter = ('location', 'gender', 'room_type', 'food_type')
    resource_classes = [HostelResource]



@admin.register(RoomBooking)
class RoomBookingAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'hostel', 'status', 'booked_at', 'verified_by')
    readonly_fields = ('verified_by',)
    list_filter = ('status', 'hostel',)
    actions = ['confirm_payment', 'cancel_booking']
    resource_classes = [RoomBookingResource]

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
    list_display = ['name', 'location', 'gender', 'room_type', 'food_type', 'person_per_room', 'total_capacity', 'rooms_booked', 'rooms_available', 'reserved_capacity']
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
        return RoomBooking.objects.filter(hostel=hostel, status__in=['confirmed', 'payment_verified', 'payment_pending']).count()
    
    def rooms_booked(self, hostel: Hostel):
        no_of_rooms_booked = self.booking_count(hostel)
        return str(no_of_rooms_booked)
    
    def rooms_available(self, hostel: Hostel):
        booked_room_count = self.booking_count(hostel)
        remaining_capacity = hostel.total_capacity - booked_room_count
        return remaining_capacity
    
    # def reserved_heads(self):
    #     booked_rooms = RoomBooking.objects.filter(
    #         hostel=self.hostel, 
    #         status__in=['confirmed', 'payment_pending', 'otp_pending']
    #     ).count()
        
    #     total_available = self.total_capacity - booked_rooms
    #     internal_reserved = int(self.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
        
    #     return min(total_available, internal_reserved)

    def reserved_capacity(self, hostel: Hostel):
        return int(hostel.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
    
class PaymentManagement(RoomBooking):
    class Meta:
        proxy = True
        verbose_name = "Payment Management"
        verbose_name_plural = "Payment Management"

@admin.register(PaymentManagement)
class PaymentManagementAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_gender', 'hostel_name', 'amount', 'payment_reference', 'payment_status', 'payment_actions')
    list_filter = ('status', 'hostel')
    search_fields = ('user__email', 'user__first_name', 'hostel__name', 'payment_reference')
    readonly_fields = ('user', 'hostel', 'user_gender', 'hostel_name', 'amount', 'status', 'payment_expiry')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status__in=['payment_pending', 'otp_pending'])
        
    def user_gender(self, obj):
        return obj.user.gender
    user_gender.short_description = 'Gender'
    
    def hostel_name(self, obj):
        return obj.hostel.name
    hostel_name.short_description = 'Hostel'
    
    def amount(self, obj):
        return f"₹{obj.hostel.amount}"
    amount.short_description = 'Amount'

    def payment_status(self, obj):
        if obj.status == 'payment_pending':
            return format_html('<span style="color: orange; font-weight: bold;">Pending</span>')
        elif obj.status == 'payment_verified':
            return format_html('<span style="color: blue; font-weight: bold;">Verified</span>')
        else:
            return obj.get_status_display()
    payment_status.short_description = 'Status'

    def payment_actions(self, obj):
        if obj.status == 'payment_pending':
            confirm_url = reverse('admin:confirm_payment', args=[obj.pk])
            reject_url = reverse('admin:reject_payment', args=[obj.pk])
            return format_html(
                '<a class="button" style="background-color: green; color: white; padding: 3px 8px; '
                'border-radius: 4px; text-decoration: none; margin-right: 5px;" href="{}">Confirm</a>'
                '<a class="button" style="background-color: red; color: white; padding: 3px 8px; '
                'border-radius: 4px; text-decoration: none;" href="{}">Reject</a>',
                confirm_url, reject_url
            )
        return "Already processed"
    payment_actions.short_description = 'Actions'

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return obj is None
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/confirm/',
                self.admin_site.admin_view(self.confirm_payment),
                name='confirm_payment',
            ),
            path(
                '<path:object_id>/reject/',
                self.admin_site.admin_view(self.reject_payment),
                name='reject_payment',
            ),
        ]
        return custom_urls + urls
    
    def confirm_payment(self, request, object_id):
        booking = self.get_object(request, object_id)
        if booking:
            booking.update_status('confirmed', verified_by_user=request.user)
            self.send_confirmation_email(booking)
        return HttpResponseRedirect(reverse('admin:hostel_paymentmanagement_changelist'))

    def reject_payment(self, request, object_id):
        booking = self.get_object(request, object_id)
        if booking:
            booking.update_status('payment_not_done', verified_by_user=request.user)
            self.send_rejection_email(booking)
        return HttpResponseRedirect(reverse('admin:hostel_paymentmanagement_changelist'))

    def send_confirmation_email(self, booking):
        subject = "Hostel Booking - Payment Confirmed"
        
        message = f"""
            <p><strong>Good news!</strong> Your payment for the hostel booking has been <span style="color: green;"><strong>confirmed</strong></span>.</p>
            
            <h3>Booking Details:</h3>
            <div class="details">
                <p><strong>Hostel:</strong> {booking.hostel.name}</p>
                <p><strong>Room Type:</strong> {booking.hostel.room_type}</p>
                <p><strong>Food Type:</strong> {booking.hostel.food_type}</p>
                <p><strong>Amount Paid:</strong> ₹{booking.hostel.amount}</p>
            </div>
            
            <p>Your booking is now confirmed. Please keep this email for your records.</p>
        """
        
        send_email(
            subject=subject,
            to_email=booking.user.email,
            context={"startingcontent": message}
        )

    
    def send_rejection_email(self, booking):
        subject = "Hostel Booking - Payment Rejected"
        
        message = f"""
            <p><strong>We regret to inform you</strong> that your payment for the hostel booking could not be verified.</p>
            
            <h3>Booking Details:</h3>
            <div class="details">
                <p><strong>Hostel:</strong> {booking.hostel.name}</p>
                <p><strong>Room Type:</strong> {booking.hostel.room_type}</p>
                <p><strong>Amount:</strong> ₹{booking.hostel.amount}</p>
            </div>
            
            <h3>Possible reasons for rejection:</h3>
            <ul>
                <li>Payment reference not found</li>
                <li>Incorrect amount paid</li>
                <li>Payment timeout</li>
            </ul>
            
            <p>Please contact the hostel administration for more information or to make a new booking.</p>
        """
        
        send_email(
            subject=subject,
            to_email=booking.user.email,
            context={"startingcontent": message}
        )
