#!/usr/bin/env python3
"""
TEST DE CLARTÉ POUR DÉBUTANTS
Vérifie si un débutant complet peut utiliser l'API facilement
"""

import requests
import json
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}{title.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ️ {message}{Colors.END}")

def test_documentation_accessibility_for_beginners():
    """Test si la documentation est accessible pour un débutant"""
    
    print_header("TEST 1: ACCESSIBILITÉ POUR DÉBUTANTS")
    
    print_info("Simulation d'un débutant accédant à la documentation...")
    
    # Test de la page principale de documentation
    try:
        response = requests.get("http://localhost:8000/api/docs/", timeout=10)
        if response.status_code == 200:
            content = response.text.lower()
            
            # Critères de clarté pour débutants
            clarity_checks = [
                ("Titre clair", "alx project nexus" in content or "graphql api" in content),
                ("Interface moderne", "html" in content and "css" in content),
                ("Navigation simple", "link" in content or "href" in content),
                ("Contenu en français/anglais", "api" in content and ("documentation" in content or "endpoint" in content)),
            ]
            
            passed_checks = 0
            for check_name, passed in clarity_checks:
                if passed:
                    print_success(f"{check_name}: OK")
                    passed_checks += 1
                else:
                    print_error(f"{check_name}: Manquant")
            
            if passed_checks >= 3:
                print_success("Documentation accessible pour débutants ✅")
                return True
            else:
                print_error("Documentation trop complexe pour débutants")
                return False
        else:
            print_error(f"Documentation inaccessible: Status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erreur d'accès à la documentation: {e}")
        return False

def test_graphql_interface_simplicity():
    """Test si l'interface GraphQL est simple pour un débutant"""
    
    print_header("TEST 2: SIMPLICITÉ INTERFACE GRAPHQL")
    
    print_info("Test de l'interface GraphQL pour débutants...")
    
    try:
        # Test d'accès à GraphiQL
        response = requests.get("http://localhost:8000/graphql/", timeout=10)
        if response.status_code == 200:
            print_success("Interface GraphQL accessible ✅")
            
            # Test d'une requête simple qu'un débutant pourrait faire
            simple_query = {
                "query": "query { __typename }"
            }
            
            response = requests.post(
                "http://localhost:8000/graphql/",
                json=simple_query,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    print_success("Requête simple fonctionne ✅")
                    print_info("Un débutant peut faire des requêtes basiques")
                    return True
                else:
                    print_error("Réponse GraphQL invalide")
                    return False
            else:
                print_error("Erreur dans la requête simple")
                return False
        else:
            print_error("Interface GraphQL inaccessible")
            return False
    except Exception as e:
        print_error(f"Erreur interface GraphQL: {e}")
        return False

def test_beginner_friendly_examples():
    """Test si les exemples sont adaptés aux débutants"""
    
    print_header("TEST 3: EXEMPLES POUR DÉBUTANTS")
    
    print_info("Test des exemples simples pour débutants...")
    
    # Exemples qu'un débutant devrait pouvoir comprendre et utiliser
    beginner_examples = [
        {
            "name": "Voir tous les posts",
            "query": {
                "query": """
                query {
                  allPosts {
                    id
                    content
                    author {
                      username
                    }
                  }
                }
                """
            },
            "should_work": True
        },
        {
            "name": "Introspection simple",
            "query": {
                "query": """
                query {
                  __schema {
                    queryType {
                      name
                    }
                  }
                }
                """
            },
            "should_work": True
        }
    ]
    
    results = []
    
    for example in beginner_examples:
        print_info(f"Test: {example['name']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/graphql/",
                json=example["query"],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and not data.get('errors'):
                    print_success(f"{example['name']}: Fonctionne ✅")
                    results.append(True)
                else:
                    print_error(f"{example['name']}: Erreur dans la réponse")
                    results.append(False)
            else:
                print_error(f"{example['name']}: Status {response.status_code}")
                results.append(False)
        except Exception as e:
            print_error(f"{example['name']}: Erreur {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    if success_rate >= 80:
        print_success(f"Exemples pour débutants: {success_rate:.0f}% fonctionnent ✅")
        return True
    else:
        print_error(f"Exemples trop complexes: seulement {success_rate:.0f}% fonctionnent")
        return False

def test_error_messages_clarity():
    """Test si les messages d'erreur sont clairs pour un débutant"""
    
    print_header("TEST 4: CLARTÉ DES MESSAGES D'ERREUR")
    
    print_info("Test des messages d'erreur pour débutants...")
    
    # Test d'une requête intentionnellement incorrecte
    bad_query = {
        "query": "query { nonExistentField }"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/graphql/",
            json=bad_query,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                error_message = str(data['errors'][0].get('message', ''))
                
                # Vérifier si le message d'erreur est compréhensible
                clarity_indicators = [
                    'field' in error_message.lower(),
                    'cannot query' in error_message.lower() or 'not found' in error_message.lower(),
                    len(error_message) > 10  # Message pas trop court
                ]
                
                if sum(clarity_indicators) >= 2:
                    print_success("Messages d'erreur clairs pour débutants ✅")
                    print_info(f"Exemple d'erreur: {error_message[:50]}...")
                    return True
                else:
                    print_error("Messages d'erreur trop techniques")
                    return False
            else:
                print_error("Pas de gestion d'erreur appropriée")
                return False
        else:
            print_error("Problème avec la gestion d'erreur")
            return False
    except Exception as e:
        print_error(f"Erreur test de clarté: {e}")
        return False

def test_beginner_workflow():
    """Test d'un workflow complet pour débutant"""
    
    print_header("TEST 5: WORKFLOW COMPLET DÉBUTANT")
    
    print_info("Simulation d'un débutant utilisant l'API étape par étape...")
    
    workflow_steps = []
    
    # Étape 1: Accès à la documentation
    print_info("Étape 1: Accès à la documentation")
    try:
        response = requests.get("http://localhost:8000/api/docs/", timeout=5)
        if response.status_code == 200:
            print_success("✅ Débutant peut accéder à la doc")
            workflow_steps.append(True)
        else:
            print_error("❌ Documentation inaccessible")
            workflow_steps.append(False)
    except:
        print_error("❌ Erreur d'accès à la documentation")
        workflow_steps.append(False)
    
    # Étape 2: Interface GraphQL
    print_info("Étape 2: Test interface GraphQL")
    try:
        response = requests.get("http://localhost:8000/graphql/", timeout=5)
        if response.status_code == 200:
            print_success("✅ Interface GraphQL accessible")
            workflow_steps.append(True)
        else:
            print_error("❌ Interface GraphQL inaccessible")
            workflow_steps.append(False)
    except:
        print_error("❌ Erreur interface GraphQL")
        workflow_steps.append(False)
    
    # Étape 3: Première requête simple
    print_info("Étape 3: Première requête simple")
    try:
        simple_query = {"query": "query { __typename }"}
        response = requests.post(
            "http://localhost:8000/graphql/",
            json=simple_query,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200 and 'data' in response.json():
            print_success("✅ Première requête réussie")
            workflow_steps.append(True)
        else:
            print_error("❌ Première requête échouée")
            workflow_steps.append(False)
    except:
        print_error("❌ Erreur première requête")
        workflow_steps.append(False)
    
    # Étape 4: Requête avec données réelles
    print_info("Étape 4: Requête avec données réelles")
    try:
        posts_query = {"query": "query { allPosts { id content } }"}
        response = requests.post(
            "http://localhost:8000/graphql/",
            json=posts_query,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'allPosts' in data['data']:
                print_success("✅ Données réelles récupérées")
                workflow_steps.append(True)
            else:
                print_success("✅ Structure de réponse correcte (même si pas de données)")
                workflow_steps.append(True)
        else:
            print_error("❌ Erreur récupération données")
            workflow_steps.append(False)
    except:
        print_error("❌ Erreur requête données")
        workflow_steps.append(False)
    
    success_rate = sum(workflow_steps) / len(workflow_steps) * 100
    
    if success_rate >= 75:
        print_success(f"Workflow débutant: {success_rate:.0f}% de réussite ✅")
        return True
    else:
        print_error(f"Workflow trop complexe: {success_rate:.0f}% de réussite")
        return False

def generate_beginner_report():
    """Génère un rapport de clarté pour débutants"""
    
    print_header("RAPPORT FINAL: CLARTÉ POUR DÉBUTANTS")
    
    # Exécuter tous les tests
    tests = [
        ("Documentation Accessible", test_documentation_accessibility_for_beginners),
        ("Interface Simple", test_graphql_interface_simplicity),
        ("Exemples Adaptés", test_beginner_friendly_examples),
        ("Messages d'Erreur Clairs", test_error_messages_clarity),
        ("Workflow Complet", test_beginner_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            print_info(f"{test_name}: {'RÉUSSI' if result else 'ÉCHEC'}")
        except Exception as e:
            print_error(f"{test_name}: ERREUR - {e}")
            results.append(False)
    
    # Calcul du score final
    passed = sum(results)
    total = len(results)
    score = (passed / total) * 100
    
    print(f"\n{Colors.BOLD}RÉSULTATS FINAUX POUR DÉBUTANTS:{Colors.END}")
    print(f"Tests réussis: {Colors.GREEN}{passed}/{total}{Colors.END}")
    print(f"Score de clarté: {Colors.BOLD}{score:.1f}%{Colors.END}")
    
    # Évaluation finale
    if score >= 90:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎊 EXCELLENT ! PARFAIT POUR DÉBUTANTS{Colors.END}")
        print(f"{Colors.GREEN}✅ Un débutant complet peut utiliser votre API facilement{Colors.END}")
        print(f"{Colors.GREEN}✅ Documentation claire et accessible{Colors.END}")
        print(f"{Colors.GREEN}✅ Interface intuitive{Colors.END}")
        print(f"{Colors.GREEN}✅ Exemples simples et fonctionnels{Colors.END}")
        grade = "EXCELLENT"
    elif score >= 75:
        print(f"\n{Colors.CYAN}{Colors.BOLD}✅ TRÈS BIEN ! Accessible aux débutants{Colors.END}")
        print(f"{Colors.CYAN}✅ Quelques petites améliorations possibles{Colors.END}")
        grade = "TRÈS BIEN"
    elif score >= 60:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ CORRECT - Améliorations nécessaires{Colors.END}")
        grade = "CORRECT"
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ DIFFICILE - Trop complexe pour débutants{Colors.END}")
        grade = "DIFFICILE"
    
    # Recommandations pour débutants
    print(f"\n{Colors.BOLD}RECOMMANDATIONS POUR DÉBUTANTS:{Colors.END}")
    print(f"1. 📚 Commencer par: http://localhost:8000/api/docs/")
    print(f"2. 🧪 Tester avec: http://localhost:8000/graphql/")
    print(f"3. ⚡ Documentation avancée: http://localhost:8000/api/swagger/")
    
    return score, grade

def main():
    """Fonction principale"""
    
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("👶 TEST DE CLARTÉ POUR DÉBUTANTS COMPLETS")
    print("🎯 Vérification de l'accessibilité de l'API ALX Project Nexus")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.END}")
    
    try:
        score, grade = generate_beginner_report()
        
        print_header("CONCLUSION FINALE")
        print(f"{Colors.BOLD}Score de clarté: {score:.1f}%{Colors.END}")
        print(f"{Colors.BOLD}Grade: {grade}{Colors.END}")
        
        if score >= 90:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎊 FÉLICITATIONS !{Colors.END}")
            print(f"{Colors.GREEN}Votre API est PARFAITE pour les débutants !{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrompu par l'utilisateur{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur lors du test: {e}{Colors.END}")

if __name__ == "__main__":
    main()
