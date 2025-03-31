from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from hostel.models import RoomBooking
from hostel.serializers import RoomBookingSerializer
from .models import *
from .serializers import *
from .authentication import IsAuthenticated


# Create your views here.
class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(dat=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # user.send_verification_mail()
        return Response({'detail':'Registration Successful'}, status=status.HTTP_201_CREATED)
    

class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            return user.generate_login_response()
        else:
            return Response({'detail':"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
class ProfileAPIView(generics.CreateAPIView):
    serializer_class = RoomBookingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        user_bookings = RoomBooking.objects.filter(user=user)
        
        serializer = self.serializer_class(user_bookings, many=True)
        print(serializer)
        print(user_bookings)
        return Response({
            "message": "Nice one",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class VerifyTokenAPIView(APIView):
    def get(self, request):
        email = request.query_params.get('email', '')
        token = request.query_params.get('token', '')
        user = get_object_or_404(User, email=email)
        
        try:
            verify = BookingOTP.objects.get(user=user, code=token)
            verify.is_verified = True
            verify.save()

            return user.generate_login_response()
        except:
            return Response({'detail': 'Invalid Code.'}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPI(generics.GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LoginSerializer

    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        try:
            user = User.objects.get(email=email)
            user.send_forgot_password_mail(new_password=password)
            return Response({'detail': 'Verification code sent to your email'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Exeption: ", e)
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        email = request.query_params.get('email', '')
        token = request.query_params.get('token', '')
        user = get_object_or_404(User, email=email)

        try:
            f = ForgetPassword.objects.get(user=user,code=token)
            user.password=f.new_password
            user.save()
            
            return user.generate_login_response()
        except:
            return Response({'detail': 'Invalid Code.'}, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutAPIView(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        response.delete_cookie('token', domain=settings.COOKIE_DOMAIN)
        return response