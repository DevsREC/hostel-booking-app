import csv
import threading
import os
import sys
import django


current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from django.db import transaction
from authentication.models import User  # Replace 'your_app' with your actual app name
def create_user_from_row(row):
    try:
        with transaction.atomic():
            user = User.objects.create(
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                gender=row['gender'],
                roll_no=row['roll_no'],
                # Set default values for required fields
                year=row['year'],  # Default year, adjust as needed
                dept=row['dept'],  # Default department, adjust as needed
                phone_number=row['phone_number'],  # Default phone number
                parent_phone_number='0000000000',  # Default parent phone number
                password='changeme@123',  # Will be hashed by save()
                student_type=row['student_type'],  # Default student type
                degree_type='UG',  # Default degree type
                tution_fee=True  # Default tuition fee status
            )
            print(f"Created user: {user.email}")
    except Exception as e:
        print(f"Error creating user {row['user__email']}: {str(e)}")

def seed_users_from_csv(csv_file_path, num_threads=4):
    # Read CSV file
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
    
    # Split rows into chunks for each thread
    chunk_size = len(rows) // num_threads
    chunks = [rows[i:i + chunk_size] for i in range(0, len(rows), chunk_size)]
    
    # Create and start threads
    threads = []
    for chunk in chunks:
        thread = threading.Thread(
            target=lambda rows_chunk: [create_user_from_row(row) for row in rows_chunk],
            args=(chunk,)
        )
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print("Data seeding completed!")

if __name__ == "__main__":
    print("Running")
    csv_file_path = "User-2025-04-28.csv"
    seed_users_from_csv(csv_file_path, num_threads=4)