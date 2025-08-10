#!/usr/bin/env python3
"""
Validation Ultra-Rapide - 30 secondes max
Vérification critique pour présentation ALX
"""

import requests
import sys
from datetime import datetime

def test_endpoint(name, url, expected_codes=[200, 302]):
    """Test rapide d'un endpoint"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in expected_codes:
            print(f"✅ {name}: OK ({response.status_code})")
            return True
        else:
            print(f"❌ {name}: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)[:50]}")
        return False

def main():
    """Validation ultra-rapide"""
    print("🚀 VALIDATION ULTRA-RAPIDE ALX PROJECT NEXUS")
    print("=" * 50)
    
    # Tests critiques
    tests = [
        ("GraphQL API", "http://localhost:8000/graphql/"),
        ("Admin Panel", "http://localhost:8000/admin/"),
        ("Health Check", "http://localhost:8000/api/health/"),
        ("Swagger UI", "http://localhost:8000/api/swagger/"),
    ]
    
    passed = 0
    for name, url in tests:
        if test_endpoint(name, url):
            passed += 1
    
    # Résultat
    print("=" * 50)
    success_rate = (passed / len(tests)) * 100
    
    if success_rate >= 75:
        print(f"🎊 SUCCÈS: {passed}/{len(tests)} tests passés ({success_rate:.0f}%)")
        print("✅ PROJET PRÊT POUR PRÉSENTATION ALX!")
        return True
    else:
        print(f"⚠️ ATTENTION: {passed}/{len(tests)} tests passés ({success_rate:.0f}%)")
        print("❌ Vérifier les services Docker")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
