#!/usr/bin/env python

import os
import sys
import django
import csv

# Set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q
from hostel.models import RoomBooking
from authentication.models import User  # Assuming this is your User model

def update_status_from_csv(csv_file_path):
    """
    Read from a CSV file with columns: user__roll_no, user__email, status
    Update the status of the corresponding RoomBooking records to 'confirmed'
    """
    updated_count = 0
    not_found_count = 0
    already_confirmed_count = 0
    errors = []
    
    print(f"Reading from CSV file: {csv_file_path}")
    
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                try:
                    roll_no = row.get('user__roll_no')
                    email = row.get('user__email')
                    status = row.get('status', '').strip().lower()
                    
                    # Skip if no roll number or email is provided
                    if not roll_no and not email:
                        errors.append(f"Missing both roll_no and email in row: {row}")
                        continue
                    
                    if status != 'confirmed':
                        errors.append(f"Skipping row with status '{status}' (not 'confirmed'): {row}")
                        continue
                    
                    # Find the user
                    user_query = Q()
                    if roll_no:
                        user_query |= Q(roll_no=roll_no)
                    if email:
                        user_query |= Q(email=email)
                    
                    user = User.objects.filter(user_query).first()
                    
                    if not user:
                        not_found_count += 1
                        errors.append(f"User not found with roll_no={roll_no}, email={email}")
                        continue
                    
                    # Find all bookings for this user
                    bookings = RoomBooking.objects.filter(user=user)
                    
                    if not bookings.exists():
                        not_found_count += 1
                        errors.append(f"No bookings found for user {user.email} ({user.roll_no})")
                        continue
                    
                    # Update each booking status
                    for booking in bookings:
                        if booking.status == 'confirmed':
                            already_confirmed_count += 1
                            print(f"Booking already confirmed for {user.email} ({user.roll_no})")
                        else:
                            old_status = booking.status
                            booking.status = 'confirmed'
                            # Set payment_completed_at if it's not set
                            if not booking.payment_completed_at:
                                booking.payment_completed_at = timezone.now()
                            booking.save(update_fields=['status', 'payment_completed_at'])
                            updated_count += 1
                            print(f"Updated booking for {user.email} ({user.roll_no}): {old_status} -> confirmed")
                
                except Exception as e:
                    errors.append(f"Error processing row {row}: {str(e)}")
    
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return
    
    # Print summary
    print("\n===== Summary =====")
    print(f"Total records updated: {updated_count}")
    print(f"Already confirmed records: {already_confirmed_count}")
    print(f"Records not found: {not_found_count}")
    print(f"Errors encountered: {len(errors)}")
    
    if errors:
        print("\n===== Errors =====")
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_status_from_csv.py path/to/your/file.csv")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        sys.exit(1)
    
    update_status_from_csv(csv_file_path)