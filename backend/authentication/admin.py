from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import *
from .resources import UserResource
from unfold.admin import ModelAdmin
# Register your models here.

class VerificationCodeInline(admin.StackedInline):
    model = BookingOTP
    extra = 0
    can_delete = False

class ForgotPasswordInline(admin.StackedInline):
    model = ForgetPassword
    extra = 0
    can_delete = False

@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, ModelAdmin):
    compressed_fields = True
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'parent_phone_number', 'gender')}),
        ('Academic Info', {'fields': ('year', 'dept', 'roll_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Other Info', {'fields': ('last_login', 'date_joined')}),
    )

    list_filter = ['is_active', 'is_staff', 'is_superuser', 'year', 'dept', 'gender']
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    list_display = ['email', 'uuid', 'first_name', 'last_name', 'year', 'dept', 'roll_no', 'gender']
    resource_classes = [UserResource]

# @admin.register(BookingOTP)
class VerificationCodeAdmin(ModelAdmin):
    list_display = ['user', 'code']
    search_fields = ['user_email', 'user_first_name']
    autocomplete_fields = ['user']

@admin.register(ForgetPassword)
class ForgotPasswordAdmin(ModelAdmin):
    list_display = ['user', 'code']
    search_fields = ['user_email', 'user_first_name']
    autocomplete_fields = ['user']