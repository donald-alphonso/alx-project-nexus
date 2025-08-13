#!/bin/bash
set -e

# Function to log messages
log_message() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Wait for PostgreSQL to be ready
log_message "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
  log_message "Still waiting for PostgreSQL..."
done
log_message "PostgreSQL is available"

# Apply database migrations
log_message "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if explicitly requested
if [ "$CREATE_SUPERUSER" = "true" ]; then
  log_message "Creating superuser..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${ADMIN_USERNAME:-admin}'
email = '${ADMIN_EMAIL:-admin@example.com}'
password = '${ADMIN_PASSWORD:-admin123}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser created: {username}')
else:
    print('Superuser already exists')
"
fi

# Create sample data if explicitly requested
if [ "$CREATE_SAMPLE_DATA" = "true" ]; then
  log_message "Creating sample data..."
  python manage.py create_sample_data --users 15 --posts 75
fi

# Collect static files
log_message "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
log_message "Starting Django server with command: $@"
exec "$@"
