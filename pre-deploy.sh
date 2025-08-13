#!/bin/bash

# Ce script prépare les fichiers nécessaires pour le déploiement
# Il doit être exécuté avant le script deploy-traefik.sh

set -e

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "docker-compose.yml" ] || [ ! -f "Dockerfile" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis la racine du projet"
    exit 1
fi

# Créer un répertoire temporaire pour le déploiement
TMP_DIR="/tmp/deploy-$(whoami)-$(date +%s)"
mkdir -p "$TMP_DIR"

# Copier les fichiers nécessaires
cp docker-compose.yml "$TMP_DIR/"
cp Dockerfile "$TMP_DIR/"
cp entrypoint.sh "$TMP_DIR/" 2>/dev/null || echo "⚠️ entrypoint.sh non trouvé, utilisation de celui dans le Dockerfile"
cp -r . "$TMP_DIR/app"

echo "✅ Fichiers préparés dans $TMP_DIR"
echo "Utilisez maintenant le script de déploiement avec:"
echo "./deploy-traefik.sh alx-project-nexus"
echo "Ou construisez l'image manuellement avec:"
echo "cd $TMP_DIR && docker build -t \${STACK_NAME}-backend:latest ."
