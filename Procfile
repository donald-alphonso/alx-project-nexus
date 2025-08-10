web: bash start_railway.sh
worker: celery -A social_media_backend worker --loglevel=info
beat: celery -A social_media_backend beat --loglevel=info
