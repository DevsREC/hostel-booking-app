#!/usr/bin/env python

import os
import sys
import django
import logging
from datetime import datetime, timedelta

# Set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from django.utils import timezone
from hostel.models import RoomBooking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('payment_status_reset.log')
    ]
)
logger = logging.getLogger(__name__)

def reset_payment_status():
    """
    Get students who confirmed their payment on April 29th, 2024,
    and reset their is_payment_link_sent status to False
    """
    print("Script is running...")
    
    # Define the target date (April 29th, 2024)
    target_date = datetime(2024, 4, 29)
    
    # Create datetime range for the entire day (start and end of day)
    start_of_day = timezone.make_aware(datetime(2025, 4, 29, 0, 0, 0))
    end_of_day = timezone.make_aware(datetime(2025, 4, 29, 23, 59, 59))
    
    # Find bookings with payment confirmation on April 29th, 2024
    bookings = RoomBooking.objects.filter(
        otp_verified_at__gte=start_of_day,
        otp_verified_at__lte=end_of_day
    )
    
    booking_count = bookings.count()
    print(f"Found {booking_count} bookings with payment confirmed on April 29th, 2024.")
    
    if booking_count == 0:
        print("No bookings to process. Exiting.")
        return
    
    # Reset is_payment_link_sent to False for found bookings
    updated_count = 0
    for booking in bookings:
        try:
            booking.is_payment_link_sent = False
            booking.save()
            updated_count += 1
            
            logger.info(f"Reset payment link status for booking ID: {booking.id}, User: {booking.user.email}")
            print(f"Reset payment link status for booking ID: {booking.id}, User: {booking.user.email}")
            
        except Exception as e:
            error_msg = f"Failed to update booking ID {booking.id}: {str(e)}"
            logger.error(error_msg)
            print(error_msg)
    
    print(f"Successfully reset {updated_count} out of {booking_count} bookings.")
    logger.info(f"Successfully reset {updated_count} out of {booking_count} bookings.")

if __name__ == "__main__":
    reset_payment_status()
    print("Script completed!")