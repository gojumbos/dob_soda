# Base image for Python
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY . /app

# Install Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Expose the port
EXPOSE 8000

# Start Nginx and Gunicorn
CMD service nginx start && gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
