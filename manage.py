#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time
import traceback

def wait_for_db(retries=5, delay=3):
    """Waits for the database to be available before proceeding."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authApi.settings")
    
    import django
    django.setup()
    
    from django.db import connections
    from django.db.utils import OperationalError
    
    for attempt in range(retries):
        try:
            connections["default"].ensure_connection()
            return  # Connection successful
        except OperationalError:
            print(f"\n⚠️ Database connection failed. Retrying in {delay} seconds... (Attempt {attempt+1}/{retries})")
            time.sleep(delay)

    print("\n❌ Database connection error: MySQL server is not running or credentials are incorrect.")
    sys.exit(1)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authApi.settings")

    if "runserver" in sys.argv or "migrate" in sys.argv:
        wait_for_db()

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and available "
            "on your PYTHONPATH. Did you forget to activate a virtual environment?"
        ) from exc
    except Exception as e:
        print (f"Unexpected Error: {e}\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
