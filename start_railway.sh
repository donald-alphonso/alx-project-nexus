#!/bin/bash
# Script de démarrage Railway pour ALX Project Nexus

# Définir le port par défaut si pas défini
export PORT=${PORT:-8000}

echo "🚀 Démarrage ALX Project Nexus sur le port $PORT"

# Debug: Afficher les variables d'environnement liées à la base de données
echo "🔍 DEBUG: Variables d'environnement disponibles:"
echo "DATABASE_URL: ${DATABASE_URL:-'NON DÉFINIE'}"
echo "PGDATABASE: ${PGDATABASE:-'NON DÉFINIE'}"
echo "PGUSER: ${PGUSER:-'NON DÉFINIE'}"
echo "PGHOST: ${PGHOST:-'NON DÉFINIE'}"
echo "PGPORT: ${PGPORT:-'NON DÉFINIE'}"
echo "PGPASSWORD: ${PGPASSWORD:-'NON DÉFINIE (masqué)'}"
echo "POSTGRES_URL: ${POSTGRES_URL:-'NON DÉFINIE'}"
echo "DB_URL: ${DB_URL:-'NON DÉFINIE'}"
echo "🔍 Toutes les variables avec 'DATA' ou 'PG':"
env | grep -i -E '(data|pg|postgres)' || echo "Aucune variable trouvée"
echo "---"

# Migrations de base de données
echo "📊 Exécution des migrations..."
python manage.py migrate --noinput

# Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Création du superuser si nécessaire
echo "👤 Vérification du superuser..."
python manage.py shell << EOF
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
# S'assurer que Django utilise les bons settings
export DJANGO_SETTINGS_MODULE=social_media_backend.settings
exec gunicorn social_media_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
