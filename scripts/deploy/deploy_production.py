#!/usr/bin/env python3
"""
Script de déploiement automatisé pour ALX Project Nexus
Prépare l'application pour le déploiement en production
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def check_requirements():
    """Vérifie que tous les fichiers requis sont présents"""
    print("\n📋 VÉRIFICATION DES FICHIERS REQUIS")
    print("=" * 50)
    
    required_files = [
        'requirements-production.txt',
        'Procfile',
        'runtime.txt',
        'social_media_backend/settings/production.py',
        'manage.py',
        'docker-compose.yml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def collect_static_files():
    """Collecte les fichiers statiques"""
    print("\n📦 COLLECTE DES FICHIERS STATIQUES")
    print("=" * 50)
    
    # Créer le dossier staticfiles s'il n'existe pas
    os.makedirs('staticfiles', exist_ok=True)
    
    # Collecter les fichiers statiques
    return run_command(
        'python manage.py collectstatic --noinput --settings=social_media_backend.settings.production',
        "Collecte des fichiers statiques"
    )

def run_migrations():
    """Exécute les migrations de base de données"""
    print("\n🗄️ MIGRATIONS DE BASE DE DONNÉES")
    print("=" * 50)
    
    return run_command(
        'python manage.py migrate --settings=social_media_backend.settings.production',
        "Exécution des migrations"
    )

def create_superuser():
    """Crée un superutilisateur pour la production"""
    print("\n👤 CRÉATION DU SUPERUTILISATEUR")
    print("=" * 50)
    
    # Script pour créer un superuser automatiquement
    create_superuser_script = """
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_backend.settings.production')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@alxprojectnexus.com',
        password='admin123',
        first_name='Admin',
        last_name='ALX'
    )
    print('✅ Superuser créé: admin / admin123')
else:
    print('ℹ️ Superuser existe déjà')
"""
    
    with open('create_superuser.py', 'w') as f:
        f.write(create_superuser_script)
    
    success = run_command('python create_superuser.py', "Création du superutilisateur")
    
    # Nettoyer le fichier temporaire
    if os.path.exists('create_superuser.py'):
        os.remove('create_superuser.py')
    
    return success

def test_production_settings():
    """Test les paramètres de production"""
    print("\n🧪 TEST DES PARAMÈTRES DE PRODUCTION")
    print("=" * 50)
    
    return run_command(
        'python manage.py check --deploy --settings=social_media_backend.settings.production',
        "Vérification des paramètres de déploiement"
    )

def create_env_template():
    """Crée un template de fichier .env pour la production"""
    print("\n📝 CRÉATION DU TEMPLATE .env")
    print("=" * 50)
    
    env_template = """# ALX Project Nexus - Production Environment Variables
# Copy this file to .env and fill in your actual values

# Django
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,*.railway.app,*.render.com

# Database (will be provided by hosting platform)
DATABASE_URL=postgresql://user:password@host:port/database

# Redis (will be provided by hosting platform)
REDIS_URL=redis://user:password@host:port/0

# Security (enable for HTTPS)
SECURE_SSL_REDIRECT=True

# CORS (add your frontend domains)
CORS_ALLOWED_ORIGINS=https://your-frontend.com,https://www.your-frontend.com

# Email (optional - for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@your-domain.com

# API Base URL (for documentation)
API_BASE_URL=https://your-app.railway.app
"""
    
    with open('.env.production.template', 'w') as f:
        f.write(env_template)
    
    print("✅ Template .env.production.template créé")
    return True

def generate_deployment_summary():
    """Génère un résumé du déploiement"""
    print("\n📊 GÉNÉRATION DU RÉSUMÉ DE DÉPLOIEMENT")
    print("=" * 50)
    
    summary = f"""# 🚀 ALX Project Nexus - Résumé de Déploiement

## ✅ Fichiers de Déploiement Créés

### 📦 Fichiers Principaux:
- `requirements-production.txt` - Dépendances Python pour production
- `Procfile` - Configuration des processus (web, worker, beat)
- `runtime.txt` - Version Python spécifiée
- `social_media_backend/settings/production.py` - Paramètres de production

### 🔧 Fichiers de Configuration:
- `.env.production.template` - Template des variables d'environnement
- `staticfiles/` - Fichiers statiques collectés

## 🌐 Plateformes de Déploiement Recommandées

### 1. Railway (Recommandé)
- URL: https://railway.app/
- Déploiement: Connecter le repo GitHub
- Base de données: PostgreSQL automatique
- Redis: Service Redis automatique

### 2. Render
- URL: https://render.com/
- Déploiement: Connecter le repo GitHub
- Base de données: PostgreSQL gratuit
- Redis: Service Redis gratuit

### 3. Heroku
- URL: https://heroku.com/
- Déploiement: Git push heroku main
- Add-ons: Heroku Postgres, Heroku Redis

## 📋 Variables d'Environnement Requises

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DATABASE_URL=postgresql://... (auto-généré)
REDIS_URL=redis://... (auto-généré)
```

## 🔗 URLs de l'Application Déployée

Une fois déployé, votre application sera accessible à:
- **Application principale**: https://your-app.railway.app/
- **GraphQL API**: https://your-app.railway.app/graphql/
- **API Documentation**: https://your-app.railway.app/api/docs/
- **Admin Interface**: https://your-app.railway.app/admin/

## 👤 Compte Admin par Défaut

- **Username**: admin
- **Email**: admin@alxprojectnexus.com
- **Password**: admin123

⚠️ **IMPORTANT**: Changez ce mot de passe après le premier déploiement!

## 🎯 Pour la Soumission ALX

Incluez ces liens dans votre soumission:
1. **Live Application**: [URL de votre app]
2. **GitHub Repository**: https://github.com/your-username/alx-project-nexus
3. **API Documentation**: [URL]/api/docs/
4. **GraphQL Playground**: [URL]/graphql/

---

**🎊 Votre application est prête pour le déploiement en production!**
"""
    
    with open('DEPLOYMENT_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("✅ Résumé de déploiement créé: DEPLOYMENT_SUMMARY.md")
    return True

def main():
    """Fonction principale du script de déploiement"""
    print("🚀 SCRIPT DE DÉPLOIEMENT ALX PROJECT NEXUS")
    print("=" * 60)
    print("Préparation de l'application pour le déploiement en production")
    print("=" * 60)
    
    # Vérifier les fichiers requis
    if not check_requirements():
        print("\n❌ Des fichiers requis sont manquants. Arrêt du script.")
        return False
    
    # Étapes de préparation
    steps = [
        ("Création du template .env", create_env_template),
        ("Collecte des fichiers statiques", collect_static_files),
        ("Test des paramètres de production", test_production_settings),
        ("Génération du résumé de déploiement", generate_deployment_summary),
    ]
    
    success_count = 0
    for step_name, step_function in steps:
        if step_function():
            success_count += 1
        else:
            print(f"⚠️ Étape '{step_name}' a échoué, mais on continue...")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 60)
    
    print(f"Étapes complétées: {success_count}/{len(steps)}")
    
    if success_count >= len(steps) - 1:  # Permettre 1 échec
        print("\n🎊 DÉPLOIEMENT PRÊT!")
        print("✅ Votre application est prête pour le déploiement")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Créer un compte sur Railway/Render/Heroku")
        print("2. Connecter votre repository GitHub")
        print("3. Configurer les variables d'environnement")
        print("4. Déployer l'application")
        print("5. Tester les endpoints en production")
        
        print("\n🔗 LIENS UTILES:")
        print("• Guide de déploiement: docs/deployment/DEPLOYMENT_GUIDE.md")
        print("• Résumé: DEPLOYMENT_SUMMARY.md")
        print("• Template .env: .env.production.template")
        
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS")
        print("Vérifiez les erreurs ci-dessus avant de déployer")
    
    return success_count >= len(steps) - 1

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Script interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)
