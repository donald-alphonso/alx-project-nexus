#!/usr/bin/env python3
"""
Script de Préparation Railway - ALX Project Nexus
Prépare tous les fichiers nécessaires pour le déploiement Railway
"""

import os
import sys
import subprocess
from datetime import datetime

def print_step(step_num, title):
    """Affiche une étape avec formatage"""
    print(f"\n{'='*60}")
    print(f"🚀 ÉTAPE {step_num}: {title}")
    print(f"{'='*60}")

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MANQUANT")
        return False

def create_railway_env_template():
    """Crée un template spécifique pour Railway"""
    print_step(1, "CRÉATION TEMPLATE VARIABLES RAILWAY")
    
    railway_env = """# 🚀 Variables d'Environnement Railway - ALX Project Nexus
# Copie ces variables dans Railway Dashboard > Variables

# ===== DJANGO CORE =====
SECRET_KEY=django-insecure-alx-project-nexus-2025-change-this-in-real-production
DEBUG=False
DJANGO_SETTINGS_MODULE=social_media_backend.settings.production
ALLOWED_HOSTS=*.railway.app

# ===== DATABASE =====
# Cette variable sera automatiquement générée par Railway PostgreSQL
# DATABASE_URL=postgresql://postgres:password@host:port/database

# ===== REDIS =====
# Cette variable sera automatiquement générée par Railway Redis
# REDIS_URL=redis://default:password@host:port

# ===== SECURITY =====
SECURE_SSL_REDIRECT=True
CORS_ALLOWED_ORIGINS=https://*.railway.app

# ===== API DOCUMENTATION =====
# Remplace 'ton-app' par le nom de ton app Railway
API_BASE_URL=https://ton-app.railway.app

# ===== EMAIL (OPTIONNEL) =====
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=ton-email@gmail.com
# EMAIL_HOST_PASSWORD=ton-mot-de-passe-app
# DEFAULT_FROM_EMAIL=noreply@alxprojectnexus.com

# ===== INSTRUCTIONS =====
# 1. Va sur Railway Dashboard
# 2. Clique sur ton service Django
# 3. Onglet "Variables"
# 4. Ajoute chaque variable (sauf DATABASE_URL et REDIS_URL qui sont auto)
# 5. Clique "Deploy" pour redémarrer
"""
    
    with open('.env.railway', 'w', encoding='utf-8') as f:
        f.write(railway_env)
    
    print("✅ Template créé: .env.railway")
    print("📋 Utilise ce fichier pour configurer tes variables sur Railway")
    return True

def verify_deployment_files():
    """Vérifie que tous les fichiers de déploiement sont présents"""
    print_step(2, "VÉRIFICATION FICHIERS DÉPLOIEMENT")
    
    required_files = [
        ('Procfile', 'Configuration des processus Railway'),
        ('requirements-production.txt', 'Dépendances Python'),
        ('runtime.txt', 'Version Python'),
        ('social_media_backend/settings/production.py', 'Paramètres production'),
        ('manage.py', 'Script de gestion Django'),
        ('social_media_backend/wsgi.py', 'Interface WSGI')
    ]
    
    all_present = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_present = False
    
    return all_present

def test_production_settings():
    """Teste les paramètres de production"""
    print_step(3, "TEST PARAMÈTRES PRODUCTION")
    
    # Définir les variables d'environnement pour le test
    os.environ['SECRET_KEY'] = 'test-key-for-validation'
    os.environ['DEBUG'] = 'False'
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'
    os.environ['REDIS_URL'] = 'redis://localhost:6379/0'
    os.environ['ALLOWED_HOSTS'] = '*.railway.app'
    
    try:
        # Test d'import des settings
        result = subprocess.run([
            sys.executable, '-c',
            'import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_backend.settings.production"); import django; django.setup(); print("✅ Settings production OK")'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Paramètres de production valides")
            return True
        else:
            print(f"❌ Erreur dans les paramètres: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def create_railway_checklist():
    """Crée une checklist pour Railway"""
    print_step(4, "CRÉATION CHECKLIST RAILWAY")
    
    checklist = f"""# 📋 Checklist Déploiement Railway - ALX Project Nexus

## ✅ AVANT DE COMMENCER
- [ ] Compte GitHub avec le projet ALX
- [ ] Branche `feature/deployment-production` active
- [ ] Tous les fichiers de déploiement présents
- [ ] 30 minutes de temps libre

## 🚀 ÉTAPES RAILWAY (Dans l'ordre)

### 1. Création du Compte
- [ ] Aller sur https://railway.app/
- [ ] S'inscrire avec GitHub
- [ ] Autoriser l'accès aux repos

### 2. Nouveau Projet
- [ ] "New Project" → "Deploy from GitHub repo"
- [ ] Sélectionner `alx-project-nexus`
- [ ] Branche: `feature/deployment-production`
- [ ] Cliquer "Deploy Now"

### 3. Ajouter PostgreSQL
- [ ] "New Service" → "Database" → "PostgreSQL"
- [ ] Copier `DATABASE_URL` depuis Variables

### 4. Ajouter Redis
- [ ] "New Service" → "Database" → "Redis"
- [ ] Copier `REDIS_URL` depuis Variables

### 5. Variables d'Environnement
- [ ] Service Django → Onglet "Variables"
- [ ] Ajouter toutes les variables du fichier `.env.railway`
- [ ] ⚠️ NE PAS ajouter DATABASE_URL et REDIS_URL (auto-générées)

### 6. Redéploiement
- [ ] Attendre le déploiement automatique
- [ ] Vérifier les logs (onglet "Logs")
- [ ] Pas d'erreurs critiques

### 7. Migrations
- [ ] Console → `python manage.py migrate --settings=social_media_backend.settings.production`
- [ ] Console → `python manage.py collectstatic --noinput --settings=social_media_backend.settings.production`

### 8. Superuser
- [ ] Console → `python manage.py shell --settings=social_media_backend.settings.production`
- [ ] Créer admin avec le script fourni

### 9. Tests Finaux
- [ ] https://ton-app.railway.app/ → Page d'accueil
- [ ] https://ton-app.railway.app/admin/ → Login admin/admin123
- [ ] https://ton-app.railway.app/graphql/ → Interface GraphQL
- [ ] https://ton-app.railway.app/api/docs/ → Documentation Swagger

## 🎯 URLS POUR ALX
```
Application: https://ton-app.railway.app/
GraphQL: https://ton-app.railway.app/graphql/
API Docs: https://ton-app.railway.app/api/docs/
Admin: https://ton-app.railway.app/admin/
GitHub: https://github.com/ton-username/alx-project-nexus
```

## 🆘 EN CAS DE PROBLÈME
1. Vérifier les logs Railway
2. Vérifier les variables d'environnement
3. Redémarrer le service
4. Consulter le guide complet: docs/deployment/RAILWAY_GUIDE_COMPLET.md

---
**Créé le {datetime.now().strftime('%d/%m/%Y à %H:%M')}**
**🚀 Bon déploiement !**
"""
    
    with open('RAILWAY_CHECKLIST.md', 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print("✅ Checklist créée: RAILWAY_CHECKLIST.md")
    return True

def create_superuser_script():
    """Crée un script pour créer le superuser"""
    print_step(5, "CRÉATION SCRIPT SUPERUSER")
    
    superuser_script = """# Script pour créer un superuser sur Railway
# À exécuter dans la console Railway

python manage.py shell --settings=social_media_backend.settings.production

# Puis dans le shell Python :
from django.contrib.auth import get_user_model
User = get_user_model()

# Créer le superuser
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

# Sortir du shell
exit()
"""
    
    with open('create_superuser_railway.txt', 'w', encoding='utf-8') as f:
        f.write(superuser_script)
    
    print("✅ Script superuser créé: create_superuser_railway.txt")
    return True

def generate_summary():
    """Génère un résumé de préparation"""
    print_step(6, "RÉSUMÉ DE PRÉPARATION")
    
    print("📊 FICHIERS CRÉÉS POUR RAILWAY:")
    print("   • .env.railway - Template des variables d'environnement")
    print("   • RAILWAY_CHECKLIST.md - Checklist étape par étape")
    print("   • create_superuser_railway.txt - Script pour admin")
    
    print("\n📋 FICHIERS EXISTANTS VÉRIFIÉS:")
    print("   • Procfile - Configuration des processus")
    print("   • requirements-production.txt - Dépendances")
    print("   • runtime.txt - Version Python")
    print("   • settings/production.py - Configuration production")
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("   1. Ouvre RAILWAY_CHECKLIST.md")
    print("   2. Suis les étapes une par une")
    print("   3. Utilise .env.railway pour les variables")
    print("   4. Teste ton application déployée")
    
    print("\n🔗 LIENS UTILES:")
    print("   • Railway: https://railway.app/")
    print("   • Guide complet: docs/deployment/RAILWAY_GUIDE_COMPLET.md")
    print("   • Checklist: RAILWAY_CHECKLIST.md")

def main():
    """Fonction principale"""
    print("🚀 PRÉPARATION RAILWAY - ALX PROJECT NEXUS")
    print(f"Heure: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # Vérifier qu'on est sur la bonne branche
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        current_branch = result.stdout.strip()
        
        if current_branch != 'feature/deployment-production':
            print(f"⚠️ Tu es sur la branche '{current_branch}'")
            print("🔄 Recommandation: git checkout feature/deployment-production")
        else:
            print(f"✅ Branche correcte: {current_branch}")
    except:
        print("ℹ️ Impossible de vérifier la branche Git")
    
    # Étapes de préparation
    steps = [
        create_railway_env_template,
        verify_deployment_files,
        test_production_settings,
        create_railway_checklist,
        create_superuser_script,
        generate_summary
    ]
    
    success_count = 0
    for step_func in steps:
        try:
            if step_func():
                success_count += 1
        except Exception as e:
            print(f"❌ Erreur dans l'étape: {e}")
    
    # Résumé final
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ FINAL")
    print(f"{'='*60}")
    
    print(f"Étapes complétées: {success_count}/{len(steps)}")
    
    if success_count == len(steps):
        print("\n🎊 PRÉPARATION RAILWAY TERMINÉE !")
        print("✅ Tous les fichiers sont prêts")
        print("📋 Suis maintenant RAILWAY_CHECKLIST.md")
        print("🚀 Temps estimé de déploiement: 30-45 minutes")
    else:
        print("\n⚠️ Quelques problèmes détectés")
        print("🔧 Vérifie les erreurs ci-dessus")
    
    return success_count == len(steps)

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Préparation interrompue")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur: {e}")
        sys.exit(1)
