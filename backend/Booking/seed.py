import os
import django
from django.db import transaction

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
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
        "room_type": "2 AC A",
        "food_type": "Veg",
        "available_rooms": 30,
        "person_per_room": 2,
        "gender": "M",
        "amount": 15000,  # Monthly amount (example)
        "room_description": "2-person AC room with basic amenities and vegetarian food option",
    },
    {
        "name": "Category B - 3 Non AC C",
        "location": "Thandalam",
        "room_type": "3 Non AC C",
        "food_type": "Non Veg",
        "available_rooms": 2,
        "person_per_room": 3,
        "gender": "M",
        "amount": 8000,  # Monthly amount (example)
        "room_description": "3-person Non-AC room with basic amenities and non-vegetarian food option",
    },
    {
        "name": "Category C - 4 AC A",
        "location": "BH2",
        "room_type": "4 AC A",
        "food_type": "Veg",
        "available_rooms": 79,
        "person_per_room": 4,
        "gender": "M",
        "amount": 12000,  # Monthly amount (example)
        "room_description": "4-person AC room with premium amenities and vegetarian food option",
    },
    {
        "name": "Category D - 4 Non AC A",
        "location": "Habitat",
        "room_type": "4 Non AC A",
        "food_type": "Non Veg",
        "available_rooms": 152,
        "person_per_room": 4,
        "gender": "M",
        "amount": 10000,  # Monthly amount (example)
        "room_description": "4-person Non-AC room with premium amenities and non-vegetarian food option",
    },
    {
        "name": "Category E - 5 Non AC C",
        "location": "Thandalam",
        "room_type": "5 Non AC C",
        "food_type": "Non Veg",
        "available_rooms": 27,
        "person_per_room": 5,
        "gender": "M",
        "amount": 7000,  # Monthly amount (example)
        "room_description": "5-person Non-AC room with basic amenities and non-vegetarian food option",
    },
    {
        "name": "Category F - 6 Non AC C",
        "location": "Habitat",
        "room_type": "6 Non AC C",
        "food_type": "Non Veg",
        "available_rooms": 240,
        "person_per_room": 6,
        "gender": "M",
        "amount": 6000,  # Monthly amount (example)
        "room_description": "6-person Non-AC room with basic amenities and non-vegetarian food option",
    },
]

GIRLS_HOSTELS = [
    {
        "name": "Category A - 2 AC A (GH1)",
        "location": "GH1 (BH3)",
        "room_type": "2 AC A",
        "food_type": "Veg",
        "available_rooms": 6,
        "person_per_room": 2,
        "gender": "F",
        "amount": 15000,  # Monthly amount (example)
        "room_description": "2-person AC room with premium amenities and vegetarian food option",
    },
    {
        "name": "Category A - 2 AC A (GH2)",
        "location": "GH2",
        "room_type": "2 AC A",
        "food_type": "Veg",
        "available_rooms": 27,
        "person_per_room": 2,
        "gender": "F",
        "amount": 15000,  # Monthly amount (example)
        "room_description": "2-person AC room with premium amenities and vegetarian food option",
    },
    {
        "name": "Category A - 2 AC A (GH3)",
        "location": "GH3 (BH1)",
        "room_type": "2 AC A",
        "food_type": "Veg",
        "available_rooms": 6,
        "person_per_room": 2,
        "gender": "F",
        "amount": 15000,  # Monthly amount (example)
        "room_description": "2-person AC room with premium amenities and vegetarian food option",
    },
    {
        "name": "Category B - 2 Non AC C (GH1)",
        "location": "GH1 (BH3)",
        "room_type": "2 Non AC C",
        "food_type": "Veg",
        "available_rooms": 118,
        "person_per_room": 2,
        "gender": "F",
        "amount": 10000,  # Monthly amount (example)
        "room_description": "2-person Non-AC room with basic amenities and vegetarian food option",
    },
    {
        "name": "Category B - 2 Non AC C (GH3)",
        "location": "GH3 (BH1)",
        "room_type": "2 Non AC C",
        "food_type": "Veg",
        "available_rooms": 43,
        "person_per_room": 2,
        "gender": "F",
        "amount": 10000,  # Monthly amount (example)
        "room_description": "2-person Non-AC room with basic amenities and vegetarian food option",
    },
    {
        "name": "Category C - 3 AC A",
        "location": "GH3 (BH1)",
        "room_type": "3 AC A",
        "food_type": "Veg",
        "available_rooms": 12,
        "person_per_room": 3,
        "gender": "F",
        "amount": 12000,  # Monthly amount (example)
        "room_description": "3-person AC room with premium amenities and vegetarian food option",
    },
    {
        "name": "Category D - 3 Non AC C",
        "location": "GH3 (BH1)",
        "room_type": "3 Non AC C",
        "food_type": "Veg",
        "available_rooms": 80,
        "person_per_room": 3,
        "gender": "F",
        "amount": 9000,  # Monthly amount (example)
        "room_description": "3-person Non-AC room with basic amenities and vegetarian food option",
    },
    {
        "name": "Category E - 4 Non AC C",
        "location": "GH3 (BH1)",
        "room_type": "4 Non AC C",
        "food_type": "Veg",
        "available_rooms": 19,
        "person_per_room": 4,
        "gender": "F",
        "amount": 8000,  # Monthly amount (example)
        "room_description": "4-person Non-AC room with basic amenities and vegetarian food option",
    },
    {
        "name": "Category F - 4 Non AC A",
        "location": "GH2",
        "room_type": "4 Non AC A",
        "food_type": "Veg",
        "available_rooms": 178,
        "person_per_room": 4,
        "gender": "F",
        "amount": 10000,  # Monthly amount (example)
        "room_description": "4-person Non-AC room with premium amenities and vegetarian food option",
    },
    {
        "name": "Category G - 6 Non AC C",
        "location": "GH1 (BH3)",
        "room_type": "6 Non AC C",
        "food_type": "Veg",
        "available_rooms": 13,
        "person_per_room": 6,
        "gender": "F",
        "amount": 6000,  # Monthly amount (example)
        "room_description": "6-person Non-AC room with basic amenities and vegetarian food option",
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