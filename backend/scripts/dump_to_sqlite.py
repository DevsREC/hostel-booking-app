import os
import sys
import django
import sqlite3
import subprocess
import tempfile

# Configure Django
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Booking.settings')
django.setup()

from django.db import connections
from django.core.management import call_command

def import_sql_to_sqlite(sql_dump_path, sqlite_db_path):
    # Create a temporary PostgreSQL database to import the dump
    temp_db_name = "temp_import_db"
    
    # Import the SQL dump to the temporary PostgreSQL database
    subprocess.run([
        "createdb", temp_db_name
    ])
    
    subprocess.run([
        "psql", "-d", temp_db_name, "-f", sql_dump_path
    ])
    
    # Use Django's dumpdata to export as JSON
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        temp_json_path = tmp.name
    
    # Configure a temporary connection to the PostgreSQL database
    temp_db_settings = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': temp_db_name,
        'USER': 'postgres',  # Adjust to your PostgreSQL user
        'PASSWORD': '',      # Adjust to your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
    # Add the temporary connection
    connections.databases['temp_db'] = temp_db_settings
    
    # Dump data from PostgreSQL to JSON
    call_command('dumpdata', '--database', 'temp_db', '--output', temp_json_path)
    
    # Configure connection to SQLite
    sqlite_settings = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlite_db_path,
    }
    connections.databases['sqlite_db'] = sqlite_settings
    
    # Load data from JSON to SQLite
    call_command('loaddata', temp_json_path, '--database', 'sqlite_db')
    
    # Clean up
    os.unlink(temp_json_path)
    subprocess.run(["dropdb", temp_db_name])
    
    print(f"Successfully imported data to SQLite database at {sqlite_db_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python import_to_sqlite.py <sql_dump_path> <sqlite_db_path>")
        sys.exit(1)
        
    import_sql_to_sqlite(sys.argv[1], sys.argv[2])