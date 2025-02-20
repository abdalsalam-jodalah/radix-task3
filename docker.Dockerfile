# Use official Python image as base
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose ports (Django runs on 8000)
EXPOSE 8000

# Start script to handle migrations, Redis, Celery, and Django
CMD ["sh", "./start.sh"]
