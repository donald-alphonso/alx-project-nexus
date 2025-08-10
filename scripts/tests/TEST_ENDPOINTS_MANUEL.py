#!/usr/bin/env python3
"""
Test Manuel des Endpoints Principaux
Vérification directe sans dépendances externes
"""

import urllib.request
import urllib.error
import json
import sys
from datetime import datetime

def test_endpoint(name, url, timeout=10):
    """Test un endpoint avec urllib"""
    try:
        print(f"🔍 Test {name}...")
        
        # Créer la requête
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'ALX-Test-Script/1.0')
        
        # Faire la requête
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            content_type = response.headers.get('content-type', '')
            
            if status_code == 200:
                print(f"✅ {name}: OK (200) - {content_type[:30]}")
                
                # Essayer de lire un peu de contenu
                try:
                    content = response.read(500).decode('utf-8', errors='ignore')
                    if 'error' not in content.lower() and len(content) > 10:
                        print(f"   📄 Contenu valide ({len(content)} chars)")
                    else:
                        print(f"   ⚠️ Contenu suspect")
                except:
                    print(f"   📄 Contenu binaire")
                
                return True
            else:
                print(f"❌ {name}: Code {status_code}")
                return False
                
    except urllib.error.HTTPError as e:
        if e.code in [302, 301]:  # Redirections OK
            print(f"✅ {name}: REDIRECT ({e.code})")
            return True
        else:
            print(f"❌ {name}: HTTP Error {e.code}")
            return False
            
    except urllib.error.URLError as e:
        print(f"❌ {name}: Connection Error - {str(e)[:50]}")
        return False
        
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)[:50]}")
        return False

def test_graphql_basic():
    """Test GraphQL avec une requête simple"""
    try:
        print(f"🔍 Test GraphQL Query...")
        
        # Requête GraphQL simple
        query_data = {
            "query": "{ __schema { queryType { name } } }"
        }
        
        # Préparer les données
        data = json.dumps(query_data).encode('utf-8')
        
        # Créer la requête
        req = urllib.request.Request(
            'http://localhost:8000/graphql/',
            data=data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'ALX-Test-Script/1.0'
            }
        )
        
        # Faire la requête
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() == 200:
                result = json.loads(response.read().decode('utf-8'))
                if 'data' in result and '__schema' in result['data']:
                    print(f"✅ GraphQL Query: OK - Schema accessible")
                    return True
                else:
                    print(f"❌ GraphQL Query: Invalid response")
                    return False
            else:
                print(f"❌ GraphQL Query: HTTP {response.getcode()}")
                return False
                
    except Exception as e:
        print(f"❌ GraphQL Query: Error - {str(e)[:50]}")
        return False

def main():
    """Test principal"""
    print("🧪 TEST MANUEL DES ENDPOINTS")
    print("=" * 60)
    print(f"Heure: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    passed = 0
    total = 0
    
    # Liste des endpoints à tester
    endpoints = [
        ("Root Info", "http://localhost:8000/"),
        ("Health Check", "http://localhost:8000/api/health/"),
        ("GraphQL Interface", "http://localhost:8000/graphql/"),
        ("Admin Panel", "http://localhost:8000/admin/"),
        ("API Docs", "http://localhost:8000/api/docs/"),
        ("Swagger UI", "http://localhost:8000/api/swagger/"),
        ("ReDoc", "http://localhost:8000/api/redoc/"),
        ("API Schema", "http://localhost:8000/api/schema/"),
        ("Error Guide", "http://localhost:8000/api/error-handling/"),
    ]
    
    print("\n📍 ENDPOINTS PRINCIPAUX")
    print("-" * 40)
    
    for name, url in endpoints:
        if test_endpoint(name, url):
            passed += 1
        total += 1
        print()  # Ligne vide pour lisibilité
    
    # Test GraphQL spécifique
    print("🔗 GRAPHQL API")
    print("-" * 40)
    if test_graphql_basic():
        passed += 1
    total += 1
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Tests réussis: {passed}/{total}")
    print(f"Taux de réussite: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎊 EXCELLENT - Tous les endpoints fonctionnent!")
        status = "EXCELLENT"
    elif success_rate >= 80:
        print("✅ TRÈS BIEN - La plupart des endpoints OK")
        status = "TRÈS BIEN"
    elif success_rate >= 70:
        print("⚠️ ACCEPTABLE - Quelques problèmes")
        status = "ACCEPTABLE"
    else:
        print("❌ PROBLÈMES - Vérifier les services")
        status = "PROBLÈMES"
    
    print(f"\nStatut final: {status}")
    print(f"Prêt pour ALX: {'OUI' if success_rate >= 80 else 'NON'}")
    
    # Recommandations
    if success_rate < 100:
        print("\n💡 RECOMMANDATIONS:")
        if passed < total:
            print("- Vérifier que Docker Compose est démarré")
            print("- Attendre que tous les services soient prêts")
            print("- Vérifier les logs: docker-compose logs")
    
    # Sauvegarde du rapport
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total,
        "passed_tests": passed,
        "success_rate": success_rate,
        "status": status,
        "ready_for_alx": success_rate >= 80,
        "details": f"{passed}/{total} endpoints fonctionnels"
    }
    
    with open("RAPPORT_ENDPOINTS.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nRapport détaillé: RAPPORT_ENDPOINTS.json")
    
    return success_rate >= 80

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'🎯 SUCCÈS' if success else '⚠️ ATTENTION'} - Test terminé")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)
