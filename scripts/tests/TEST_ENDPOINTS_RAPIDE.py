#!/usr/bin/env python3
"""
Test rapide de tous les endpoints - URGENCE ALX
"""

import requests
import time

def test_endpoint(nom, url):
    """Tester un endpoint rapidement"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in [200, 302]:
            print(f"✅ {nom} - OK ({response.status_code})")
            return True
        else:
            print(f"⚠️ {nom} - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {nom} - Erreur: {str(e)[:50]}")
        return False

def main():
    print("🚀 TEST RAPIDE ENDPOINTS - ALX PROJECT NEXUS")
    print("=" * 60)
    
    endpoints = [
        ("🎯 GraphQL", "http://localhost:8000/graphql/"),
        ("🔧 Admin", "http://localhost:8000/admin/"),
        ("📚 Swagger", "http://localhost:8000/api/docs/"),
        ("📖 ReDoc", "http://localhost:8000/api/redoc/"),
        ("🏠 API Home", "http://localhost:8000/"),
        ("📊 Stats", "http://localhost:8000/api/stats/"),
        ("💚 Health", "http://localhost:8000/api/health/"),
        ("🔍 Search", "http://localhost:8000/api/search/?q=test"),
    ]
    
    resultats = []
    for nom, url in endpoints:
        resultat = test_endpoint(nom, url)
        resultats.append((nom, resultat))
    
    print("\n📊 RÉSUMÉ :")
    ok_count = sum(1 for _, ok in resultats if ok)
    total = len(resultats)
    
    print(f"✅ {ok_count}/{total} endpoints fonctionnels")
    
    if ok_count >= 6:  # Au moins GraphQL + Admin + 4 autres
        print("🎊 PROJET PRÊT POUR PRÉSENTATION ALX !")
    else:
        print("⚠️ Quelques ajustements nécessaires")
    
    return ok_count >= 6

if __name__ == "__main__":
    main()
