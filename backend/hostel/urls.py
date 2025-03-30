from django.urls import path, include
from .views import *

urlpatterns = [
    path('', GetHostelDataAPI.as_view(), name="get-hostel"),
    path('book/<int:hostel_id>/', InitiateBookingAPI.as_view(), name="initiate-booking"),
    path('verify_otp/', VerifyOTPApi.as_view(), name='verify-otp')
]
