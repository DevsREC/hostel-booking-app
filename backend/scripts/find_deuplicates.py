#!/usr/bin/env python

import os
import sys
import django
from django.core.exceptions import ValidationError

# Set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from django.utils import timezone
from hostel.models import Penalty
from django.db.models import Count, Max

def find_and_handle_duplicates():
    """
    Find duplicate Penalty entries (same user and hostel combination)
    and keep only the one with the latest payment_expiry.
    """
    # Find all user-hostel combinations with duplicates
    duplicates = Penalty.objects.values('user', 'hostel') \
        .annotate(count=Count('id'), max_expiry=Max('payment_expiry')) \
        .filter(count__gt=1)
    
    total_duplicates = 0
    total_deleted = 0
    
    print(f"Found {len(duplicates)} duplicate user-hostel combinations")
    
    for dup in duplicates:
        user_id = dup['user']
        hostel_id = dup['hostel']
        count = dup['count']
        latest_expiry = dup['max_expiry']
        
        print(f"\nProcessing user {user_id}, hostel {hostel_id} - {count} entries")
        print(f"Latest payment expiry in this group: {latest_expiry}")
        
        # Get all entries for this user-hostel combination
        entries = Penalty.objects.filter(
            user_id=user_id, 
            hostel_id=hostel_id
        ).order_by('-payment_expiry', '-booked_at')  # First by payment_expiry, then by booked_at
        
        # The first one is the one with latest payment_expiry - we'll keep this one
        keeper = entries.first()
        print(f"Keeping entry ID {keeper.id} with payment expiry {keeper.payment_expiry}")
        
        # Delete all others (skip the first one)
        for entry in entries[1:]:
            try:
                # Bypass the delete protection for this operation
                print(f"Deleting duplicate entry ID {entry.id} with payment expiry {entry.payment_expiry}")
                entry.delete()
                total_deleted += 1
            except Exception as e:
                print(f"Error deleting entry ID {entry.id}: {str(e)}")
        
        total_duplicates += (count - 1)
    
    print(f"\nProcessing complete. Found {total_duplicates} duplicate entries total.")
    print(f"Successfully deleted {total_deleted} duplicate entries.")

if __name__ == "__main__":
    print("Starting duplicate penalty cleanup...")
    find_and_handle_duplicates()
    print("Cleanup complete.")