#!/usr/bin/env python

import os
import sys
import django
import logging
import threading
import time
from datetime import datetime, timedelta

# Set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from django.utils import timezone
from hostel.models import RoomBooking
from authentication.utils import send_email

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('payment_reminders.log')
    ]
)
logger = logging.getLogger(__name__)

def process_booking(booking, midnight_expiry, payment_expiry_formatted):
    """Process a single booking in its own thread"""
    try:
        # Update payment expiry date
        booking.payment_expiry = midnight_expiry
        
        # Set payment link
        booking.payment_link = f"https://fees.easebuzz.in/view/RAJALAKSHMI40E7S"
        
        # Send payment reminder email
        amount = booking.get_amount()
        
        subject = "URGENT: Complete Your Hostel Booking Payment"
        to_email = booking.user.email
        
        send_email(
            subject=subject,
            to_email=to_email,
            context={
                "user_name": booking.user.first_name or "Valued Guest",
                "hostel_name": booking.hostel.name,
                "room_type": booking.hostel.room_type,
                "amount": amount,
                "payment_link": booking.payment_link,
                "food_type": booking.food_type,
                "payment_expiry_date": payment_expiry_formatted,
            },
            template_name="payment_reminder_template.html"
        )
        
        # Mark as sent to avoid duplicate emails
        booking.is_payment_link_sent = True
        booking.save()
        
        logger.info(f"Payment reminder sent to {to_email} for booking ID: {booking.id}")
        print(f"Payment reminder sent to {to_email}")
        return True
        
    except Exception as e:
        error_msg = f"Failed to send payment reminder for booking ID {booking.id}: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        return False

def send_payment_reminders():
    print("Script is running...")
    
    # Define cutoff date (April 24th, 2025)
    cutoff_date = timezone.make_aware(datetime(2025, 5, 2, 23, 59, 59))
    
    # Get bookings that have verified OTP on or before cutoff date but payment is still pending
    bookings = RoomBooking.objects.filter(
        status='payment_pending',
        otp_verified_at__lte=cutoff_date,
        is_payment_link_sent=False  # To avoid sending duplicate reminders
    )
    
    booking_count = bookings.count()
    print(f"Found {booking_count} bookings that need payment reminders.")
    
    if booking_count == 0:
        print("No bookings to process. Exiting.")
        return
    
    # Calculate new payment expiry (5 days from now)
    now = timezone.now()
    payment_expiry = now + timedelta(days=5)
    
    # Format as midnight of the 5th day
    midnight_expiry = datetime.combine(payment_expiry.date(), datetime.min.time()) + timedelta(days=1, seconds=-1)
    if timezone.is_aware(now):
        midnight_expiry = timezone.make_aware(midnight_expiry)
    
    payment_expiry_formatted = midnight_expiry.strftime("%d %b %Y, %I:%M %p")
    
    # Create and start threads for each booking
    threads = []
    for booking in bookings:
        thread = threading.Thread(
            target=process_booking,
            args=(booking, midnight_expiry, payment_expiry_formatted)
        )
        threads.append(thread)
        thread.start()
        # Small delay to prevent overloading the mail server
        time.sleep(1)  
    
    # Wait for all threads to complete
    success_count = 0
    failed_count = 0
    
    for thread in threads:
        thread.join()
        
    # Count successful and failed operations
    for booking in bookings:
        if booking.is_payment_link_sent:
            success_count += 1
        else:
            failed_count += 1
    
    print(f"Payment reminders sent: {success_count} successful, {failed_count} failed")
    logger.info(f"Payment reminders sent: {success_count} successful, {failed_count} failed")

if __name__ == "__main__":
    # Run the main function in a separate thread
    main_thread = threading.Thread(target=send_payment_reminders)
    main_thread.start()
    
    print("Script started in background thread...")
    
    # Optional: You can have the main thread do other things here while the reminders are being sent
    
    # If you want to wait for the process to complete before exiting:
    main_thread.join()
    print("Script completed!")