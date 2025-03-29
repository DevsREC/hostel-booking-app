from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('staff', 'Staff')
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    username = None
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    year = models.IntegerField(default=0,)
    dept = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    parent_phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="hostel_user_groups",
        related_query_name="hostel_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="hostel_user_permissions",
        related_query_name="hostel_user",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"

class Hostel(models.Model):
    TYPE_CHOICES = [
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC')
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    FOOD_CHOICES = [
        ('Veg', 'Vegetarian'),
        ('Non-Veg', 'Non-Vegetarian'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    no_of_persons = models.IntegerField()
    total_capacity = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    food_type = models.CharField(max_length=10, choices=FOOD_CHOICES)
    room_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.location})"

class BookingOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_expired = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user} - {self.otp}"
    
class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_deadline = models.DateTimeField()
    
    def __str__(self):
        return f"Booking #{self.id} - {self.user} at {self.hostel}"