from django.utils import timezone
from .models import RoomBooking
from authentication.utils import send_email

def cancel_expired_bookings():
    expired_otp_bookings = RoomBooking.objects.filter(
        status='otp_pending',
        otp_expiry__lt=timezone.now()
    )

    count = expired_otp_bookings.count()
    
    for booking in expired_otp_bookings:
        send_cancellation_email(booking)
    
    expired_otp_bookings.delete()
    
    print(f"[{timezone.now()}] Cancelled and deleted {count} expired OTP bookings.")
    return count

# def mark_expired_payment():
#     expired_payment_bookings = RoomBooking.objects.filter(
#         status='payment_pending',
#         payment_expiry__lt=timezone.now()
#     )

#     count = expired_payment_bookings.count()
    
#     for booking in expired_payment_bookings:
#         send_payment_expired_email(booking)
#         booking.status = 'payment_not_done'
#         booking.save()
    
#     print(f"[{timezone.now()}] Marked {count} bookings as 'payment_not_done' due to expired payment")
#     return count

def send_cancellation_email(self, booking):
    subject = "Booking Cancellation - OTP Verification Timeout"
    to_email = booking.user.email
    
    booking_url = "https://yourhostelbooking.com/booking/new"
    
    send_email(
        subject=subject,
        to_email=to_email,
        context={
            "user_name": booking.user.first_name or "Valued Guest",
            "hostel_name": booking.hostel.name,
            "room_type": booking.hostel.room_type,
            "food_type": booking.hostel.food_type,
        },
        template_name="booking_cancellation_template.html"
    )

# def send_payment_expired_email(self, booking):
#     subject = "Payment Deadline Expired - Hostel Booking"
#     to_email = booking.user.email
#     )
#     booking_url = "https://yourhostelbooking.com/booking/new"
    
#     send_email(
#         subject=subject,
#         to_email=to_email,
#         context={
#             "user_name": booking.user.first_name or "Valued Guest",
#             "hostel_name": booking.hostel.name,
#             "room_type": booking.hostel.room_type,
#             "food_type": booking.hostel.food_type,
#         },
#         template_name="payment_expired_template.html"
#     )