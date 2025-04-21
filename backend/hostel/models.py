from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from authentication.models import User
from authentication.utils import send_email
from django.contrib.auth.hashers import make_password
from datetime import timedelta, time, datetime

INTERNAL_RESERVATION_PERCENT = 25

# Create your models here.
class Hostel(models.Model):
    ROOM_TYPE = [
        ('AC', 'AC'),
        ('NON-AC', 'NON-AC'),
    ]
    FOOD_TYPE = [
        ('Veg', "Veg"),
        ('Non_veg', 'Non-Veg'),
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
    # food_type = models.CharField('Food Type', max_length=20, blank=False, choices=FOOD_TYPE)
    is_veg = models.BooleanField('Veg Available', default=True)
    is_non_veg = models.BooleanField('Non-Veg Available', default=False)
    
    gender = models.CharField('Gender', max_length=10, blank=False, choices=GENDER)
    person_per_room = models.IntegerField(blank=False)
    no_of_rooms = models.IntegerField(blank=False)
    total_capacity = models.IntegerField(editable=False)
    room_description = models.CharField(max_length=100, blank=False)
    # amount = models.IntegerField(blank=False)
    image = models.ImageField(upload_to='rooms/', blank=True, default=None)
    enable = models.BooleanField(default=False)
    allow_bookings = models.BooleanField(default=False)
    bathroom_type = models.CharField(max_length=20, choices=BATHROOM_CHOICES, default='Common')
    
    first_year_fee_mgmt_veg = models.IntegerField(blank=False, null=False, default=0)
    first_year_fee_mgmt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    first_year_fee_govt_veg = models.IntegerField(blank=False, null=False, default=0)
    first_year_fee_govt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    second_year_fee_mgmt_veg = models.IntegerField(blank=False, null=False, default=0)
    second_year_fee_mgmt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    second_year_fee_govt_veg = models.IntegerField(blank=False, null=False, default=0)
    second_year_fee_govt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    third_year_fee_mgmt_veg = models.IntegerField(blank=False, null=False, default=0)
    third_year_fee_mgmt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    third_year_fee_govt_veg = models.IntegerField(blank=False, null=False, default=0)
    third_year_fee_govt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    fourth_year_fee_mgmt_veg = models.IntegerField(blank=False, null=False, default=0)
    fourth_year_fee_mgmt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    fourth_year_fee_govt_veg = models.IntegerField(blank=False, null=False, default=0)
    fourth_year_fee_govt_non_veg = models.IntegerField(blank=False, null=False, default=0)
    
    def __str__(self):
        return f"{self.name}-{self.location}-{self.room_type}-{self.person_per_room}"
    
    def clean(self):
        self.total_capacity = self.person_per_room * self.no_of_rooms

    def get_amount(self, year, quota):
        if not year or not quota:
            year = self.context.get('year')
            quota = self.context.get('quota')
        amounts = {
            1: {
                "Govt": {
                    "Govt_veg": self.first_year_fee_govt_veg,
                    "Govt_non_veg": self.first_year_fee_govt_non_veg,
                },
                "Mgmt": {
                    "Mgmt_veg": self.first_year_fee_mgmt_veg,
                    "Mgmt_non_veg": self.first_year_fee_mgmt_non_veg,
                }
            },
            2: {
                "Govt": {
                    "Govt_veg": self.second_year_fee_govt_veg,
                    "Govt_non_veg": self.second_year_fee_govt_non_veg,
                },
                "Mgmt": {
                    "Mgmt_veg": self.second_year_fee_mgmt_veg,
                    "Mgmt_non_veg": self.second_year_fee_mgmt_non_veg,
                }
            },
            3: {
                "Govt": {
                    "Govt_veg": self.third_year_fee_govt_veg,
                    "Govt_non_veg": self.third_year_fee_govt_non_veg,
                },
                "Mgmt": {
                    "Mgmt_veg": self.third_year_fee_mgmt_veg,
                    "Mgmt_non_veg": self.third_year_fee_mgmt_non_veg,
                }
            },
            4: {
                "Govt": {
                    "Govt_veg": self.fourth_year_fee_govt_veg,
                    "Govt_non_veg": self.fourth_year_fee_govt_non_veg,
                },
                "Mgmt": {
                    "Mgmt_veg": self.fourth_year_fee_mgmt_veg,
                    "Mgmt_non_veg": self.fourth_year_fee_mgmt_non_veg,
                }
            },
        }
        return amounts[year][quota]
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
        internal_reserved = int(self.total_capacity * (INTERNAL_RESERVATION_PERCENT / 100))
        
        return min(total_available, internal_reserved)
    
class RoomBooking(models.Model):
    BOOKING_STATUS = [
        ('otp_pending', 'OTP Pending'),
        ('payment_pending', 'Payment Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('payment_not_done', 'Payment Not Done'), # Worst case scenario
        ('vacated', 'Vacated'),
        ('course_completed', 'Course Completed'),
    ]
    FOOD_TYPE = [
        ('Veg', "Veg"),
        ('Non_veg', 'Non-Veg'),
    ]

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, 
        default='otp_pending', 
        choices=BOOKING_STATUS
    )
    food_type = models.CharField('Food Type', null=True, choices=FOOD_TYPE, max_length=20)
    is_internal_booking = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)
    otp_verified_at = models.DateTimeField(null=True, blank=True)
    is_payment_link_sent = models.BooleanField(default=False)
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
        unique_together = ('user', 'hostel', 'status', 'booked_at')

    # def clean(self):
    #     if self.user.gender != self.hostel.gender:
    #         raise ValidationError("User gender doesn't match hostel gender requirement")
        
    #     if self.is_internal_booking:
    #         return

    #     if self.pk is None or self.status not in ['confirmed', 'payment_verified']:
    #     # if self.pk is None:
    #         if self.is_internal_booking:
    #             if self.hostel.admin_bookings_available() <= 0:
    #                 raise ValidationError("No more internal reservation slots available")
    #         else:
    #             if not self.hostel.is_available():
    #                 raise ValidationError("This hostel is currently not available")

    def clean(self):

        # if self.is_internal_booking:
        #     return
        if self.pk:
            original = RoomBooking.objects.get(pk=self.pk)
            
            if original.hostel_id != self.hostel_id:
                if self.user.gender != self.hostel.gender:
                    raise ValidationError("User gender doesn't match hostel gender requirement")
                    
                if self.is_internal_booking:
                    if self.hostel.admin_bookings_available() <= 0:
                        raise ValidationError("No more internal reservation slots available in the new hostel")
                else:
                    if not self.hostel.is_available():
                        raise ValidationError("The new hostel is currently not available")
            
            elif not original.is_internal_booking and self.is_internal_booking:
                if self.hostel.admin_bookings_available() <= 0:
                    raise ValidationError("No more internal reservation slots available")
        else:
            old_bookings = RoomBooking.objects.filter(user=self.user, status__in = ['payment_pending', 'otp_pending', 'confirmed'])
            if old_bookings.exists():
                raise ValidationError("Already an existing booking is found!")
            if self.user.gender != self.hostel.gender:
                raise ValidationError("User gender doesn't match hostel gender requirement")
                
            if self.is_internal_booking:
                if self.hostel.admin_bookings_available() <= 0:
                    raise ValidationError("No more internal reservation slots available")
            else:
                if not self.hostel.is_available():
                    raise ValidationError("This hostel is currently not available")

    def save(self, *args, **kwargs):
        self.clean()
        if self.status == 'payment_not_done':
            Penalty.objects.create(
                user=self.user,
                hostel=self.hostel,
                status=self.status,
                is_internal_booking=self.is_internal_booking,
                booked_at=self.booked_at,
                otp_verified_at=self.otp_verified_at,
                payment_completed_at=self.payment_completed_at,
                payment_link=self.payment_link,
                payment_reference=self.payment_reference,
                otp_code=self.otp_code,
                otp_expiry=self.otp_expiry,
                payment_expiry=self.payment_expiry,
                admin_notes=self.admin_notes,
            )
            self.save()
            return
        elif self.status == 'confirmed':
            subject = "Booking Confirmed - Your Stay is Ready!"
            to_email = self.user.email
            
            send_email(
                subject=subject,
                to_email=to_email,
                context={
                    "user_name": self.user.first_name or "Valued Guest",
                    "hostel_name": self.hostel.name,
                    "room_type": self.hostel.room_type,
                    "food_type": self.food_type,
                },
                template_name="booking_confirmation_template.html"
            )
        elif self.status == 'cancelled':
            subject = "Important Update on Your Hostel Booking Payment"
            to_email = self.user.email
            send_email(
                subject=subject,
                to_email=to_email,
                context={
                    "user_name": self.user.first_name or "Valued Guest",
                    "hostel_name": self.hostel.name,
                    "room_type": self.hostel.room_type,
                },
                template_name="payment_rejection_template.html"
            )
        super().save(*args, **kwargs)

    def get_amount(self):
        try:
            amounts = {
                1: {
                    "Govt": {
                        "veg": self.hostel.first_year_fee_govt_veg,
                        "non_veg": self.hostel.first_year_fee_govt_non_veg,
                    },
                    "Mgmt": {
                        "veg": self.hostel.first_year_fee_mgmt_veg,
                        "non_veg": self.hostel.first_year_fee_mgmt_non_veg,
                    }
                },
                2: {
                    "Govt": {
                        "veg": self.hostel.second_year_fee_govt_veg,
                        "non_veg": self.hostel.second_year_fee_govt_non_veg,
                    },
                    "Mgmt": {
                        "veg": self.hostel.second_year_fee_mgmt_veg,
                        "non_veg": self.hostel.second_year_fee_mgmt_non_veg,
                    }
                },
                3: {
                    "Govt": {
                        "veg": self.hostel.third_year_fee_govt_veg,
                        "non_veg": self.hostel.third_year_fee_govt_non_veg,
                    },
                    "Mgmt": {
                        "veg": self.hostel.third_year_fee_mgmt_veg,
                        "non_veg": self.hostel.third_year_fee_mgmt_non_veg,
                    }
                },
                4: {
                    "Govt": {
                        "veg": self.hostel.fourth_year_fee_govt_veg,
                        "non_veg": self.hostel.fourth_year_fee_govt_non_veg,
                    },
                    "Mgmt": {
                        "veg": self.hostel.fourth_year_fee_mgmt_veg,
                        "non_veg": self.hostel.fourth_year_fee_mgmt_non_veg,
                    }
                },
            }

            year = self.user.year
            quota = self.user.student_type.title()
            return amounts[year][quota][self.food_type.lower()]
        except Exception as e:
            print(e)
            return 0

    def update_status(self, new_status, verified_by_user=None):
        old_status = self.status
        self.status = new_status
        if old_status != new_status and verified_by_user is not None:
            if verified_by_user.is_staff or verified_by_user.is_superuser:
                self.verified_by = verified_by_user
        if self.status == 'confirmed':
            self.payment_completed_at = timezone.now()
            
        if self.status == 'payment_not_done':
            Penalty.objects.create(
                user=self.user,
                hostel=self.hostel,
                status=self.status,
                is_internal_booking=self.is_internal_booking,
                booked_at=self.booked_at,
                otp_verified_at=self.otp_verified_at,
                payment_completed_at=self.payment_completed_at,
                payment_link=self.payment_link,
                payment_reference=self.payment_reference,
                otp_code=self.otp_code,
                otp_expiry=self.otp_expiry,
                payment_expiry=self.payment_expiry,
                admin_notes=self.admin_notes,
            )
            self.save()
        else:
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
        amount = self.get_amount()
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "otp_code": self.otp_code,
                "hostel_name": self.hostel.name,
                "room_type": self.hostel.room_type,
                "amount": amount,
                "food_type": self.food_type
            },
            template_name='otp_email.html'
        )
   
    def calculate_payment_expiry(self):
        now = timezone.now()
    
        midnight_today = datetime.combine(now.date(), datetime.min.time())
    
        expiry_date = midnight_today + timedelta(days=5, hours=23, minutes=59, seconds=59)
    
        if timezone.is_aware(now):
            expiry_date = timezone.make_aware(expiry_date)
    
        return expiry_date
    
    def verify_otp(self, otp_code):
        if (self.status != 'otp_pending' or 
            timezone.now() > self.otp_expiry or 
            self.otp_code != str(otp_code)):
            return False
        
        self.otp_verified_at = timezone.now()
        self.status = 'payment_pending'
        self.payment_expiry = self.calculate_payment_expiry()
        self.payment_link = f"https://payment.link.should.be.pasted.here"
        self.save()
        self.send_payment_instructions()
        return True

    def send_payment_instructions(self):
        subject = "Complete Your Hostel Booking Payment"
        to_email = self.user.email
        amount = self.get_amount()
        
        payment_expiry_formatted = self.payment_expiry.strftime("%d %b %Y, %I:%M %p")
        
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "hostel_name": self.hostel.name,
                "room_type": self.hostel.room_type,
                "amount": amount,
                "payment_link": self.payment_link,
                'food_type': self.food_type,
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

class Penalty(models.Model):
    BOOKING_STATUS = [
        ('otp_pending', 'OTP Pending'),
        ('payment_pending', 'Payment Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('payment_not_done', 'Payment Not Done'),
        ('vacated', 'Vacated'),
        ('course_completed', 'Course Completed'),
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

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Penalty records cannot be modified once created")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Penalty records cannot be deleted")