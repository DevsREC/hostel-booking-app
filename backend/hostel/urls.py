from django.urls import path, include
from .views import *

urlpatterns = [
    path('book/<int:hostel_id>/', InitiateBookingAPI.as_view(), name="initiate-booking"),
    path('verify-otp/<int:booking_id>/', VerifyOTPApi.as_view(), name='verofy-otp'),
]
