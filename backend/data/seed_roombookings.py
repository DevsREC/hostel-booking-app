import os
import django
import csv
from datetime import datetime, timedelta
from django.utils import timezone
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from hostel.models import RoomBooking
from authentication.models import User

def create_room_bookings():
    # Read the vacated list CSV file
    with open('data/matched_roll_numbers_with_emails.csv', 'r') as file:
        reader = csv.reader(file)
        # next(reader)  # Skip header row
        
        for row in reader:
            if not row or len(row) < 2:  # Skip empty or incomplete rows
                continue
                
            try:
                # Extract data from CSV (assuming format: Roll No., E-mail ID)
                roll_number = row[0].strip()
                email = row[1].strip()
                
                # Get existing user
                try:
                    user = User.objects.get(roll_no=roll_number)
                    
                    # Create room booking
                    RoomBooking.objects.create(
                        user=user,
                        hostel_id=14,  # Hostel ID 6 as specified
                        status='confirmed',
                        food_type='Veg',  # Default to Non-veg
                        is_internal_booking=True,
                        booked_at=timezone.now(),
                        otp_verified_at=timezone.now(),
                        payment_completed_at=timezone.now(),
                        payment_expiry=timezone.now() + timedelta(days=5)
                    )
                    
                    print(f"Created booking for {user.first_name} (Roll No: {roll_number})")
                except User.DoesNotExist:
                    print(f"User with email {email} (Roll No: {roll_number}) does not exist. Skipping...")
                
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {str(e)}")

if __name__ == '__main__':
    print("Starting to create room bookings...")
    create_room_bookings()
    print("Finished creating room bookings!")