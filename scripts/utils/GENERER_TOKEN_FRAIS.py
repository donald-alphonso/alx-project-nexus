#!/usr/bin/env python3
"""
Script pour générer un token JWT frais et valide
"""

import requests
import json
import time

def generer_token_frais():
    """Générer un nouveau token JWT valide"""
    
    print("🔑 GÉNÉRATION TOKEN JWT FRAIS")
    print("=" * 40)
    
    base_url = "http://localhost:8000/graphql/"
    
    # Étape 1 : Créer un nouvel utilisateur avec un nom unique
    timestamp = str(int(time.time()))
    username = f"user{timestamp}"
    email = f"user{timestamp}@example.com"
    
    print(f"\n1️⃣ Création utilisateur unique : {username}")
    
    create_user_mutation = {
        "query": f"""
        mutation {{
            createUser(
                username: "{username}"
                email: "{email}"
                password: "motdepasse123"
                firstName: "User"
                lastName: "Fresh"
            ) {{
                user {{
                    id
                    username
                    email
                }}
                success
                errors
            }}
        }}
        """
    }
    
    try:
        response = requests.post(base_url, json=create_user_mutation, timeout=10)
        result = response.json()
        
        if 'errors' in result:
            print(f"❌ Erreur création utilisateur : {result['errors']}")
            return None
        
        user_data = result.get('data', {}).get('createUser', {})
        if not user_data.get('success'):
            print(f"❌ Échec création utilisateur : {user_data.get('errors', [])}")
            return None
        
        print(f"✅ Utilisateur créé : {user_data['user']['username']}")
        
    except Exception as e:
        print(f"❌ Erreur création utilisateur : {e}")
        return None
    
    # Étape 2 : Se connecter et récupérer un token frais
    print(f"\n2️⃣ Génération token JWT pour {username}...")
    
    login_mutation = {
        "query": f"""
        mutation {{
            tokenAuth(email: "{email}", password: "motdepasse123") {{
                token
                payload
                refreshExpiresIn
            }}
        }}
        """
    }
    
    try:
        response = requests.post(base_url, json=login_mutation, timeout=10)
        result = response.json()
        
        if 'errors' in result:
            print(f"❌ Erreur génération token : {result['errors']}")
            return None
        
        token_data = result.get('data', {}).get('tokenAuth', {})
        token = token_data.get('token')
        
        if not token:
            print("❌ Token non généré")
            return None
        
        print(f"✅ Token JWT généré avec succès !")
        print(f"🔑 Token : {token}")
        
        return token, username, email
        
    except Exception as e:
        print(f"❌ Erreur génération token : {e}")
        return None

def tester_token(token):
    """Tester la validité du token généré"""
    
    print(f"\n3️⃣ Test de validité du token...")
    
    base_url = "http://localhost:8000/graphql/"
    
    headers = {
        "Authorization": f"JWT {token}",
        "Content-Type": "application/json"
    }
    
    # Test avec la query 'me'
    me_query = {
        "query": """
        query {
            me {
                id
                username
                email
                firstName
                lastName
            }
        }
        """
    }
    
    try:
        response = requests.post(base_url, json=me_query, headers=headers, timeout=10)
        result = response.json()
        
        if 'errors' in result:
            print(f"❌ Erreur test token : {result['errors']}")
            return False
        
        me_data = result.get('data', {}).get('me', {})
        if me_data:
            print(f"✅ Token valide ! Utilisateur : {me_data['username']}")
            return True
        else:
            print("❌ Token invalide - pas de données utilisateur")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test token : {e}")
        return False

def afficher_instructions(token, username):
    """Afficher les instructions d'utilisation"""
    
    print("\n" + "=" * 60)
    print("🎯 INSTRUCTIONS POUR UTILISER LE TOKEN")
    print("=" * 60)
    
    print(f"\n🔑 VOTRE TOKEN JWT VALIDE :")
    print(f"JWT {token}")
    
    print(f"\n📋 ÉTAPES POUR TESTER DANS LE NAVIGATEUR :")
    print("1. Aller sur : http://localhost:8000/graphql/")
    print("2. Cliquer sur 'HTTP Headers' en bas à gauche")
    print("3. Dans la zone qui s'ouvre, copier-coller EXACTEMENT :")
    print()
    print(f'{{"Authorization": "JWT {token}"}}')
    print()
    print("4. Tester cette requête :")
    
    print("""
query {
  me {
    id
    username
    email
    firstName
    lastName
  }
}
    """)
    
    print(f"✅ Résultat attendu : Profil de {username}")
    
    print("\n🚀 REQUÊTES À TESTER ENSUITE :")
    
    print("\n📝 Créer un post :")
    print("""
mutation {
  createPost(content: "Mon post avec le nouveau token ! 🎉") {
    post {
      id
      content
      author {
        username
      }
      likesCount
    }
    success
    errors
  }
}
    """)
    
    print("\n📊 Voir tous les posts :")
    print("""
query {
  allPosts {
    id
    content
    author {
      username
    }
    likesCount
    commentsCount
  }
}
    """)

def main():
    """Fonction principale"""
    
    print("🚀 GÉNÉRATEUR DE TOKEN JWT FRAIS")
    print("=" * 50)
    print("Ce script va créer un nouvel utilisateur et générer un token valide")
    
    # Générer le token
    result = generer_token_frais()
    
    if result is None:
        print("\n❌ ÉCHEC - Impossible de générer un token valide")
        print("Vérifiez que votre serveur fonctionne :")
        print("- docker-compose ps")
        print("- http://localhost:8000/graphql/")
        return
    
    token, username, email = result
    
    # Tester le token
    if tester_token(token):
        print(f"\n🎊 SUCCÈS TOTAL !")
        print(f"✅ Token JWT valide généré")
        print(f"✅ Utilisateur créé : {username}")
        print(f"✅ Email : {email}")
        
        # Afficher les instructions
        afficher_instructions(token, username)
        
        print(f"\n🌟 VOTRE TOKEN EST PRÊT À UTILISER !")
        print("Copiez le token ci-dessus et utilisez-le dans GraphQL")
        
    else:
        print(f"\n⚠️ Token généré mais problème de validation")
        print("Essayez de redémarrer le serveur :")
        print("docker-compose restart web")

if __name__ == "__main__":
    main()
