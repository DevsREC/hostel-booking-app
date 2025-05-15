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
from django.db.models import Q
from hostel.models import RoomBooking

def find_status_unknown():
    """Find bookings with empty, null, or invalid status values"""
    # Get the list of valid status choices from the model
    valid_statuses = [status[0] for status in RoomBooking.BOOKING_STATUS]
    
    # Find bookings where:
    # 1. Status is empty or null
    # 2. Status is not in the list of valid statuses
    bookings = RoomBooking.objects.filter(
        Q(status__isnull=True) | 
        Q(status='') | 
        ~Q(status__in=valid_statuses)
    )
    
    print(f"Found {bookings.count()} bookings with unknown status:")
    for booking in bookings:
        print(f"ID: {booking.id}, User: {booking.user}, Hostel: {booking.hostel}, "
              f"Status: '{booking.status}', Booked at: {booking.booked_at}")
    
    return bookings

def find_bookings_in_date_range(start_date=None, end_date=None):
    """Find bookings with payment_expiry in a specific date range"""
    if start_date is None:
        start_date = timezone.make_aware(datetime(2025, 5, 1, 0, 0, 0))
    if end_date is None:
        end_date = timezone.make_aware(datetime(2025, 5, 10, 23, 59, 59))
    
    # Find all bookings in the date range
    bookings = RoomBooking.objects.filter(
        payment_expiry__gte=start_date,
        payment_expiry__lte=end_date
    )
    
    print(f"\nFound {bookings.count()} bookings with payment_expiry between {start_date} and {end_date}:")
    for booking in bookings:
        print(f"ID: {booking.id}, User: {booking.user}, Hostel: {booking.hostel}, "
              f"Status: '{booking.status}', Payment Expiry: {booking.payment_expiry}")
    
    return bookings

if __name__ == "__main__":
    print("==== Looking for bookings with unknown status ====")
    unknown_status_bookings = find_status_unknown()
    
    print("\n==== Looking for bookings in date range ====")
    date_range_bookings = find_bookings_in_date_range()