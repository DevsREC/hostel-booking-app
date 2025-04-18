from django.contrib import admin
from authentication.utils import send_email
from .models import *
from column_toggle.admin import ColumnToggleModelAdmin
from import_export.admin import ExportActionModelAdmin, ImportExportActionModelAdmin
from .models import RoomBooking
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .resources import *
from unfold.admin import ModelAdmin

INTERNAL_RESERVATION_PERCENT = 25

# Register your models here.
@admin.register(Hostel)
class HostelAdmin(ImportExportActionModelAdmin, ModelAdmin):
    list_display = ('id', 'name', 'enable', 'location', 'room_type', 'is_veg', 'is_non_veg','person_per_room', 'no_of_rooms' ,'total_capacity', 'gender')
    list_filter = ('location', 'gender', 'room_type')
    list_search = ('name', 'location')
    resource_classes = [HostelResource]
# 'mgmt_amount', 'govt_amount'
    def mgmt_amount(self, obj):
        return format_html(
            '<p class="text-xs">1 - ₹{}</p>'
            '<p class="text-xs">2 - ₹{}</p>'
            '<p class="text-xs">3 - ₹{}</p>'
            '<p class="text-xs">4 - ₹{}</p>',
            obj.first_year_fee_mgmt,
            obj.second_year_fee_mgmt,
            obj.third_year_fee_mgmt,
            obj.fourth_year_fee_mgmt,
        )

    def govt_amount(self, obj):
        return format_html(
            '<p class="text-xs">1 - ₹{}</p>'
            '<p class="text-xs">2 - ₹{}</p>'
            '<p class="text-xs">3 - ₹{}</p>'
            '<p class="text-xs">4 - ₹{}</p>',
            obj.first_year_fee_govt,
            obj.second_year_fee_govt,
            obj.third_year_fee_govt,
            obj.fourth_year_fee_govt,
        )

@admin.register(RoomBooking)
class RoomBookingAdmin(ExportActionModelAdmin, ModelAdmin):
    list_display = ('user', 'hostel', 'status', 'booked_at','food_type', 'amount', 'verified_by',)
    readonly_fields = ('verified_by',)
    list_filter = ('status', 'hostel', 'hostel__location')
    search_fields = ('user__first_name', 'hostel__name', 'verified_by__first_name')
    # actions = ['confirm_payment',   'cancel_booking']
    resource_classes = [RoomBookingResource]
    
    def amount(self, obj):
        return obj.get_amount()

    def save_model(self, request, obj, form, change):
        if change:
            original_obj = self.model.objects.get(pk=obj.pk)
            
            if original_obj.status != obj.status:
                obj.verified_by = request.user
        super().save_model(request, obj, form, change)

    # def confirm_payment(self, request, queryset):
    #     queryset.filter(status='payment_verified').update(status='confirmed')
    #     self.message_user(request, "Selected bookings confirmed")
    # confirm_payment.short_description = "Confirm payment for selected bookings"
    
    # def cancel_booking(self, request, queryset):
    #     queryset.update(status='cancelled')
    #     self.message_user(request, "Selected bookings cancelled")
    # cancel_booking.short_description = "Cancel selected bookings"

class RoomStats(Hostel):
    class Meta:
        proxy = True

@admin.register(RoomStats)
class RoomBookingStats(ColumnToggleModelAdmin):
    list_display = ['name', 'location', 'gender', 'room_type', 'person_per_room', 'total_capacity', 'rooms_booked', 'rooms_available', 'reserved_capacity']
    default_selected_columns=list_display
    search_fields = ['name']
    list_filter = ['name', 'location', 'gender', 'room_type']

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
        # booked_room_count = self.booking_count(hostel)

        # remaining_capacity = hostel.total_capacity - booked_room_count
        # return remaining_capacity
        booked_rooms = RoomBooking.objects.filter(
            hostel=hostel, 
            status__in=['confirmed', 'payment_verified', 'payment_pending']
        ).count()   

        total_available = hostel.total_capacity - booked_rooms
        internal_reserved = int(hostel.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
        online_available = total_available - internal_reserved

        return max(0, online_available)
    
    # def reserved_heads(self):
    #     booked_rooms = RoomBooking.objects.filter(
    #         hostel=self.hostel, 
    #         status__in=['confirmed', 'payment_pending', 'otp_pending']
    #     ).count()
        
    #     total_available = self.total_capacity - booked_rooms
    #     internal_reserved = int(self.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
        
    #     return min(total_available, internal_reserved)

    def reserved_capacity(self, hostel: Hostel):
        booked_rooms = RoomBooking.objects.filter(
            hostel=hostel, 
            status__in=['confirmed', 'payment_pending', 'otp_pending']
        ).count()
        
        total_available = hostel.total_capacity - booked_rooms
        internal_reserved = int(hostel.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
        
        return min(total_available, internal_reserved)
class PaymentManagement(RoomBooking):
    class Meta:
        proxy = True
        verbose_name = "Payment Management"
        verbose_name_plural = "Payment Management"

@admin.register(PaymentManagement)
class PaymentManagementAdmin(ExportActionModelAdmin, ModelAdmin):
    list_display = ('user', 'user_year', 'student_type', 'user_gender', 'hostel_name', 'is_payment_link_sent', 'amount', 'payment_status', 'payment_actions')
    list_filter = ('status', 'hostel', 'status')
    search_fields = ('user__email', 'user__first_name', 'hostel__name', 'payment_reference')
    readonly_fields = ('user', 'hostel', 'user_gender', 'hostel_name', 'amount', 'status', 'payment_expiry')
    resource_classes = [RoomBookingResource]
    actions = ['set_sent_payment_mail']

    def set_sent_payment_mail(self, request, queryset):
        updated = queryset.filter(status='payment_pending').update(is_payment_link_sent=True)
        self.message_user(
            request,
            f"Successfully marked {updated} payment{'s' if updated != 1 else ''} as mail sent",
        )
    set_sent_payment_mail.short_description = 'Mark selected as payment mail sent'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status__in=['payment_pending', 'otp_pending'])
        
    def user_gender(self, obj):
        return obj.user.gender
    user_gender.short_description = 'Gender'

    def user_year(self, obj):
        return obj.user.year
    user_year.short_description = 'Year'
    
    def hostel_name(self, obj):
        return obj.hostel.name
    hostel_name.short_description = 'Hostel'

    def student_type(self, obj):
        return obj.user.student_type
    
    def amount(self, obj):
        return obj.get_amount()
    amount.short_description = 'Amount'

    def payment_status(self, obj):
        if obj.status == 'payment_pending':
            return format_html('<span class="badge badge-soft badge-error">Pending</span>')
        elif obj.status == 'payment_verified':
            return format_html('<span class="badge badge-soft badge-success">Verified</span>')
        else:
            return obj.get_status_display()
    payment_status.short_description = 'Status'

    def payment_actions(self, obj):
        if obj.status == 'payment_pending':
            confirm_url = reverse('admin:confirm_payment', args=[obj.pk])
            reject_url = reverse('admin:reject_payment', args=[obj.pk])
            return format_html(
                '<div>'
                '<a style="padding: 4px 8px; background-color: rgba(168, 85, 247, .4); color: rgb(168, 85, 247); border-radius: 4px; margin: 2px 4px;" href="{}">Confirm</a>'
                '<a style="padding: 4px 8px; background-color: rgba(239, 68, 68, .4); color: rgba(239, 68, 68, 1); border-radius: 4px; margin: 2px 4px;" href="{}">Reject</a>'
                '</div>',
                confirm_url, reject_url
            )
        elif obj.status == 'otp_pending':
            return "Verification Pending"
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
        try:
            booking = self.get_object(request, object_id)
            if booking:
                booking.update_status('cancelled', verified_by_user=request.user)
                self.send_rejection_email(booking)
            return HttpResponseRedirect(reverse('admin:hostel_paymentmanagement_changelist'))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('admin:hostel_paymentmanagement_changelist'))
        

    def send_confirmation_email(self, booking):
        subject = "Booking Confirmed - Your Stay is Ready!"
        to_email = booking.user.email
        
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "user_name": booking.user.first_name or "Valued Guest",
                "hostel_name": booking.hostel.name,
                "room_type": booking.hostel.room_type,
                "food_type": booking.food_type,
            },
            template_name="booking_confirmation_template.html"
        )

    
    def send_rejection_email(self, booking):
        subject = "Important Update on Your Hostel Booking Payment"
        to_email = booking.user.email
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "user_name": booking.user.first_name or "Valued Guest",
                "hostel_name": booking.hostel.name,
                "room_type": booking.hostel.room_type,
            },
            template_name="payment_rejection_template.html"
        )

@admin.register(Penalty)
class PenaltyAdmin(ModelAdmin):
    list_display = ['user', 'hostel', 'payment_expiry', 'status']
    list_filter = list_display
    search_fields = ['user', 'hostel']
    # readonly_fields = list_display