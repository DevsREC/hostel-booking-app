from django.utils import timezone
from authentication.utils import send_email
import logging
import os
from subprocess import Popen, PIPE
from datetime import datetime

logger = logging.getLogger(__name__)

def cancel_expired_bookings():
    from .models import RoomBooking
    from django.utils import timezone
    import logging
    
    logger = logging.getLogger(__name__)
    
    expired_otp_bookings = RoomBooking.objects.filter(
        status='otp_pending',
        otp_expiry__lt=timezone.now()
    )
    
    expired_bookings_data = []
    count = expired_otp_bookings.count()
    
    logger.info(f"Found {count} expired OTP bookings")
    
    for booking in expired_otp_bookings:
        booking_data = {
            'user_name': f"{booking.user.first_name} {booking.user.last_name}" if hasattr(booking, 'user') else booking.guest_name,
            'user_email': booking.user.email if hasattr(booking, 'user') else booking.guest_email,
            'otp_expiry': booking.otp_expiry,
            'roll_no': booking.user.roll_no,
        }
        expired_bookings_data.append(booking_data)
        
        send_cancellation_email(booking=booking)
    
    send_email(
        subject=f"OTP Cleanup Report - {count} Expired Bookings",
        to_email="220701317@rajalakshmi.edu.in",
        context={
            "count": count,
            "expired_bookings": expired_bookings_data,
            "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        template_name="otp_expired.html"
    )
    
    expired_otp_bookings.delete()
    print(f"[{timezone.now()}] Cancelled and deleted {count} expired OTP bookings.")
    return count

def mark_expired_payment():
    from .models import RoomBooking, Penalty
    from django.utils import timezone
    import logging
    
    logger = logging.getLogger(__name__)
    
    expired_payment_bookings = RoomBooking.objects.filter(
        status='payment_pending',
        payment_expiry__lt=timezone.now()
    )

    count = expired_payment_bookings.count()
    
    expired_bookings_data = []
    
    for booking in expired_payment_bookings:
        booking_data = {
            'user_name': f"{booking.user.first_name} {booking.user.last_name}" if hasattr(booking.user, 'first_name') else booking.user.username,
            'user_email': booking.user.email,
            'roll_no': booking.user.roll_no if hasattr(booking.user, 'roll_no') else 'N/A',
            'hostel_name': booking.hostel.name if hasattr(booking, 'hostel') else 'N/A',
            'payment_link': booking.payment_link,
            'payment_expiry': booking.payment_expiry
        }
        expired_bookings_data.append(booking_data)
        
        Penalty.objects.create(
            user=booking.user,
            hostel=booking.hostel,
            status=booking.status,
            is_internal_booking=booking.is_internal_booking,
            booked_at=booking.booked_at,
            otp_verified_at=booking.otp_verified_at,
            payment_completed_at=booking.payment_completed_at,
            payment_link=booking.payment_link,
            payment_reference=booking.payment_reference,
            otp_code=booking.otp_code,
            otp_expiry=booking.otp_expiry,
            payment_expiry=booking.payment_expiry,
            admin_notes=booking.admin_notes,
        )
        
        send_payment_expired_email(booking)
        
        booking.status = 'payment_not_done'
        booking.delete()
    
    if count > 0:
        send_email(
            subject=f"Payment Expiry Report - {count} Expired Bookings",
            to_email="220701317@rajalakshmi.edu.in",
            context={
                "count": count,
                "expired_bookings": expired_bookings_data,
                "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            template_name="payment_expired.html"
        )
    
    logger.info(f"[{timezone.now()}] Marked {count} bookings as 'payment_not_done' due to expired payment")
    return count

def send_cancellation_email(booking):
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

def send_payment_expired_email(booking):
    subject = "Payment Deadline Expired - Hostel Booking"
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
        template_name="payment_expired_template.html"
    )

logger = logging.getLogger(__name__)

def create_db_dump_and_send_email():
    try:
        from django.conf import settings
        db_config = settings.DATABASES['default']
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_filename = f"db_dump_{timestamp}.sql"
        dump_path = os.path.join('/tmp', dump_filename)
        
        pg_dump_cmd = [
            'pg_dump',
            '-h', db_config['HOST'],
            '-U', db_config['USER'],
            '-d', db_config['NAME'],
            '-f', dump_path
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = db_config['PASSWORD']
        
        process = Popen(pg_dump_cmd, env=env, stderr=PIPE)
        _, stderr = process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"pg_dump failed: {stderr.decode('utf-8')}")
        
        if not os.path.exists(dump_path):
            raise Exception("Database dump file was not created")
        
        file_size = os.path.getsize(dump_path) / (1024 * 1024)
        
        with open(dump_path, 'rb') as f:
            dump_content = f.read()
        
        send_email(
            subject=f"Database Backup - {timestamp}",
            to_email="220701317@rajalakshmi.edu.in",
            context={
                "timestamp": timezone.now().strftime(   "%Y-%m-%d %H:%M:%S"),
                "file_size": f"{file_size:.2f} MB",
                "db_name": db_config['NAME']
            },
            template_name="db_backup_email.html",
            attachments=[(dump_filename, dump_content, 'application/sql')]
        )
        
        os.remove(dump_path)
        
        logger.info(f"Successfully created and sent database dump. Size: {file_size:.2f} MB")
        return True
    
    except Exception as e:
        print(e)
        logger.error(f"Error creating database dump: {str(e)}")
        
        send_email(
            subject="Database Backup Failed",
            to_email="220701317@rajalakshmi.edu.in",
            context={
                "error": str(e),
                "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            template_name="db_backup_error.html"
        )
        return False