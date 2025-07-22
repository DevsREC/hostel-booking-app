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
        old_expiry_formatted = booking.payment_expiry.strftime("%d %b %Y, %I:%M %p")
        
        # Update payment expiry date
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
            template_name="payment_extension_template.html"
        )
        
        # Mark as extended to track this operation
        # booking.payment_deadline_extended = True
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
    
    # Get current date and target expiry date (May 1, 2025)
    now = timezone.now()
    target_date = timezone.make_aware(datetime(2025, 5, 1, 23, 59, 59))
    
    # Get bookings with payment expiry on or before May 1, 2025
    bookings = RoomBooking.objects.filter(
        status='payment_pending',
        payment_expiry__lte=target_date,
        is_payment_link_sent=True,  # Only extend deadlines for bookings that received payment links
        # payment_deadline_extended=False  # To avoid extending deadlines multiple times
    )
    
    booking_count = bookings.count()
    print(f"Found {booking_count} bookings that need payment deadline extensions.")
    
    if booking_count == 0:
        print("No bookings to process. Exiting.")
        return
    
    # Calculate new payment expiry (1 day after current expiry)
    threads = []
    for booking in bookings:
        # Add one day to the current expiry date
        new_expiry = booking.payment_expiry + timedelta(days=1)
        expiry_formatted = new_expiry.strftime("%d %b %Y, %I:%M %p")
        
        thread = threading.Thread(
            target=process_booking_extension,
            args=(booking, new_expiry, expiry_formatted)
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
        success_count += 1 


    
    print(f"Payment deadlines extended: {success_count} successful, {failed_count} failed")
    logger.info(f"Payment deadlines extended: {success_count} successful, {failed_count} failed")

if __name__ == "__main__":
    # Run the main function in a separate thread
    main_thread = threading.Thread(target=extend_payment_deadlines)
    main_thread.start()
    
    print("Script started in background thread...")
    
    # If you want to wait for the process to complete before exiting:
    main_thread.join()
    print("Script completed!")