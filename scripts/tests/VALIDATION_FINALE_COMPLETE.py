#!/usr/bin/env python3
"""
VALIDATION FINALE COMPLÈTE - ALX PROJECT NEXUS
Test exhaustif avec gestion d'erreurs robuste
"""

import requests
import json
import sys
import time
from datetime import datetime
import traceback

class ComprehensiveValidator:
    """Validateur complet avec gestion d'erreurs robuste"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.graphql_url = f"{base_url}/graphql/"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'ALX-Project-Nexus-Validator/1.0'
        })
        
        # Statistiques
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors = []
        self.warnings = []
        
        # Configuration des timeouts
        self.timeout = 30
        
    def log_success(self, message):
        """Log un succès"""
        print(f"✅ {message}")
        self.passed_tests += 1
    
    def log_error(self, message, error=None):
        """Log une erreur"""
        print(f"❌ {message}")
        if error:
            print(f"   Détail: {str(error)}")
            self.errors.append(f"{message}: {str(error)}")
        else:
            self.errors.append(message)
        self.failed_tests += 1
    
    def log_warning(self, message):
        """Log un avertissement"""
        print(f"⚠️ {message}")
        self.warnings.append(message)
    
    def safe_request(self, method, url, **kwargs):
        """Effectue une requête sécurisée avec gestion d'erreurs"""
        
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            response = self.session.request(method, url, **kwargs)
            return response, None
        
        except requests.exceptions.ConnectionError as e:
            return None, f"Connection error: {str(e)}"
        
        except requests.exceptions.Timeout as e:
            return None, f"Timeout error: {str(e)}"
        
        except requests.exceptions.RequestException as e:
            return None, f"Request error: {str(e)}"
        
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
    
    def test_server_connectivity(self):
        """Test la connectivité du serveur"""
        
        print("\n🔌 TEST DE CONNECTIVITÉ SERVEUR")
        print("-" * 50)
        
        self.total_tests += 1
        
        response, error = self.safe_request('GET', self.base_url)
        
        if error:
            self.log_error("Serveur inaccessible", error)
            return False
        
        if response.status_code == 200:
            self.log_success("Serveur accessible")
            return True
        else:
            self.log_error(f"Serveur répond avec code {response.status_code}")
            return False
    
    def test_graphql_endpoint(self):
        """Test l'endpoint GraphQL"""
        
        print("\n🎯 TEST ENDPOINT GRAPHQL")
        print("-" * 50)
        
        # Test d'introspection
        self.total_tests += 1
        
        introspection_query = {
            "query": """
            query IntrospectionQuery {
              __schema {
                queryType { name }
                mutationType { name }
                types {
                  name
                  kind
                }
              }
            }
            """
        }
        
        response, error = self.safe_request('POST', self.graphql_url, json=introspection_query)
        
        if error:
            self.log_error("GraphQL endpoint inaccessible", error)
            return False
        
        if response.status_code != 200:
            self.log_error(f"GraphQL endpoint erreur {response.status_code}")
            return False
        
        try:
            data = response.json()
            
            if 'errors' in data:
                self.log_error("Erreurs GraphQL", data['errors'])
                return False
            
            if 'data' in data and '__schema' in data['data']:
                schema = data['data']['__schema']
                
                # Vérifier les types de base
                if schema.get('queryType', {}).get('name') == 'Query':
                    self.log_success("Type Query détecté")
                else:
                    self.log_error("Type Query manquant")
                
                if schema.get('mutationType', {}).get('name') == 'Mutation':
                    self.log_success("Type Mutation détecté")
                else:
                    self.log_error("Type Mutation manquant")
                
                # Compter les types
                types = schema.get('types', [])
                type_count = len([t for t in types if not t['name'].startswith('__')])
                
                if type_count > 10:
                    self.log_success(f"Schema riche avec {type_count} types")
                else:
                    self.log_warning(f"Schema simple avec {type_count} types")
                
                return True
            
            else:
                self.log_error("Réponse GraphQL invalide")
                return False
        
        except json.JSONDecodeError as e:
            self.log_error("Réponse JSON invalide", e)
            return False
        
        except Exception as e:
            self.log_error("Erreur parsing GraphQL", e)
            return False
    
    def test_authentication_flow(self):
        """Test le flux d'authentification complet"""
        
        print("\n🔐 TEST FLUX D'AUTHENTIFICATION")
        print("-" * 50)
        
        # Test 1: Création d'utilisateur
        self.total_tests += 1
        
        create_user_query = {
            "query": """
            mutation CreateTestUser {
              createUser(
                username: "testuser_validation"
                email: "test.validation@example.com"
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
        
        response, error = self.safe_request('POST', self.graphql_url, json=create_user_query)
        
        if error:
            self.log_error("Erreur création utilisateur", error)
            return False
        
        try:
            data = response.json()
            
            if 'errors' in data:
                # Vérifier si c'est une erreur de duplication (acceptable)
                error_messages = [str(err) for err in data['errors']]
                if any('already exists' in msg.lower() or 'duplicate' in msg.lower() for msg in error_messages):
                    self.log_warning("Utilisateur existe déjà (normal)")
                else:
                    self.log_error("Erreurs création utilisateur", data['errors'])
                    return False
            
            elif 'data' in data and data['data']['createUser']['success']:
                self.log_success("Utilisateur créé avec succès")
            
            else:
                self.log_warning("Création utilisateur: résultat ambigu")
        
        except Exception as e:
            self.log_error("Erreur parsing création utilisateur", e)
            return False
        
        # Test 2: Authentification
        self.total_tests += 1
        
        auth_query = {
            "query": """
            mutation AuthenticateUser {
              tokenAuth(
                email: "test.validation@example.com"
                password: "TestPass123!"
              ) {
                token
                payload
                refreshExpiresIn
              }
            }
            """
        }
        
        response, error = self.safe_request('POST', self.graphql_url, json=auth_query)
        
        if error:
            self.log_error("Erreur authentification", error)
            return False
        
        try:
            data = response.json()
            
            if 'errors' in data:
                self.log_error("Erreurs authentification", data['errors'])
                return False
            
            if 'data' in data and data['data']['tokenAuth']['token']:
                token = data['data']['tokenAuth']['token']
                self.session.headers['Authorization'] = f'JWT {token}'
                self.log_success("Authentification réussie")
                return True
            
            else:
                self.log_error("Token JWT non reçu")
                return False
        
        except Exception as e:
            self.log_error("Erreur parsing authentification", e)
            return False
    
    def test_crud_operations(self):
        """Test les opérations CRUD"""
        
        print("\n📝 TEST OPÉRATIONS CRUD")
        print("-" * 50)
        
        # Test 1: Création de post
        self.total_tests += 1
        
        create_post_query = {
            "query": """
            mutation CreateTestPost {
              createPost(
                content: "Post de test pour validation complète #ALX #GraphQL"
                visibility: "public"
              ) {
                post {
                  id
                  content
                  author {
                    username
                  }
                  createdAt
                }
                success
                errors
              }
            }
            """
        }
        
        response, error = self.safe_request('POST', self.graphql_url, json=create_post_query)
        
        if error:
            self.log_error("Erreur création post", error)
            return False
        
        try:
            data = response.json()
            
            if 'errors' in data:
                self.log_error("Erreurs création post", data['errors'])
                return False
            
            if 'data' in data and data['data']['createPost']['success']:
                post_id = data['data']['createPost']['post']['id']
                self.log_success(f"Post créé avec ID: {post_id}")
                
                # Test 2: Lecture de posts
                self.total_tests += 1
                
                read_posts_query = {
                    "query": """
                    query ReadPosts {
                      allPosts(first: 5) {
                        edges {
                          node {
                            id
                            content
                            author {
                              username
                            }
                            likesCount
                            commentsCount
                          }
                        }
                      }
                    }
                    """
                }
                
                response, error = self.safe_request('POST', self.graphql_url, json=read_posts_query)
                
                if error:
                    self.log_error("Erreur lecture posts", error)
                    return False
                
                read_data = response.json()
                
                if 'errors' in read_data:
                    self.log_error("Erreurs lecture posts", read_data['errors'])
                    return False
                
                posts = read_data['data']['allPosts']['edges']
                if len(posts) > 0:
                    self.log_success(f"Lecture réussie: {len(posts)} posts trouvés")
                else:
                    self.log_warning("Aucun post trouvé")
                
                return True
            
            else:
                self.log_error("Création post échouée")
                return False
        
        except Exception as e:
            self.log_error("Erreur parsing CRUD", e)
            return False
    
    def test_error_handling(self):
        """Test la gestion d'erreurs"""
        
        print("\n🛡️ TEST GESTION D'ERREURS")
        print("-" * 50)
        
        # Test 1: Requête invalide
        self.total_tests += 1
        
        invalid_query = {
            "query": "query InvalidQuery { nonExistentField }"
        }
        
        response, error = self.safe_request('POST', self.graphql_url, json=invalid_query)
        
        if error:
            self.log_error("Erreur test requête invalide", error)
            return False
        
        try:
            data = response.json()
            
            if 'errors' in data:
                self.log_success("Gestion d'erreur: requête invalide détectée")
            else:
                self.log_warning("Requête invalide non détectée")
        
        except Exception as e:
            self.log_error("Erreur parsing test erreur", e)
        
        # Test 2: Authentification requise
        self.total_tests += 1
        
        # Supprimer temporairement l'authentification
        auth_header = self.session.headers.pop('Authorization', None)
        
        protected_query = {
            "query": """
            query ProtectedQuery {
              me {
                id
                username
              }
            }
            """
        }
        
        response, error = self.safe_request('POST', self.graphql_url, json=protected_query)
        
        if error:
            self.log_error("Erreur test authentification", error)
        else:
            try:
                data = response.json()
                
                if 'errors' in data:
                    error_messages = [str(err) for err in data['errors']]
                    if any('authentication' in msg.lower() or 'login' in msg.lower() for msg in error_messages):
                        self.log_success("Gestion d'erreur: authentification requise détectée")
                    else:
                        self.log_warning("Erreur d'authentification non spécifique")
                else:
                    self.log_warning("Requête protégée accessible sans authentification")
            
            except Exception as e:
                self.log_error("Erreur parsing test auth", e)
        
        # Restaurer l'authentification
        if auth_header:
            self.session.headers['Authorization'] = auth_header
        
        return True
    
    def test_api_documentation(self):
        """Test la documentation API"""
        
        print("\n📚 TEST DOCUMENTATION API")
        print("-" * 50)
        
        endpoints_to_test = [
            ('/api/docs/', 'Documentation principale'),
            ('/api/swagger/', 'Interface Swagger'),
            ('/api/health/', 'Health check'),
            ('/api/schema/', 'Schéma API')
        ]
        
        for endpoint, description in endpoints_to_test:
            self.total_tests += 1
            
            response, error = self.safe_request('GET', f"{self.base_url}{endpoint}")
            
            if error:
                self.log_error(f"{description} inaccessible", error)
            elif response.status_code == 200:
                self.log_success(f"{description} accessible")
            else:
                self.log_warning(f"{description} code {response.status_code}")
    
    def generate_final_report(self):
        """Génère le rapport final"""
        
        print("\n" + "="*60)
        print("📊 RAPPORT FINAL DE VALIDATION")
        print("="*60)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📈 Tests exécutés: {self.total_tests}")
        print(f"✅ Tests réussis: {self.passed_tests}")
        print(f"❌ Tests échoués: {self.failed_tests}")
        print(f"⚠️ Avertissements: {len(self.warnings)}")
        print(f"🎯 Taux de réussite: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("\n🎊 EXCELLENT! Projet prêt pour production")
            grade = "A+"
        elif success_rate >= 80:
            print("\n🎉 TRÈS BIEN! Quelques améliorations mineures")
            grade = "A"
        elif success_rate >= 70:
            print("\n👍 BIEN! Corrections nécessaires")
            grade = "B"
        elif success_rate >= 60:
            print("\n⚠️ PASSABLE! Améliorations importantes requises")
            grade = "C"
        else:
            print("\n❌ INSUFFISANT! Corrections majeures nécessaires")
            grade = "D"
        
        print(f"📝 Note finale: {grade}")
        
        if self.errors:
            print(f"\n❌ ERREURS DÉTECTÉES ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
        
        if self.warnings:
            print(f"\n⚠️ AVERTISSEMENTS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"   {i}. {warning}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS:")
        if success_rate >= 90:
            print("   - Projet excellent, prêt pour présentation ALX")
            print("   - Documentation complète et fonctionnelle")
            print("   - API robuste avec gestion d'erreurs")
        else:
            print("   - Corriger les erreurs identifiées")
            print("   - Améliorer la gestion d'erreurs")
            print("   - Vérifier la documentation")
        
        return grade, success_rate
    
    def run_complete_validation(self):
        """Lance la validation complète"""
        
        print("🚀 DÉMARRAGE VALIDATION COMPLÈTE ALX PROJECT NEXUS")
        print("=" * 60)
        print(f"⏰ Heure de début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = time.time()
        
        try:
            # Tests séquentiels
            if not self.test_server_connectivity():
                print("\n❌ ARRÊT: Serveur inaccessible")
                return
            
            if not self.test_graphql_endpoint():
                print("\n❌ ARRÊT: GraphQL non fonctionnel")
                return
            
            self.test_authentication_flow()
            self.test_crud_operations()
            self.test_error_handling()
            self.test_api_documentation()
            
        except KeyboardInterrupt:
            print("\n⏹️ Validation interrompue par l'utilisateur")
        
        except Exception as e:
            print(f"\n💥 Erreur inattendue: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
        
        finally:
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\n⏰ Durée totale: {duration:.2f} secondes")
            
            grade, success_rate = self.generate_final_report()
            
            return grade, success_rate

def main():
    """Fonction principale"""
    
    validator = ComprehensiveValidator()
    
    try:
        grade, success_rate = validator.run_complete_validation()
        
        # Code de sortie basé sur le taux de réussite
        if success_rate >= 80:
            sys.exit(0)  # Succès
        else:
            sys.exit(1)  # Échec
    
    except Exception as e:
        print(f"\n💥 Erreur fatale: {str(e)}")
        sys.exit(2)  # Erreur système

if __name__ == "__main__":
    main()
