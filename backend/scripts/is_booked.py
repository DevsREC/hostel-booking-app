#!/usr/bin/env python

import os
import sys
import django
import logging
import threading
import time
from datetime import datetime, timedelta
import csv

# Set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from hostel.models import RoomBooking
from authentication.models import User
def check_is_alloted():
    with open('./combined-special.csv', 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            try:    
                is_booking_there = RoomBooking.objects.get(user__roll_no=i[1], status='confirmed')
                if not is_booking_there:
                    print(i[1])
            except RoomBooking.DoesNotExist:
                try:
                    user = User.objects.get(roll_no=i[1])
                    print(int(i[1]), user.gender)  
                except User.DoesNotExist:
                    print("Not exist", i[1])
    
check_is_alloted()