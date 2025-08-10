web: gunicorn social_media_backend.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A social_media_backend worker --loglevel=info
beat: celery -A social_media_backend beat --loglevel=info
