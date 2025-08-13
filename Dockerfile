# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Django and other Python dependencies
RUN pip install --no-cache-dir \
    django==5.0.2 \
    djangorestframework==3.14.0 \
    django-cors-headers==4.3.1 \
    django-filter==23.5 \
    psycopg2-binary==2.9.9 \
    gunicorn==21.2.0 \
    celery==5.3.6 \
    redis==5.0.1 \
    graphene-django==3.2.0 \
    django-graphql-jwt==0.4.0 \
    pillow==10.2.0

# Set work directory
WORKDIR /app

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Create a simple entrypoint script
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo 'echo "Waiting for PostgreSQL..."' >> /entrypoint.sh && \
    echo 'while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do' >> /entrypoint.sh && \
    echo '  sleep 1' >> /entrypoint.sh && \
    echo 'done' >> /entrypoint.sh && \
    echo 'echo "PostgreSQL is available"' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo 'echo "Applying migrations..."' >> /entrypoint.sh && \
    echo 'python manage.py migrate --noinput' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo 'echo "Collecting static files..."' >> /entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput' >> /entrypoint.sh && \
    echo '' >> /entrypoint.sh && \
    echo 'echo "Starting server..."' >> /entrypoint.sh && \
    echo 'exec "$@"' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "social_media_backend.wsgi:application"]
