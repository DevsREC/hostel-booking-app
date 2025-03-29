from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, HostelViewSet, BookingOTPViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hostels', HostelViewSet)
router.register(r'booking-otp', BookingOTPViewSet, basename='bookingotp')
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]