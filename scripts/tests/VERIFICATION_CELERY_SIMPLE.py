#!/usr/bin/env python3
"""
Vérification Simple des Tâches Celery
Sans dépendance à django_celery_beat
"""

import os
import sys
from datetime import datetime

def check_task_files():
    """Vérifier que les fichiers de tâches existent"""
    print("📁 VÉRIFICATION DES FICHIERS DE TÂCHES")
    print("=" * 50)
    
    task_files = [
        'users/tasks.py',
        'posts/tasks.py'
    ]
    
    files_ok = 0
    for file_path in task_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
            files_ok += 1
            
            # Vérifier le contenu
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '@shared_task' in content:
                    print(f"   📝 Contient des tâches Celery")
                else:
                    print(f"   ⚠️ Pas de tâches Celery détectées")
        else:
            print(f"❌ {file_path} - MANQUANT")
    
    print(f"\n📊 Fichiers: {files_ok}/{len(task_files)} OK")
    return files_ok == len(task_files)

def check_celery_config():
    """Vérifier la configuration Celery"""
    print("\n⚙️ VÉRIFICATION CONFIGURATION CELERY")
    print("=" * 50)
    
    config_files = [
        'social_media_backend/celery.py',
        'social_media_backend/celery_schedule.py'
    ]
    
    config_ok = 0
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
            config_ok += 1
        else:
            print(f"❌ {file_path} - MANQUANT")
    
    # Vérifier settings.py
    settings_path = 'social_media_backend/settings.py'
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'CELERY_BROKER_URL' in content:
                print(f"✅ {settings_path} - Configuration Celery présente")
                config_ok += 1
            else:
                print(f"⚠️ {settings_path} - Configuration Celery manquante")
    
    print(f"\n📊 Configuration: {config_ok}/{len(config_files) + 1} OK")
    return config_ok >= 2

def analyze_tasks():
    """Analyser les tâches définies"""
    print("\n🔍 ANALYSE DES TÂCHES DÉFINIES")
    print("=" * 50)
    
    tasks_found = []
    
    # Analyser users/tasks.py
    if os.path.exists('users/tasks.py'):
        with open('users/tasks.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Chercher les fonctions avec @shared_task
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '@shared_task' in line:
                    # Chercher la fonction suivante
                    for j in range(i+1, min(i+5, len(lines))):
                        if 'def ' in lines[j]:
                            func_name = lines[j].split('def ')[1].split('(')[0]
                            tasks_found.append(f"users.tasks.{func_name}")
                            break
    
    # Analyser posts/tasks.py
    if os.path.exists('posts/tasks.py'):
        with open('posts/tasks.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '@shared_task' in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        if 'def ' in lines[j]:
                            func_name = lines[j].split('def ')[1].split('(')[0]
                            tasks_found.append(f"posts.tasks.{func_name}")
                            break
    
    print(f"📋 Tâches trouvées: {len(tasks_found)}")
    for task in tasks_found:
        print(f"   ✅ {task}")
    
    return tasks_found

def check_documentation():
    """Vérifier la documentation"""
    print("\n📚 VÉRIFICATION DOCUMENTATION")
    print("=" * 50)
    
    docs = [
        'docs/guides/CELERY_GUIDE.md',
        'docs/guides/ADMIN_DASHBOARD_GUIDE.md',
        'README.md'
    ]
    
    docs_ok = 0
    for doc_path in docs:
        if os.path.exists(doc_path):
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Celery' in content or 'celery' in content:
                    print(f"✅ {doc_path} - Contient documentation Celery")
                    docs_ok += 1
                else:
                    print(f"⚠️ {doc_path} - Pas de mention Celery")
        else:
            print(f"❌ {doc_path} - MANQUANT")
    
    print(f"\n📊 Documentation: {docs_ok}/{len(docs)} OK")
    return docs_ok >= 2

def check_docker_config():
    """Vérifier la configuration Docker"""
    print("\n🐳 VÉRIFICATION DOCKER")
    print("=" * 50)
    
    docker_ok = 0
    
    # Vérifier docker-compose.yml
    if os.path.exists('docker-compose.yml'):
        with open('docker-compose.yml', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'celery:' in content and 'celery-beat:' in content:
                print("✅ docker-compose.yml - Services Celery configurés")
                docker_ok += 1
            else:
                print("⚠️ docker-compose.yml - Services Celery manquants")
    
    # Vérifier pyproject.toml
    if os.path.exists('pyproject.toml'):
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'celery' in content and 'django-celery-beat' in content:
                print("✅ pyproject.toml - Dépendances Celery présentes")
                docker_ok += 1
            else:
                print("⚠️ pyproject.toml - Dépendances Celery manquantes")
    
    print(f"\n📊 Docker: {docker_ok}/2 OK")
    return docker_ok == 2

def main():
    """Vérification principale"""
    print("🔧 VÉRIFICATION CELERY SIMPLIFIÉE - ALX PROJECT NEXUS")
    print("=" * 70)
    print(f"Heure: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    # Tests
    files_ok = check_task_files()
    config_ok = check_celery_config()
    tasks = analyze_tasks()
    docs_ok = check_documentation()
    docker_ok = check_docker_config()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 70)
    
    tests = [
        ("Fichiers de tâches", files_ok),
        ("Configuration", config_ok),
        ("Documentation", docs_ok),
        ("Docker", docker_ok)
    ]
    
    passed = sum(1 for _, ok in tests if ok)
    total = len(tests)
    
    for test_name, ok in tests:
        status = "✅ OK" if ok else "❌ PROBLÈME"
        print(f"{test_name:20} {status}")
    
    print(f"\nTâches trouvées: {len(tasks)}")
    print(f"Tests réussis: {passed}/{total}")
    
    success_rate = (passed / total) * 100
    
    if success_rate == 100 and len(tasks) >= 8:
        print("🎊 EXCELLENT - Celery parfaitement configuré!")
        status = "EXCELLENT"
    elif success_rate >= 75 and len(tasks) >= 6:
        print("✅ TRÈS BIEN - Celery bien configuré")
        status = "TRÈS BIEN"
    elif success_rate >= 50:
        print("⚠️ ACCEPTABLE - Configuration partielle")
        status = "ACCEPTABLE"
    else:
        print("❌ PROBLÈMES - Configuration incomplète")
        status = "PROBLÈMES"
    
    print(f"\nStatut final: {status}")
    print(f"Prêt pour ALX: {'OUI' if success_rate >= 75 and len(tasks) >= 6 else 'NON'}")
    
    # Recommandations
    if success_rate < 100 or len(tasks) < 8:
        print("\n💡 RECOMMANDATIONS:")
        if not files_ok:
            print("- Vérifier les fichiers users/tasks.py et posts/tasks.py")
        if not config_ok:
            print("- Vérifier la configuration Celery dans settings.py")
        if not docs_ok:
            print("- Compléter la documentation Celery")
        if not docker_ok:
            print("- Reconstruire les containers Docker")
        if len(tasks) < 8:
            print(f"- Ajouter plus de tâches (actuellement {len(tasks)}, recommandé: 8+)")
    
    return success_rate >= 75 and len(tasks) >= 6

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Erreur: {e}")
        sys.exit(1)
