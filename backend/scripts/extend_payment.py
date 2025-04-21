from django.utils import timezone
from datetime import timedelta
import os
import django
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from hostel.models import RoomBooking

def extend_payment_expiry():
    """
    Extends payment expiry by one day for all bookings with payment expiring today
    """
    # Get current date (start and end of day)
    today = timezone.now().date()
    start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
    
    # Find all bookings with payment status pending and expiry date today
    expiring_bookings = RoomBooking.objects.filter(
        status='payment_pending',
        payment_expiry__gte=start_of_day,
        payment_expiry__lte=end_of_day
    )
    
    count = 0
    for booking in expiring_bookings:
        # Extend by one day
        booking.payment_expiry = booking.payment_expiry + timedelta(days=1)
        booking.admin_notes = (booking.admin_notes or "") + f"\nPayment expiry extended by 1 day on {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
        booking.save()
        count += 1
    
    print(f"Successfully extended payment expiry for {count} bookings")
    return count