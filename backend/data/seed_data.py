import os
import csv
import django
import sys
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from authentication.models import User
from django.contrib.auth.hashers import make_password

def create_user(row: Dict) -> None:
    """Create a single user from a row of data."""
    try:
        user = User.objects.create(
            email=row['email'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            year=int(row['year']),
            dept=row['dept'],
            roll_no=row['roll_no'],
            phone_number=row['phone_number'],
            parent_phone_number=row.get('parent_phone_number', '0000000000'),
            gender=row['gender'],
            tution_fee=True,
            student_type='Mgmt'
        )
        
        user.set_password("changeme@123")
        user.save()
        
        print(f"Created user: {user.email}")
        
    except Exception as e:
        print(f"Error creating user from row: {row}")
        print(f"Error details: {str(e)}")

def process_csv_file(file_path: str) -> None:
    """Process a single CSV file using multiple threads."""
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found. Skipping...")
        return
        
    print(f"Processing {os.path.basename(file_path)}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)  # Convert to list for threading
            
            # Use ThreadPoolExecutor for parallel processing of rows
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(create_user, rows)
                
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

def seed_data():
    """Main function to seed data using multiple processes."""
    # List of CSV files to process
    csv_files = [
        '2thyear_final.csv',
        '3thyear_final.csv',
        '4thyear_final.csv'
    ]
    
    # Base directory where CSV files are located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create full paths for CSV files
    file_paths = [os.path.join(base_dir, csv_file) for csv_file in csv_files]
    
    # Use multiprocessing to handle multiple files concurrently
    with multiprocessing.Pool(processes=min(len(file_paths), multiprocessing.cpu_count())) as pool:
        pool.map(process_csv_file, file_paths)

if __name__ == '__main__':
    print("Starting data seeding...")
    seed_data()
    print("Data seeding completed!") 