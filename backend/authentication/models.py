from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from .utils import send_email
import uuid
import jwt

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', "Male"),
        ('F', 'Female')
    ]

    username = None

    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('First Name',max_length=255, blank=False)
    last_name = models.CharField('Last Name',max_length=255, blank=False)
    year = models.IntegerField('Year', blank=False, default=0)
    dept = models.CharField('Department', max_length=50)
    roll_no = models.CharField('Roll No', max_length=50)
    phone_number = models.CharField('Phone Number', max_length=20)
    parent_phone_number = models.CharField('Parent Ph. No.', max_length=20)
    gender = models.CharField('Gender', max_length=10, blank=False, choices=GENDER_CHOICES)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name}'
    
    def generate_login_response(self):
        payload = {
            'id': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'exp': timezone.now() + timezone.timedelta(days=30),
            'iat': timezone.now()
        }

        token = jwt.encode(payload, settings.JWT_KEY, algorithm='HS256')
        response = Response({
            'id': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }, status=status.HTTP_200_OK)

        response.set_cookie(key='token', value=token, samesite='Lax', httponly=True, secure=False, domain=settings.COOKIE_DOMAIN)

        return response
    
    def send_verification_mail(self):
        verfication_code = get_random_string(length=8)
        start_content = f'Hostel Room Booking: Initiated\nOTP: {verfication_code}'
        subject = "Hostel Room Booking"
        to_email = self.email
        verfication, created = BookingOTP.objects.get_or_create(user=self)
        verfication.code = verfication_code
        verfication.save()
        send_email(subject, to_email, {
            "startingcontent": start_content,
        })

    def send_forgot_password_mail(self, new_password):
        verfication_code = get_random_string(length=8)
        start_content = f'Hostel Room Booking: Forgot Password\nOTP: {verfication_code}'
        subject = "Hostel Room Booking: Forgot Password"
        to_email = self.email
        verfication, created = ForgetPassword.objects.get_or_create(user=self)
        verfication.code = verfication_code
        verfication.new_password = new_password
        verfication.save()
        send_email(subject, to_email, {
            "startingcontent": start_content,
        })

class BookingOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"
    

class ForgetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new_password = models.CharField(max_length=128)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user}"
    
    def __save__(self, *args, **kwargs):
        if not self.new_password.startswith('pbkdf2_sha256$'):
            self.new_password = make_password(self.new_password)
        super().save(*args, **kwargs)
