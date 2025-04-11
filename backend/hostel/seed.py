import os
import sys
import django
from django.db import transaction

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup() 

from hostel.models import Hostel

# Sample image URLs for hostels
SAMPLE_IMAGES = [
    "https://example.com/hostel1.jpg",
    "https://example.com/hostel2.jpg",
    "https://example.com/hostel3.jpg",
]

# Hostel data from the table
BOYS_HOSTELS = [
    {
        "name": "Category A - 2 AC A",
        "location": "BH2",
        "room_type": "AC",
        "food_type": "Veg",
        "no_of_rooms": 30,
        "person_per_room": 2,
        "gender": "M",
        "room_description": "2-person AC room with basic amenities and vegetarian food option",
        "bathroom_type": "Attached",
        "first_year_fee": 150000,
        "second_year_fee": 140000,
        "third_year_fee": 130000,
        "fourth_year_fee": 120000,
    },
    {
        "name": "Category B - 3 Non AC C",
        "location": "Thandalam",
        "room_type": "NON-AC",
        "food_type": "Non-veg",
        "no_of_rooms": 2,
        "person_per_room": 3,
        "gender": "M",
        "room_description": "3-person Non-AC room with basic amenities and non-vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 120000,
        "second_year_fee": 110000,
        "third_year_fee": 100000,
        "fourth_year_fee": 90000,
    },
    {
        "name": "Category C - 4 AC A",
        "location": "BH2",
        "room_type": "AC",
        "food_type": "Veg",
        "no_of_rooms": 79,
        "person_per_room": 4,
        "gender": "M",
        "room_description": "4-person AC room with premium amenities and vegetarian food option",
        "bathroom_type": "Attached",
        "first_year_fee": 100000,
        "second_year_fee": 90000,
        "third_year_fee": 80000,
        "fourth_year_fee": 70000,
    },
    {
        "name": "Category D - 4 Non AC A",
        "location": "Habitat",
        "room_type": "NON-AC",
        "food_type": "Non-veg",
        "no_of_rooms": 152,
        "person_per_room": 4,
        "gender": "M",
        "room_description": "4-person Non-AC room with premium amenities and non-vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 90000,
        "second_year_fee": 80000,
        "third_year_fee": 70000,
        "fourth_year_fee": 60000,
    },
    {
        "name": "Category E - 5 Non AC C",
        "location": "Thandalam",
        "room_type": "NON-AC",
        "food_type": "Non-veg",
        "no_of_rooms": 27,
        "person_per_room": 5,
        "gender": "M",
        "room_description": "5-person Non-AC room with basic amenities and non-vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 80000,
        "second_year_fee": 70000,
        "third_year_fee": 60000,
        "fourth_year_fee": 50000,
    },
    {
        "name": "Category F - 6 Non AC C",
        "location": "Habitat",
        "room_type": "NON-AC",
        "food_type": "Non-veg",
        "no_of_rooms": 240,
        "person_per_room": 6,
        "gender": "M",
        "room_description": "6-person Non-AC room with basic amenities and non-vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 70000,
        "second_year_fee": 60000,
        "third_year_fee": 50000,
        "fourth_year_fee": 40000,
    },
]

GIRLS_HOSTELS = [
    {
        "name": "Category A - 2 AC A (GH1)",
        "location": "GH1 (BH3)",
        "room_type": "AC",
        "food_type": "Veg",
        "no_of_rooms": 6,
        "person_per_room": 2,
        "gender": "F",
        "room_description": "2-person AC room with premium amenities and vegetarian food option",
        "bathroom_type": "Attached",
        "first_year_fee": 150000,
        "second_year_fee": 140000,
        "third_year_fee": 130000,
        "fourth_year_fee": 120000,
    },
    {
        "name": "Category A - 2 AC A (GH2)",
        "location": "GH2",
        "room_type": "AC",
        "food_type": "Veg",
        "no_of_rooms": 27,
        "person_per_room": 2,
        "gender": "F",
        "room_description": "2-person AC room with premium amenities and vegetarian food option",
        "bathroom_type": "Attached",
        "first_year_fee": 150000,
        "second_year_fee": 140000,
        "third_year_fee": 130000,
        "fourth_year_fee": 120000,
    },
    {
        "name": "Category A - 2 AC A (GH3)",
        "location": "GH3 (BH1)",
        "room_type": "AC",
        "food_type": "Veg",
        "no_of_rooms": 6,
        "person_per_room": 2,
        "gender": "F",
        "room_description": "2-person AC room with premium amenities and vegetarian food option",
        "bathroom_type": "Attached",
        "first_year_fee": 150000,
        "second_year_fee": 140000,
        "third_year_fee": 130000,
        "fourth_year_fee": 120000,
    },
    {
        "name": "Category B - 2 Non AC C (GH1)",
        "location": "GH1 (BH3)",
        "room_type": "NON-AC",
        "food_type": "Veg",
        "no_of_rooms": 118,
        "person_per_room": 2,
        "gender": "F",
        "room_description": "2-person Non-AC room with basic amenities and vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 120000,
        "second_year_fee": 110000,
        "third_year_fee": 100000,
        "fourth_year_fee": 90000,
    },
    {
        "name": "Category B - 2 Non AC C (GH3)",
        "location": "GH3 (BH1)",
        "room_type": "NON-AC",
        "food_type": "Veg",
        "no_of_rooms": 43,
        "person_per_room": 2,
        "gender": "F",
        "room_description": "2-person Non-AC room with basic amenities and vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 120000,
        "second_year_fee": 110000,
        "third_year_fee": 100000,
        "fourth_year_fee": 90000,
    },
    {
        "name": "Category C - 3 AC A",
        "location": "GH3 (BH1)",
        "room_type": "AC",
        "food_type": "Veg",
        "no_of_rooms": 12,
        "person_per_room": 3,
        "gender": "F",
        "room_description": "3-person AC room with premium amenities and vegetarian food option",
        "bathroom_type": "Attached",
        "first_year_fee": 100000,
        "second_year_fee": 90000,
        "third_year_fee": 80000,
        "fourth_year_fee": 70000,
    },
    {
        "name": "Category D - 3 Non AC C",
        "location": "GH3 (BH1)",
        "room_type": "NON-AC",
        "food_type": "Veg",
        "no_of_rooms": 80,
        "person_per_room": 3,
        "gender": "F",
        "room_description": "3-person Non-AC room with basic amenities and vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 90000,
        "second_year_fee": 80000,
        "third_year_fee": 70000,
        "fourth_year_fee": 60000,
    },
    {
        "name": "Category E - 4 Non AC C",
        "location": "GH3 (BH1)",
        "room_type": "NON-AC",
        "food_type": "Veg",
        "no_of_rooms": 19,
        "person_per_room": 4,
        "gender": "F",
        "room_description": "4-person Non-AC room with basic amenities and vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 80000,
        "second_year_fee": 70000,
        "third_year_fee": 60000,
        "fourth_year_fee": 50000,
    },
    {
        "name": "Category F - 4 Non AC A",
        "location": "GH2",
        "room_type": "NON-AC",
        "food_type": "Veg",
        "no_of_rooms": 178,
        "person_per_room": 4,
        "gender": "F",
        "room_description": "4-person Non-AC room with premium amenities and vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 90000,
        "second_year_fee": 80000,
        "third_year_fee": 70000,
        "fourth_year_fee": 60000,
    },
    {
        "name": "Category G - 6 Non AC C",
        "location": "GH1 (BH3)",
        "room_type": "NON-AC",
        "food_type": "Veg",
        "no_of_rooms": 13,
        "person_per_room": 6,
        "gender": "F",
        "room_description": "6-person Non-AC room with basic amenities and vegetarian food option",
        "bathroom_type": "Common",
        "first_year_fee": 70000,
        "second_year_fee": 60000,
        "third_year_fee": 50000,
        "fourth_year_fee": 40000,
    },
]

def seed_hostels():
    """
    Seed the database with hostel data
    """
    try:
        with transaction.atomic():
            # Clear existing hostels
            Hostel.objects.all().delete()
            
            # Add boys hostels
            for hostel_data in BOYS_HOSTELS:
                Hostel.objects.create(
                    **hostel_data,
                    image=SAMPLE_IMAGES[0]  # Using a sample image
                )
            
            # Add girls hostels
            for hostel_data in GIRLS_HOSTELS:
                Hostel.objects.create(
                    **hostel_data,
                    image=SAMPLE_IMAGES[0]  # Using a sample image
                )
            
            print("Successfully seeded hostel data!")
            print(f"Added {len(BOYS_HOSTELS)} boys hostels")
            print(f"Added {len(GIRLS_HOSTELS)} girls hostels")
            print(f"Total capacity - Boys: 2565, Girls: 1542")
            
    except Exception as e:
        print(f"Error seeding hostel data: {str(e)}")

if __name__ == "__main__":
    seed_hostels() 