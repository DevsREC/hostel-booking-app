from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User
import jwt

class IsAuthenticated(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get('token')
            if not token:
                raise exceptions.AuthenticationFailed('Authentication Failed')
            try:
                payload = jwt.decode(token, settings.JWT_KEY, 'HS256')
            except:
                raise exceptions.AuthenticationFailed('Authentication Failed')
            email = payload['id']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('Authentication Failed')

            return (user, None)
        except:
            raise exceptions.AuthenticationFailed('Authentication Failed')

class CheckAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get('token')
            if not token:
                return (None, None)
            try:
                payload = jwt.decode(token, settings.JWT_KEY, 'HS256')
            except jwt.ExpiredSignatureError:
                return (None, None)
            email=payload['id']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return (None, None)
            return (user, None)
        except:
            return (None, None)