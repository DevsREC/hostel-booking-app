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

def mark_expired_payment():
    expired_payment_bookings = RoomBooking.objects.filter(
        status='payment_pending',
        payment_expiry__lt=timezone.now()
    )

    count = expired_payment_bookings.count()
    
    for booking in expired_payment_bookings:
        send_payment_expired_email(booking)
        booking.status = 'payment_not_done'
        booking.save()
    
    print(f"[{timezone.now()}] Marked {count} bookings as 'payment_not_done' due to expired payment")
    return count

def send_cancellation_email(self, booking):
    subject = "Hostel Booking Cancelled - OTP Verification Timeout"
    
    message = f"""
        <p><strong>Your hostel booking has been cancelled</strong> due to OTP verification timeout.</p>
        
        <h3>Booking Details:</h3>
        <div class="details">
            <p><strong>Hostel:</strong> {booking.hostel.name}</p>
            <p><strong>Room Type:</strong> {booking.hostel.room_type}</p>
            <p><strong>Food Type:</strong> {booking.hostel.food_type}</p>
        </div>
        
        <p>To book again, please revisit our booking portal and restart the process.</p>
        <p>We apologize for any inconvenience caused.</p>
        
        <p><strong>Note:</strong> OTP verification must be completed within 10 minutes of booking initiation.</p>
    """
    
    send_email(
        subject=subject, 
        to_email=booking.user.email, 
        context={"startingcontent": message}
    )

def send_payment_expired_email(self, booking):
    subject = "Hostel Booking - Payment Deadline Expired"
    
    message = f"""
        <p><strong>Your hostel booking payment deadline has expired.</strong></p>
        
        <h3>Booking Details:</h3>
        <div class="details">
            <p><strong>Hostel:</strong> {booking.hostel.name}</p>
            <p><strong>Room Type:</strong> {booking.hostel.room_type}</p>
            <p><strong>Food Type:</strong> {booking.hostel.food_type}</p>
            <p><strong>Amount:</strong> ₹{booking.hostel.amount}</p>
        </div>
        
        <p>Your booking status has been changed to <strong>"Payment Not Done"</strong>. If you still wish to book this room, you will need to start a new booking process.</p>
        
        <p><strong>Note:</strong> Payments must be completed within 24 hours after OTP verification.</p>
    """
    
    send_email(
        subject=subject, 
        to_email=booking.user.email, 
        context={"startingcontent": message}
    )
