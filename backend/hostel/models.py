from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from authentication.models import User
from authentication.utils import send_email
from django.contrib.auth.hashers import make_password

INTERNAL_RESERVATION_PERCENT = 25

# Create your models here.
class Hostel(models.Model):
    ROOM_TYPE = [
        ('AC', 'AC'),
        ('NON-AC', 'NON-AC'),
    ]
    FOOD_TYPE = [
        ('Veg', "Veg"),
        ('Non-veg', 'Non-Veg'),
    ]
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    BATHROOM_CHOICES = [
        ('Attached', 'Attached'),
        ('Common', 'Common')
    ]

    name = models.CharField('Hostel Name', blank=False, max_length=50)
    location = models.CharField('Location', blank=False,max_length=50)
    room_type = models.CharField('Room Type', max_length=20, blank=False, choices=ROOM_TYPE)
    food_type = models.CharField('Food Type', max_length=20, blank=False, choices=FOOD_TYPE)
    gender = models.CharField('Gender', max_length=10, blank=False, choices=GENDER)
    person_per_room = models.IntegerField(blank=False)
    no_of_rooms = models.IntegerField(blank=False)
    total_capacity = models.IntegerField(editable=False)
    room_description = models.CharField(max_length=100, blank=False)
    # amount = models.IntegerField(blank=False)
    image = models.ImageField(upload_to='rooms/')
    enable = models.BooleanField(default=False)
    bathroom_type = models.CharField(max_length=20, choices=BATHROOM_CHOICES, default='Common')
    first_year_fee = models.IntegerField(blank=False, null=False)
    second_year_fee = models.IntegerField(blank=False, null=False)
    third_year_fee = models.IntegerField(blank=False, null=False)
    fourth_year_fee = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name}-{self.location}-{self.room_type}-{self.food_type}-{self.person_per_room}"
    
    def clean(self):
        self.total_capacity = self.person_per_room * self.no_of_rooms

    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        self.clean()
        return super().save()
    
    def available_rooms(self):
        booked_rooms = RoomBooking.objects.filter(
            hostel=self, 
            status__in=['confirmed', 'payment_verified', 'payment_pending']
        ).count()

        total_available = self.total_capacity - booked_rooms
        internal_reserved = int(self.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
        online_available = total_available - internal_reserved

        return max(0, online_available)

    def is_available(self):
        return self.enable and self.available_rooms() > 0
    
    def admin_bookings_available(self):
        booked_rooms = RoomBooking.objects.filter(
            hostel=self, 
            status__in=['confirmed', 'payment_pending', 'otp_pending']
        ).count()
        
        total_available = self.total_capacity - booked_rooms
        internal_reserved = int(self.total_capacity * (self.internal_reservation_percent / 100))
        
        return min(total_available, internal_reserved)
    
class RoomBooking(models.Model):
    BOOKING_STATUS = [
        ('otp_pending', 'OTP Pending'),
        ('payment_pending', 'Payment Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('payment_not_done', 'Payment Not Done'), # Worst case scenario
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, 
        default='otp_pending', 
        choices=BOOKING_STATUS
    )
    is_internal_booking = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)
    otp_verified_at = models.DateTimeField(null=True, blank=True)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    payment_link = models.URLField(max_length=255, blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    otp_code = models.CharField(max_length=10, blank=True, null=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    payment_expiry = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        related_name="verified_bookings",
        null=True,
        blank=True,
        editable=False
    )

    def __str__(self):
        return f'{self.user.email} - {self.hostel.name} - {self.status}'

    class Meta:
        unique_together = ('user', 'hostel')

    def clean(self):
        if self.user.gender != self.hostel.gender:
            raise ValidationError("User gender doesn't match hostel gender requirement")
        
        if self.pk is None or self.status not in ['confirmed', 'payment_verified']:
            if self.is_internal_booking:
                if self.hostel.admin_bookings_available() <= 0:
                    raise ValidationError("No more internal reservation slots available")
            else:
                if not self.hostel.is_available():
                    raise ValidationError("This hostel is currently not available")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def update_status(self, new_status, verified_by_user=None):
        old_status = self.status
        self.status = new_status
        
        if old_status != new_status and verified_by_user is not None:
            if verified_by_user.is_staff or verified_by_user.is_superuser:
                self.verified_by = verified_by_user
        
        self.save()
        return True

    def generate_otp(self):
        import random
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expiry = timezone.now() + timezone.timedelta(minutes=10)
        self.status = 'otp_pending'
        self.save()
        self.send_otp_email()

    def send_otp_email(self):
        subject = "Hostel Booking OTP Verification"
        to_email = self.user.email
        amount = 0
        if self.user.year == 1:
            amount = self.hostel.first_year_fee
        elif self.user.year == 2:
            amount = self.hostel.second_year_fee
        elif self.user.year == 3:
            amount = self.hostel.third_year_fee
        elif self.user.year == 4:
            amount = self.hostel.fourth_year_fee
        
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "otp_code": self.otp_code,
                "hostel_name": self.hostel.name,
                "room_type": self.hostel.room_type,
                "amount": amount
            },
            template_name='otp_email.html'
        )


    def verify_otp(self, otp_code):
        if (self.status != 'otp_pending' or 
            timezone.now() > self.otp_expiry or 
            self.otp_code != str(otp_code)):
            return False
        
        self.otp_verified_at = timezone.now()
        self.status = 'payment_pending'
        self.payment_expiry = timezone.now() + timezone.timedelta(hours=24 * 7)
        self.payment_link = f"https://payment.link.should.be.pasted.here"
        self.save()
        self.send_payment_instructions()
        return True

    def send_payment_instructions(self):
        subject = "Complete Your Hostel Booking Payment"
        to_email = self.user.email
        amount = 0
        if self.user.year == 1:
            amount = self.hostel.first_year_fee
        elif self.user.year == 2:
            amount = self.hostel.second_year_fee
        elif self.user.year == 3:
            amount = self.hostel.third_year_fee
        elif self.user.year == 4:
            amount = self.hostel.fourth_year_fee
        payment_expiry_formatted = self.payment_expiry.strftime("%d %b %Y, %I:%M %p")
        
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "hostel_name": self.hostel.name,
                "room_type": self.hostel.room_type,
                "amount": amount,
                "payment_link": self.payment_link,
                "payment_expiry_date": payment_expiry_formatted
            },
            template_name="payment_instructions_template.html"  # Path to the HTML template
        )

    # def submit_payment_reference(self, reference):
    #     self.payment_reference = reference
    #     self.status = 'payment_verified'
    #     self.save()
    #     self.notify_admin()

    # def notify_admin(self):
    #     print(f"Admin notification: Payment reference {self.payment_reference} submitted for booking {self.id}")