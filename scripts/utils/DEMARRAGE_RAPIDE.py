#!/usr/bin/env python3
"""
DÉMARRAGE RAPIDE - ALX PROJECT NEXUS
Script pour démarrer et tester le projet rapidement
"""

import subprocess
import time
import requests
import json
import sys
from pathlib import Path

class QuickStart:
    """Démarrage rapide du projet"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.base_url = "http://localhost:8000"
        
    def print_header(self, title):
        """Affiche un en-tête formaté"""
        print("\n" + "="*60)
        print(f"🚀 {title}")
        print("="*60)
    
    def print_step(self, step, description):
        """Affiche une étape"""
        print(f"\n📋 Étape {step}: {description}")
        print("-" * 50)
    
    def run_command(self, command, cwd=None, check=True):
        """Exécute une commande"""
        try:
            if cwd is None:
                cwd = self.project_root
            
            print(f"💻 Exécution: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                capture_output=True, 
                text=True,
                check=check
            )
            
            if result.stdout:
                print(f"✅ Sortie: {result.stdout.strip()}")
            
            return result
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur: {e}")
            if e.stderr:
                print(f"   Détail: {e.stderr.strip()}")
            return None
    
    def check_docker(self):
        """Vérifie que Docker est disponible"""
        self.print_step(1, "Vérification de Docker")
        
        result = self.run_command("docker --version", check=False)
        if result is None or result.returncode != 0:
            print("❌ Docker n'est pas installé ou accessible")
            return False
        
        result = self.run_command("docker-compose --version", check=False)
        if result is None or result.returncode != 0:
            print("❌ Docker Compose n'est pas installé ou accessible")
            return False
        
        print("✅ Docker et Docker Compose sont disponibles")
        return True
    
    def start_services(self):
        """Démarre les services Docker"""
        self.print_step(2, "Démarrage des services Docker")
        
        # Arrêter les services existants
        print("🛑 Arrêt des services existants...")
        self.run_command("docker-compose down", check=False)
        
        # Démarrer les services
        print("🚀 Démarrage des services...")
        result = self.run_command("docker-compose up -d")
        
        if result is None:
            print("❌ Échec du démarrage des services")
            return False
        
        print("✅ Services démarrés avec succès")
        return True
    
    def wait_for_services(self):
        """Attend que les services soient prêts"""
        self.print_step(3, "Attente de la disponibilité des services")
        
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(f"{self.base_url}/graphql/", timeout=5)
                if response.status_code == 200:
                    print("✅ Services prêts et accessibles")
                    return True
                    
            except requests.exceptions.RequestException:
                pass
            
            attempt += 1
            print(f"⏳ Tentative {attempt}/{max_attempts} - Attente...")
            time.sleep(2)
        
        print("❌ Services non accessibles après 60 secondes")
        return False
    
    def test_graphql_endpoint(self):
        """Test l'endpoint GraphQL"""
        self.print_step(4, "Test de l'endpoint GraphQL")
        
        # Test d'introspection simple
        query = {
            "query": """
            query {
              __schema {
                queryType { name }
                mutationType { name }
              }
            }
            """
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/graphql/",
                json=query,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and '__schema' in data['data']:
                    print("✅ Endpoint GraphQL fonctionnel")
                    print(f"   Query Type: {data['data']['__schema']['queryType']['name']}")
                    print(f"   Mutation Type: {data['data']['__schema']['mutationType']['name']}")
                    return True
                else:
                    print("❌ Réponse GraphQL invalide")
                    return False
            else:
                print(f"❌ Endpoint GraphQL erreur {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion GraphQL: {e}")
            return False
    
    def test_documentation_endpoints(self):
        """Test les endpoints de documentation"""
        self.print_step(5, "Test des endpoints de documentation")
        
        endpoints = [
            ("/api/docs/", "Documentation API"),
            ("/api/swagger/", "Interface Swagger"),
            ("/api/health/", "Health Check"),
            ("/admin/", "Interface Admin")
        ]
        
        success_count = 0
        
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {description}: Accessible")
                    success_count += 1
                else:
                    print(f"⚠️ {description}: Code {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {description}: Erreur {e}")
        
        print(f"\n📊 Résultat: {success_count}/{len(endpoints)} endpoints accessibles")
        return success_count >= len(endpoints) // 2  # Au moins 50% accessibles
    
    def create_test_user(self):
        """Crée un utilisateur de test"""
        self.print_step(6, "Création d'un utilisateur de test")
        
        mutation = {
            "query": """
            mutation CreateTestUser {
              createUser(
                username: "testuser_quickstart"
                email: "test.quickstart@example.com"
                password: "TestPass123!"
                firstName: "Test"
                lastName: "User"
              ) {
                user {
                  id
                  username
                  email
                }
                success
                errors
              }
            }
            """
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/graphql/",
                json=mutation,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'errors' in data:
                    # Vérifier si c'est une erreur de duplication (acceptable)
                    error_messages = [str(err) for err in data['errors']]
                    if any('already exists' in msg.lower() for msg in error_messages):
                        print("⚠️ Utilisateur existe déjà (normal)")
                        return True
                    else:
                        print(f"❌ Erreurs création utilisateur: {data['errors']}")
                        return False
                
                elif 'data' in data and data['data']['createUser']['success']:
                    user = data['data']['createUser']['user']
                    print(f"✅ Utilisateur créé: {user['username']} ({user['email']})")
                    return True
                
                else:
                    print("❌ Création utilisateur échouée")
                    return False
            
            else:
                print(f"❌ Erreur HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur création utilisateur: {e}")
            return False
    
    def display_access_info(self):
        """Affiche les informations d'accès"""
        self.print_step(7, "Informations d'accès")
        
        print("🌐 ENDPOINTS DISPONIBLES:")
        print(f"   • GraphQL API: {self.base_url}/graphql/")
        print(f"   • Documentation: {self.base_url}/api/docs/")
        print(f"   • Swagger UI: {self.base_url}/api/swagger/")
        print(f"   • Interface Admin: {self.base_url}/admin/")
        print(f"   • Health Check: {self.base_url}/api/health/")
        
        print("\n🔑 AUTHENTIFICATION:")
        print("   • Email: test.quickstart@example.com")
        print("   • Mot de passe: TestPass123!")
        
        print("\n📚 DOCUMENTATION:")
        print("   • Guides: docs/guides/")
        print("   • API: docs/api/")
        print("   • Tests: scripts/tests/")
    
    def run_quick_start(self):
        """Lance le démarrage rapide complet"""
        
        self.print_header("DÉMARRAGE RAPIDE ALX PROJECT NEXUS")
        
        print("🎯 Ce script va :")
        print("   1. Vérifier Docker")
        print("   2. Démarrer les services")
        print("   3. Attendre la disponibilité")
        print("   4. Tester GraphQL")
        print("   5. Tester la documentation")
        print("   6. Créer un utilisateur de test")
        print("   7. Afficher les informations d'accès")
        
        input("\n⏸️ Appuyez sur Entrée pour continuer...")
        
        # Étapes du démarrage
        steps = [
            self.check_docker,
            self.start_services,
            self.wait_for_services,
            self.test_graphql_endpoint,
            self.test_documentation_endpoints,
            self.create_test_user
        ]
        
        success_count = 0
        
        for step in steps:
            if step():
                success_count += 1
            else:
                print(f"\n⚠️ Étape échouée, mais continuation...")
        
        # Affichage final
        self.display_access_info()
        
        # Résultat final
        self.print_header("RÉSULTAT FINAL")
        
        success_rate = (success_count / len(steps)) * 100
        
        print(f"📊 Taux de réussite: {success_rate:.1f}% ({success_count}/{len(steps)})")
        
        if success_rate >= 80:
            print("🎉 SUCCÈS! Projet démarré avec succès")
            print("✅ Vous pouvez maintenant utiliser l'API")
        elif success_rate >= 60:
            print("⚠️ PARTIEL! Projet partiellement fonctionnel")
            print("🔧 Vérifiez les erreurs ci-dessus")
        else:
            print("❌ ÉCHEC! Problèmes de démarrage")
            print("🆘 Consultez la documentation pour résoudre les problèmes")
        
        print(f"\n🌐 Interface principale: {self.base_url}/graphql/")
        print("📚 Documentation complète dans docs/")
        
        return success_rate >= 60

def main():
    """Fonction principale"""
    
    quick_start = QuickStart()
    
    try:
        success = quick_start.run_quick_start()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⏹️ Démarrage interrompu par l'utilisateur")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
