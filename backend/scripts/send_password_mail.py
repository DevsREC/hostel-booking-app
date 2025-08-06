import django
import os
import sys
from threading import Thread
from queue import Queue

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from authentication.utils import send_email
from authentication.models import User
from django.contrib.auth.hashers import make_password

DEPT_MAPPING = {
    'Aeronautical Engineering': 'aero',
    'Artificial Intelligence & Data Science': 'aids',
    'Artificial Intelligence & Machine Learning': 'aiml',
    'Automobile Engineering': 'auto',
    'Biomedical Engineering': 'bme',
    'Biotechnology': 'bt',
    'Chemical Engineering': 'chem',
    'Civil Engineering': 'civil',
    'Computer Science & Business Systems': 'csbs',
    'Computer Science & Design': 'csd',
    'Computer Science & Engineering': 'cse',
    'Computer Science & Engineering (Cyber Security)': 'csecs',
    'Electrical & Electronics Engineering': 'eee',
    'Electronics & Communication Engineering': 'ece',
    'Food Technology': 'ft',
    'Information Technology': 'it',
    'Mechanical Engineering': 'mech',
    'Mechatronics Engineering': 'mct',
    'Robotics & Automation': 'rna',
}

# Worker function for threads
def email_worker(queue):
    while True:
        student_data = queue.get()
        if student_data is None:
            break
            
        student, dept_name = student_data
        # new_password = f"{student.student_id.first_name}.{student.batch}@{DEPT_MAPPING[dept_name]}${student.roll_no[-3:]}"
        new_password = "Changeme@123"
        user_name = student.get_name()
        student_email = student.email
        
        # Context for the email template
        context = {
            'student_name': user_name,
            'password': new_password,
            'student_email': student_email,
            'department': dept_name,
            'roll_no': student.roll_no
        }
        
        try:
            send_email(
                subject="Login Credential for Hostel Booking Portal",
                to_email=student_email,  # Changed to actual student email
                # to_email='cvignesh404@gmail.com',
                context=context,
                template_name='password_notify.html'
            )
            print(f"Password sent to {user_name} ({student_email})")
        except Exception as e:
            print(f"Failed to send email to {user_name} ({student_email}): {str(e)}")
        
        queue.task_done()

def send_password_mail():
    students_from_4th_year = User.objects.filter(year=1)
    
    # Create a queue and worker threads
    queue = Queue()
    num_worker_threads = 5  # Adjust based on your needs and email server limits
    
    threads = []
    for i in range(num_worker_threads):
        t = Thread(target=email_worker, args=(queue,))
        t.start()
        threads.append(t)
    
    # Add tasks to the queue
    for student in students_from_4th_year:
        dept_name = student.dept  # Using select_related to optimize
        queue.put((student, dept_name))
    
    # Block until all tasks are done
    queue.join()
    
    # Stop workers
    for i in range(num_worker_threads):
        queue.put(None)
    for t in threads:
        t.join()
        
    print("All emails processed")

if __name__ == '__main__':
    send_password_mail()