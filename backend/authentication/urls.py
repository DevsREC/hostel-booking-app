from django.urls import path
from .views import *

urlpatterns = [
    # path('regitser/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    # path('verify/', VerifyTokenAPIView.as_view(), name='verify'),
    path('forgot_password/', ForgotPasswordAPI.as_view(), name='forget-password'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
]
