#!/usr/bin/env python3
"""
Script pour corriger l'erreur "Error decoding signature" JWT
"""

import os
import secrets
from pathlib import Path

def corriger_secret_key():
    """Corriger la SECRET_KEY Django pour JWT"""
    
    print("🔧 CORRECTION ERREUR JWT SIGNATURE")
    print("=" * 40)
    
    # 1. Générer une nouvelle SECRET_KEY sécurisée
    nouvelle_secret_key = secrets.token_urlsafe(50)
    print(f"✅ Nouvelle SECRET_KEY générée : {nouvelle_secret_key[:20]}...")
    
    # 2. Corriger settings.py avec une SECRET_KEY fixe
    settings_path = Path('social_media_backend/settings.py')
    
    if not settings_path.exists():
        print("❌ Fichier settings.py non trouvé")
        return False
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer la ligne SECRET_KEY
    old_secret_line = "SECRET_KEY = config('SECRET_KEY', default='django-insecure-gk+s44id-d2-q*fs5x(5whp(j2rv0f0!*msdpwh#1*7h$xd27%')"
    new_secret_line = f"SECRET_KEY = '{nouvelle_secret_key}'"
    
    if old_secret_line in content:
        content = content.replace(old_secret_line, new_secret_line)
        print("✅ SECRET_KEY mise à jour dans settings.py")
    else:
        # Chercher une ligne SECRET_KEY existante
        import re
        secret_pattern = r"SECRET_KEY = .*"
        if re.search(secret_pattern, content):
            content = re.sub(secret_pattern, new_secret_line, content)
            print("✅ SECRET_KEY existante remplacée")
        else:
            print("⚠️ Ligne SECRET_KEY non trouvée")
    
    # 3. Simplifier la configuration JWT
    jwt_config_old = """# GraphQL JWT Configuration
GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=60),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}"""
    
    jwt_config_new = """# GraphQL JWT Configuration
GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=60),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_ALGORITHM': 'HS256',
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALLOW_ANY_CLASSES': [
        'graphql_jwt.mutations.ObtainJSONWebToken',
        'graphql_jwt.mutations.Refresh',
        'graphql_jwt.mutations.Verify',
    ],
}"""
    
    if jwt_config_old in content:
        content = content.replace(jwt_config_old, jwt_config_new)
        print("✅ Configuration JWT mise à jour")
    
    # Sauvegarder
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fichier settings.py sauvegardé")
    return True

def tester_correction():
    """Tester si la correction fonctionne"""
    
    print("\n🧪 TEST DE LA CORRECTION")
    print("=" * 30)
    
    import subprocess
    import time
    import requests
    
    # Redémarrer le conteneur web
    print("🔄 Redémarrage du conteneur web...")
    try:
        subprocess.run(['docker-compose', 'restart', 'web'], cwd='.', check=True)
        print("✅ Conteneur redémarré")
        
        # Attendre le démarrage
        print("⏳ Attente démarrage (15 secondes)...")
        time.sleep(15)
        
        # Test simple
        print("🧪 Test de l'API...")
        
        base_url = "http://localhost:8000/graphql/"
        
        # Test de santé
        health_query = {
            "query": "query { health }"
        }
        
        response = requests.post(base_url, json=health_query, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if 'errors' not in result:
                print("✅ API GraphQL fonctionne")
                
                # Test création utilisateur
                print("🧪 Test création utilisateur...")
                
                create_user = {
                    "query": """
                    mutation {
                        createUser(
                            username: "testfix2025"
                            email: "testfix2025@example.com"
                            password: "motdepasse123"
                            firstName: "Test"
                            lastName: "Fix"
                        ) {
                            user {
                                id
                                username
                            }
                            success
                            errors
                        }
                    }
                    """
                }
                
                response = requests.post(base_url, json=create_user, timeout=10)
                result = response.json()
                
                if 'errors' in result:
                    print(f"❌ Erreur création utilisateur : {result['errors']}")
                    return False
                else:
                    user_data = result.get('data', {}).get('createUser', {})
                    if user_data and user_data.get('success'):
                        print("✅ Création utilisateur réussie !")
                        
                        # Test connexion JWT
                        print("🧪 Test connexion JWT...")
                        
                        login_mutation = {
                            "query": """
                            mutation {
                                tokenAuth(email: "testfix2025@example.com", password: "motdepasse123") {
                                    token
                                }
                            }
                            """
                        }
                        
                        response = requests.post(base_url, json=login_mutation, timeout=10)
                        result = response.json()
                        
                        if 'errors' in result:
                            print(f"❌ Erreur JWT : {result['errors']}")
                            return False
                        else:
                            token_data = result.get('data', {}).get('tokenAuth', {})
                            if token_data and token_data.get('token'):
                                print("✅ Token JWT récupéré avec succès !")
                                print(f"🔑 Token : {token_data['token'][:30]}...")
                                return True
                            else:
                                print("❌ Token non récupéré")
                                return False
                    else:
                        print(f"❌ Échec création utilisateur : {user_data.get('errors', [])}")
                        return False
            else:
                print(f"❌ Erreur API : {result['errors']}")
                return False
        else:
            print(f"❌ Erreur HTTP : {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test : {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🚀 CORRECTION ERREUR JWT SIGNATURE")
    print("=" * 50)
    
    # Étape 1 : Corriger la configuration
    if not corriger_secret_key():
        print("❌ Impossible de corriger la configuration")
        return
    
    # Étape 2 : Tester la correction
    if tester_correction():
        print("\n🎊 SUCCÈS TOTAL !")
        print("✅ Erreur JWT signature corrigée")
        print("✅ Authentification fonctionnelle")
        print("\n📋 Vous pouvez maintenant tester :")
        print("1. http://localhost:8000/graphql/")
        print("2. Créer des utilisateurs sans erreur")
        print("3. Se connecter et récupérer des tokens JWT")
        print("\n🌟 Votre projet ALX est parfait !")
    else:
        print("\n⚠️ Correction partielle")
        print("✅ Configuration mise à jour")
        print("⚠️ Tests à refaire manuellement")
        print("\n📋 Essayez de nouveau :")
        print("1. http://localhost:8000/graphql/")
        print("2. Créer un utilisateur")

if __name__ == "__main__":
    main()
