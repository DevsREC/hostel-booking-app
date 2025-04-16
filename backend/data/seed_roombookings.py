import os
import django
import csv
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_booking.settings')
django.setup()

from hostel.models import RoomBooking
from authentication.models import User

def create_room_bookings():
    # Read the vacated list CSV file
    with open('data/vacatedlist.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        next(reader)  # Skip title row
        next(reader)  # Skip empty row
        
        for row in reader:
            if not row or not row[0]:  # Skip empty rows
                continue
                
            try:
                # Extract data from CSV
                email = row[5].strip()
                
                # Get existing user
                try:
                    user = User.objects.get(email=email)
                    
                    # Create room booking
                    RoomBooking.objects.create(
                        user=user,
                        hostel_id=2,  # Hostel ID 2 as specified
                        status='confirmed',
                        food_type='Veg',  # Default to Veg
                        is_internal_booking=False,
                        booked_at=timezone.now(),
                        otp_verified_at=timezone.now(),
                        payment_completed_at=timezone.now(),
                        payment_expiry=timezone.now() + timedelta(days=5)
                    )
                    
                    print(f"Created booking for {user.name}")
                except User.DoesNotExist:
                    print(f"User with email {email} does not exist. Skipping...")
                
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {str(e)}")

if __name__ == '__main__':
    print("Starting to create room bookings...")
    create_room_bookings()
    print("Finished creating room bookings!") 