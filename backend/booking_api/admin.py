from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Hostel, BookingOTP, Booking

class UserAdmin(UserAdmin):
    ordering = ('email',)

    list_display = ('email', 'first_name', 'last_name', 'roll_number', 'year', 'dept', 'role', 'gender')
    list_filter = ('role', 'year', 'dept', 'gender')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'parent_phone_number', 'gender')}),
        ('Academic info', {'fields': ('year', 'dept', 'roll_number')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'roll_number', 'year', 'dept'),
        }),
    )

class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'no_of_persons', 'gender', 'food_type', 'amount')
    list_filter = ('type', 'gender', 'food_type')
    search_fields = ('name', 'location')

class BookingOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_expired', 'is_validated', 'created_at', 'expires_at')
    list_filter = ('is_expired', 'is_validated')
    readonly_fields = ('created_at', 'expires_at')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostel', 'payment_status', 'booked_at', 'payment_deadline')
    list_filter = ('payment_status', 'hostel')
    readonly_fields = ('booked_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(BookingOTP, BookingOTPAdmin)
admin.site.register(Booking, BookingAdmin)