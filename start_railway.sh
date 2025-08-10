#!/bin/bash
# Script de démarrage Railway pour ALX Project Nexus

# Définir le port par défaut si pas défini
export PORT=${PORT:-8000}

echo "🚀 Démarrage ALX Project Nexus sur le port $PORT"

# Migrations de base de données
echo "📊 Exécution des migrations..."
python manage.py migrate --settings=social_media_backend.settings.production --noinput

# Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --settings=social_media_backend.settings.production --noinput

# Création du superuser si nécessaire
echo "👤 Vérification du superuser..."
python manage.py shell --settings=social_media_backend.settings.production << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@alxprojectnexus.com', 'admin123')
    print('✅ Superuser créé')
else:
    print('ℹ️ Superuser existe déjà')
EOF

# Démarrage du serveur
echo "🌐 Démarrage du serveur Gunicorn..."
exec gunicorn social_media_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
