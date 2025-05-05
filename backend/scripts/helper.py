#!/usr/bin/env python
import os
import sys
import django
from collections import defaultdict
from datetime import datetime

# Setup Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

# Import your models (after Django setup)
from hostel.models import RoomBooking  # Replace with your actual app name

def find_duplicate_bookings():
    """
    Find duplicate bookings where a user has multiple bookings in active statuses.
    Active statuses are: 'payment_pending', 'otp_pending', 'confirmed'
    """
    print("Searching for duplicate bookings...")
    
    # Get all bookings with active statuses
    active_statuses = ['payment_pending', 'otp_pending', 'confirmed']
    bookings = RoomBooking.objects.filter(status__in=active_statuses)
    
    # Group bookings by user
    user_bookings = defaultdict(list)
    for booking in bookings:
        user_bookings[booking.user.id].append(booking)
    
    # Find users with multiple active bookings
    duplicates_found = False
    for user_id, user_bookings_list in user_bookings.items():
        if len(user_bookings_list) > 1:
            duplicates_found = True
            user = user_bookings_list[0].user
            print(f"\nDuplicate bookings found for user: {user.email} (ID: {user_id})")
            print("-" * 80)
            
            for i, booking in enumerate(user_bookings_list, 1):
                print(f"Booking #{i}:")
                print(f"Booking UserL {booking.user}")
                print(f"  Hostel: {booking.hostel.name}")
                print(f"  Status: {booking.status}")
                print(f"  Booked at: {booking.booked_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Food type: {booking.food_type}")
                print(f"  Internal booking: {'Yes' if booking.is_internal_booking else 'No'}")
                if booking.payment_completed_at:
                    print(f"  Payment completed: {booking.payment_completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Booking ID: {booking.id}")
                print()
    
    if not duplicates_found:
        print("No duplicate bookings found.")
    else:
        print("Analysis complete. See above for duplicate bookings.")

def get_all_user_bookings(email):
    """
    Get all bookings for a specific user by email address.
    """
    try:
        from authentication.models import User  # Replace with your actual user model import
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f"No user found with email: {email}")
            return
        
        bookings = RoomBooking.objects.filter(user=user)
        
        if not bookings.exists():
            print(f"No bookings found for user: {email}")
            return
        
        print(f"\nAll bookings for user: {email} (ID: {user.id})")
        print("-" * 80)
        
        for i, booking in enumerate(bookings, 1):
            print(f"Booking #{i}:")
            print(f"  Hostel: {booking.hostel.name}")
            print(f"  Status: {booking.status}")
            print(f"  Booked at: {booking.booked_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Food type: {booking.food_type}")
            print(f"  Internal booking: {'Yes' if booking.is_internal_booking else 'No'}")
            if booking.payment_completed_at:
                print(f"  Payment completed: {booking.payment_completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Booking ID: {booking.id}")
            print()
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage:")
            print("  python find_duplicate_bookings.py             - Find all duplicate bookings")
            print("  python find_duplicate_bookings.py user_email  - Find all bookings for a specific user")
        else:
            user_email = sys.argv[1]
            get_all_user_bookings(user_email)
    else:
        find_duplicate_bookings()