#!/usr/bin/env python
import django
import os
import sys
from collections import defaultdict

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

# Import the RoomBooking model (adjust the import path as needed)
from hostel.models import RoomBooking

def find_duplicate_bookings():
    """
    Find all instances where a user has multiple bookings with the same status.
    """
    print("Finding duplicate bookings where users have multiple bookings with the same status...")
    
    # Get all bookings ordered by user and status
    all_bookings = RoomBooking.objects.all().order_by('user', 'status')
    
    # Group bookings by user and status
    duplicates = defaultdict(list)
    for booking in all_bookings:
        key = (booking.user.id, booking.status)
        duplicates[key].append(booking)
    
    # Filter for groups with more than one booking
    duplicate_bookings = {k: v for k, v in duplicates.items() if len(v) > 1}
    
    # Display results
    if not duplicate_bookings:
        print("No duplicate bookings found.")
        return
    
    print("\n==== DUPLICATE BOOKINGS ====\n")
    for (user_id, status), bookings in duplicate_bookings.items():
        user_email = bookings[0].user.email
        print(f"User: {user_email} (ID: {user_id})")
        print(f"Status: {status}")
        print(f"Number of duplicate bookings: {len(bookings)}")
        
        print("\nDetails:")
        for i, booking in enumerate(bookings, 1):
            print(f"  {i}. Booking ID: {booking.id}")
            print(f"     Hostel: {booking.hostel.name}")
            print(f"     Booked at: {booking.booked_at}")
            print(f"     Food type: {booking.food_type}")
            print(f"     Internal booking: {booking.is_internal_booking}")
            print()
        print("-" * 50)

if __name__ == "__main__":
    find_duplicate_bookings()