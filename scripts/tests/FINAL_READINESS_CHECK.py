#!/usr/bin/env python3
"""
🎯 FINAL READINESS CHECK - ALX PROJECT NEXUS
Vérification finale avant présentation ALX

Ce script vérifie que tous les éléments sont prêts pour la présentation.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header(title):
    """Affiche un en-tête formaté"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Affiche une section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: MANQUANT - {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Vérifie qu'un répertoire existe"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: MANQUANT - {dirpath}")
        return False

def check_file_content(filepath, required_content, description):
    """Vérifie le contenu d'un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if required_content in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description}: Contenu manquant")
                return False
    except Exception as e:
        print(f"❌ {description}: Erreur lecture - {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print_header("VÉRIFICATION FINALE - ALX PROJECT NEXUS")
    
    total_checks = 0
    passed_checks = 0
    
    # 1. VÉRIFICATION STRUCTURE PROJET
    print_section("STRUCTURE DU PROJET")
    
    project_files = [
        ("README.md", "Documentation principale"),
        ("docker-compose.yml", "Configuration Docker"),
        ("Dockerfile", "Image Docker"),
        ("pyproject.toml", "Dépendances Python"),
        ("railway.json", "Configuration Railway"),
        (".env.docker", "Variables d'environnement"),
        ("manage.py", "Script Django"),
    ]
    
    for filepath, description in project_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            passed_checks += 1
    
    # 2. VÉRIFICATION APPS DJANGO
    print_section("APPLICATIONS DJANGO")
    
    django_apps = [
        ("users/", "App utilisateurs"),
        ("posts/", "App publications"),
        ("interactions/", "App interactions"),
        ("social_media_backend/", "Configuration principale"),
    ]
    
    for dirpath, description in django_apps:
        total_checks += 1
        if check_directory_exists(dirpath, description):
            passed_checks += 1
    
    # 3. VÉRIFICATION SCHÉMAS GRAPHQL
    print_section("SCHÉMAS GRAPHQL")
    
    schema_files = [
        ("users/schema.py", "Schéma utilisateurs"),
        ("posts/schema.py", "Schéma publications"),
        ("interactions/schema.py", "Schéma interactions"),
        ("social_media_backend/schema.py", "Schéma principal"),
    ]
    
    for filepath, description in schema_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            passed_checks += 1
    
    # 4. VÉRIFICATION MODÈLES
    print_section("MODÈLES DE BASE DE DONNÉES")
    
    model_files = [
        ("users/models.py", "Modèles utilisateurs"),
        ("posts/models.py", "Modèles publications"),
        ("interactions/models.py", "Modèles interactions"),
    ]
    
    for filepath, description in model_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            passed_checks += 1
    
    # 5. VÉRIFICATION SCRIPTS DE TEST
    print_section("SCRIPTS DE TEST")
    
    test_files = [
        ("FUNCTIONALITY_AUDIT.py", "Audit fonctionnalités"),
        ("VALIDATE_PROJECT.py", "Validation projet"),
        ("COMPLETE_FUNCTIONALITY_TEST.py", "Tests complets"),
        ("SIMPLE_TEST.py", "Tests simples"),
    ]
    
    for filepath, description in test_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            passed_checks += 1
    
    # 6. VÉRIFICATION DOCUMENTATION
    print_section("DOCUMENTATION")
    
    doc_files = [
        ("FINAL_TEST_GUIDE.md", "Guide de test final"),
        ("PROJECT_FINAL_SUMMARY.md", "Résumé du projet"),
        ("ERD_SPECIFICATION.md", "Spécification ERD"),
        ("DATABASE_SCHEMA.sql", "Schéma base de données"),
        ("LUCIDCHART_GUIDE.md", "Guide Lucidchart"),
    ]
    
    for filepath, description in doc_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            passed_checks += 1
    
    # 7. VÉRIFICATION GUIDES PRÉSENTATION
    print_section("GUIDES DE PRÉSENTATION")
    
    presentation_files = [
        ("NEXT_STEPS_ALX.md", "Prochaines étapes ALX"),
        ("GOOGLE_DOC_TEMPLATE.md", "Template Google Doc"),
        ("RAILWAY_DEPLOYMENT_GUIDE.md", "Guide déploiement Railway"),
        ("PRESENTATION_TEMPLATE.md", "Template présentation"),
    ]
    
    for filepath, description in presentation_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            passed_checks += 1
    
    # 8. VÉRIFICATION CONTENU CRITIQUE
    print_section("CONTENU CRITIQUE")
    
    # Vérifier que le schéma principal inclut toutes les apps
    total_checks += 1
    if check_file_content(
        "social_media_backend/schema.py",
        "UserQuery, PostQuery, InteractionQuery",
        "Schéma principal avec toutes les queries"
    ):
        passed_checks += 1
    
    # Vérifier que les mutations Report sont présentes
    total_checks += 1
    if check_file_content(
        "interactions/schema.py",
        "CreateReport",
        "Mutations Report implémentées"
    ):
        passed_checks += 1
    
    # Vérifier la configuration Docker
    total_checks += 1
    if check_file_content(
        "docker-compose.yml",
        "postgresql",
        "Configuration PostgreSQL"
    ):
        passed_checks += 1
    
    # 9. VÉRIFICATION CONFIGURATION RAILWAY
    print_section("CONFIGURATION DÉPLOIEMENT")
    
    total_checks += 1
    if os.path.exists("railway.json"):
        try:
            with open("railway.json", 'r') as f:
                config = json.load(f)
                if "deploy" in config and "startCommand" in config["deploy"]:
                    print("✅ Configuration Railway valide")
                    passed_checks += 1
                else:
                    print("❌ Configuration Railway incomplète")
        except:
            print("❌ Configuration Railway invalide")
    else:
        print("❌ Fichier railway.json manquant")
    
    # 10. RÉSUMÉ FINAL
    print_section("RÉSUMÉ FINAL")
    
    percentage = (passed_checks / total_checks) * 100
    
    print(f"📊 SCORE DE PRÉPARATION: {passed_checks}/{total_checks} ({percentage:.1f}%)")
    
    if percentage >= 95:
        print("🎊 EXCELLENT! Votre projet est parfaitement prêt pour la présentation ALX!")
        print("✅ Tous les éléments critiques sont en place")
    elif percentage >= 85:
        print("🎯 TRÈS BIEN! Votre projet est presque prêt")
        print("⚠️ Quelques éléments mineurs à finaliser")
    elif percentage >= 75:
        print("⚠️ ATTENTION! Plusieurs éléments manquent")
        print("🔧 Travail nécessaire avant la présentation")
    else:
        print("❌ CRITIQUE! Beaucoup d'éléments manquent")
        print("🚨 Préparation urgente requise")
    
    # 11. PROCHAINES ÉTAPES
    print_section("PROCHAINES ÉTAPES RECOMMANDÉES")
    
    if percentage >= 95:
        print("1. 📊 Créer l'ERD avec Lucidchart")
        print("2. 🚀 Déployer sur Railway")
        print("3. 🎤 Préparer les slides de présentation")
        print("4. 🎥 Enregistrer la vidéo démo")
        print("5. 📝 Finaliser le Google Doc")
    else:
        print("1. 🔧 Corriger les éléments manquants ci-dessus")
        print("2. 🧪 Relancer ce script de vérification")
        print("3. 📊 Créer l'ERD une fois tout corrigé")
        print("4. 🚀 Procéder au déploiement")
    
    print_section("LIENS UTILES")
    print("📊 ERD: https://lucid.app/ ou https://app.diagrams.net/")
    print("🚀 Déploiement: https://railway.app/")
    print("🎤 Slides: https://slides.google.com/")
    print("🎥 Vidéo: https://www.loom.com/ ou OBS Studio")
    
    print(f"\n{'='*60}")
    print("🎯 BONNE CHANCE POUR VOTRE PRÉSENTATION ALX! 🚀")
    print(f"{'='*60}\n")
    
    return percentage >= 85

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
