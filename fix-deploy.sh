#!/bin/bash

# Ce script aide à résoudre le problème de déploiement en copiant les fichiers nécessaires
# dans le répertoire temporaire utilisé par le script deploy-traefik.sh

set -e

# Trouver le fichier docker-compose.yml temporaire créé par le script de déploiement
TEMP_COMPOSE=$(find /tmp -name "*-compose.yml" -type f -mmin -5 2>/dev/null | head -n 1)

if [ -z "$TEMP_COMPOSE" ]; then
    echo "❌ Aucun fichier docker-compose.yml temporaire trouvé"
    echo "Exécutez d'abord ./deploy-traefik.sh alx-project-nexus"
    exit 1
fi

# Obtenir le répertoire temporaire
TEMP_DIR=$(dirname "$TEMP_COMPOSE")

echo "🔍 Fichier temporaire trouvé: $TEMP_COMPOSE"
echo "📁 Répertoire temporaire: $TEMP_DIR"

# Copier les fichiers nécessaires
echo "📋 Copie des fichiers nécessaires..."
cp Dockerfile "$TEMP_DIR/"
cp entrypoint.sh "$TEMP_DIR/" 2>/dev/null || echo "⚠️ entrypoint.sh non trouvé (ce n'est pas grave)"
cp -r . "$TEMP_DIR/src" 2>/dev/null || mkdir -p "$TEMP_DIR/src"

echo "✅ Fichiers copiés avec succès"
echo "🚀 Vous pouvez maintenant continuer le déploiement"
