#!/usr/bin/env python3
"""
Script de validation améliorée pour ALX Project Nexus
Teste toutes les fonctionnalités avec gestion d'erreurs améliorée
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
GRAPHQL_URL = f"{BASE_URL}/graphql/"
HEALTH_URL = f"{BASE_URL}/api/health/"

def log_test(message, status="INFO"):
    """Log des tests avec timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {status}: {message}")

def test_health_check():
    """Test du health check"""
    log_test("🏥 Test Health Check")
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            log_test(f"✅ Health Check: {data['status']}")
            log_test(f"   Database: {data['services']['database']}")
            log_test(f"   Cache: {data['services']['cache']}")
            return True
        else:
            log_test(f"❌ Health Check failed: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log_test(f"❌ Health Check error: {e}", "ERROR")
        return False

def test_graphql_endpoint():
    """Test de l'endpoint GraphQL"""
    log_test("🎯 Test GraphQL Endpoint")
    
    # Test query simple
    query = """
    query {
        allUsers {
            id
            username
            email
        }
    }
    """
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" not in data:
                log_test("✅ GraphQL endpoint accessible")
                return True
            else:
                log_test(f"⚠️ GraphQL errors: {data['errors']}")
                return False
        else:
            log_test(f"❌ GraphQL failed: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log_test(f"❌ GraphQL error: {e}", "ERROR")
        return False

def test_user_creation():
    """Test de création d'utilisateur avec gestion d'erreurs améliorée"""
    log_test("👤 Test Création Utilisateur")
    
    # Générer un nom d'utilisateur unique
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"test_{timestamp}@example.com"
    
    mutation = f"""
    mutation {{
        createUser(
            username: "{username}",
            email: "{email}",
            password: "testpassword123"
        ) {{
            success
            errors
            user {{
                id
                username
                email
            }}
        }}
    }}
    """
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" not in data:
                result = data["data"]["createUser"]
                if result["success"]:
                    log_test(f"✅ Utilisateur créé: {result['user']['username']}")
                    return True
                else:
                    log_test(f"⚠️ Création échouée: {result['errors']}")
                    return False
            else:
                log_test(f"❌ Erreurs GraphQL: {data['errors']}", "ERROR")
                return False
        else:
            log_test(f"❌ Création utilisateur failed: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log_test(f"❌ Erreur création utilisateur: {e}", "ERROR")
        return False

def test_authentication():
    """Test d'authentification"""
    log_test("🔐 Test Authentification")
    
    # Test d'accès à une mutation protégée sans token
    mutation = """
    mutation {
        createPost(
            content: "Test post",
            visibility: "public"
        ) {
            success
            errors
        }
    }
    """
    
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                error_msg = data["errors"][0]["message"]
                if "Authentication required" in error_msg:
                    log_test("✅ Protection authentification active")
                    return True
                else:
                    log_test(f"⚠️ Message d'erreur inattendu: {error_msg}")
                    return False
            else:
                log_test("❌ Mutation protégée accessible sans auth", "ERROR")
                return False
        else:
            log_test(f"❌ Test auth failed: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log_test(f"❌ Erreur test auth: {e}", "ERROR")
        return False

def test_swagger_documentation():
    """Test de la documentation Swagger"""
    log_test("📚 Test Documentation Swagger")
    
    endpoints_to_test = [
        "/api/docs/",
        "/api/swagger/",
        "/api/error-handling/"
    ]
    
    success_count = 0
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                log_test(f"✅ {endpoint} accessible")
                success_count += 1
            else:
                log_test(f"❌ {endpoint} failed: {response.status_code}", "ERROR")
        except Exception as e:
            log_test(f"❌ {endpoint} error: {e}", "ERROR")
    
    return success_count == len(endpoints_to_test)

def main():
    """Fonction principale de validation"""
    log_test("🚀 DÉMARRAGE VALIDATION AMÉLIORÉE ALX PROJECT NEXUS")
    log_test("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("GraphQL Endpoint", test_graphql_endpoint),
        ("Création Utilisateur", test_user_creation),
        ("Authentification", test_authentication),
        ("Documentation Swagger", test_swagger_documentation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        log_test(f"\n🧪 Test: {test_name}")
        log_test("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                log_test(f"✅ {test_name}: SUCCÈS")
            else:
                log_test(f"❌ {test_name}: ÉCHEC")
                
        except Exception as e:
            log_test(f"❌ {test_name}: ERREUR - {e}", "ERROR")
            results.append((test_name, False))
    
    # Résumé final
    log_test("\n" + "=" * 60)
    log_test("📊 RÉSUMÉ FINAL")
    log_test("=" * 60)
    
    success_count = sum(1 for _, result in results if result)
    total_tests = len(results)
    success_rate = (success_count / total_tests) * 100
    
    for test_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        log_test(f"{test_name}: {status}")
    
    log_test(f"\n🎯 TAUX DE RÉUSSITE: {success_rate:.1f}% ({success_count}/{total_tests})")
    
    if success_rate >= 80:
        log_test("🎊 VALIDATION RÉUSSIE - PROJET PRÊT POUR ALX !")
    elif success_rate >= 60:
        log_test("⚠️ VALIDATION PARTIELLE - Quelques corrections nécessaires")
    else:
        log_test("❌ VALIDATION ÉCHOUÉE - Corrections importantes requises")
    
    log_test("=" * 60)
    log_test(f"⏰ Validation terminée: {datetime.now().strftime('%H:%M:%S')}")
    
    return success_rate >= 80

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
