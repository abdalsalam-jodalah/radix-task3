#!/bin/bash

# Start Redis in the background
redis-server --daemonize yes

# Wait for Redis to be available
sleep 3

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Start Celery worker in the background
celery -A authApi worker --loglevel=info &

# Run Django server
python manage.py runserver 0.0.0.0:8000
