#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time
import django.db.utils
import pymysql

def wait_for_db(retries=5, delay=3):
    """Retry connecting to the database before proceeding."""
    for attempt in range(retries):
        try:
            import django
            from django.db import connections
            django.setup()
            connections["default"].cursor()
            return  # Connection successful
        except (django.db.utils.OperationalError, pymysql.err.OperationalError):
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
    except django.db.utils.OperationalError:
        print("\n❌ Database connection error: MySQL server is not running. Please start the database and try again.\n")
        sys.exit(1)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
