# First set up Django environment before any imports
import os
import sys
import django
import requests

# Configure Django
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

# Now import after Django is configured
from hostel.models import RoomBooking  # Use absolute import path

def update_payment_status():
    api_end_point = 'https://edu.easebuzz.in/api/student/getStudentInstallment/'
    room_bookings = RoomBooking.objects.filter(status="payment_pending", is_payment_link_sent=True)
    print(room_bookings)
    print("This runs")
    for student in room_bookings:
        status = requests.post(
            api_end_point,
            {
                "institute_id": 3247,
                "student_prn": student.user.roll_no,
                "otp_code": "",
                "fees_password": "",
                "jsonData": 1
            }
        )
        if status.ok:
            print(status.json())  # Note: json is a method, not a property

if __name__ == "__main__":
    update_payment_status()