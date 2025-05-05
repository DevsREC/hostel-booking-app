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
        logging.FileHandler('payment_extensions.log')
    ]
)
logger = logging.getLogger(__name__)

def process_booking_extension(booking, new_expiry, expiry_formatted):
    """Process a single booking extension in its own thread"""
    try:
        # Save the old expiry date for the email
        old_expiry_formatted = booking.payment_expiry.strftime("%d %b %Y, %I:%M %p") if booking.payment_expiry else "Not Set"
        
        # Update booking status and payment expiry date
        booking.status = 'payment_pending'
        booking.payment_expiry = new_expiry
        
        # Send payment extension email
        amount = booking.get_amount()
        
        subject = "IMPORTANT: Your Hostel Payment Deadline Extended"
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
                "old_payment_expiry_date": old_expiry_formatted,
                "payment_expiry_date": expiry_formatted,
            },
            template_name="p_e.html"
        )
        
        # Mark as extended to track this operation
        # booking.payment_deadline_extended = True  # Assuming this field exists
        booking.save()
        
        logger.info(f"Payment deadline extended for {to_email} (Booking ID: {booking.id}) to {expiry_formatted}")
        print(f"Payment deadline extended for {to_email}")
        return True
        
    except Exception as e:
        error_msg = f"Failed to extend payment deadline for booking ID {booking.id}: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        return False

def extend_payment_deadlines():
    print("Payment extension script is running...")
    
    # Get current date and set target expiry date (May 6, 2025, 11:59 PM)
    now = timezone.now()
    target_date = timezone.make_aware(datetime(2025, 5, 6, 23, 59, 59))
    
    # Get bookings with status 'payment_not_done'
    bookings = RoomBooking.objects.filter(
        status='payment_not_done',
        is_payment_link_sent=True  # Only extend deadlines for bookings that received payment links
    )
    
    booking_count = bookings.count()
    print(f"Found {booking_count} bookings with status 'payment_not_done' that need updates.")
    
    if booking_count == 0:
        print("No bookings to process. Exiting.")
        return
    
    expiry_formatted = target_date.strftime("%d %b %Y, %I:%M %p")
    
    # Process each booking
    threads = []
    for booking in bookings:
        thread = threading.Thread(
            target=process_booking_extension,
            args=(booking, target_date, expiry_formatted)
        )
        threads.append(thread)
        thread.start()
        # Small delay to prevent overloading the mail server
        time.sleep(1)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Count successful and failed operations
    success_count = RoomBooking.objects.filter(
        status='payment_pending',
        payment_expiry=target_date
    ).count()
    
    failed_count = booking_count - success_count
    
    print(f"Payment deadlines extended: {success_count} successful, {failed_count} failed")
    logger.info(f"Payment deadlines extended: {success_count} successful, {failed_count} failed")

if __name__ == "__main__":
    # Run the main function in a separate thread
    main_thread = threading.Thread(target=extend_payment_deadlines)
    main_thread.start()
    
    print("Script started in background thread...")
    
    # Wait for the process to complete before exiting
    main_thread.join()
    print("Script completed!")