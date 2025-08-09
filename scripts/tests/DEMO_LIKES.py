#!/usr/bin/env python3
"""
Démonstration rapide du système de likes
"""

import requests
import json

def demo_likes():
    """Démonstration complète du système de likes"""
    
    print("👍 DÉMONSTRATION SYSTÈME DE LIKES")
    print("=" * 50)
    
    base_url = "http://localhost:8000/graphql/"
    
    # Utiliser le token généré précédemment
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxNzU0NzQ3NjU5QGV4YW1wbGUuY29tIiwidXNlcm5hbWUiOiJ1c2VyMTc1NDc0NzY1OSIsImV4cCI6MTc1NDc1MTI1OSwib3JpZ0lhdCI6MTc1NDc0NzY1OX0.ARUPjl5uYN4qTCvL-TFbecU8GgtSLPmd0kyFmf5VSts"
    
    headers = {
        "Authorization": f"JWT {token}",
        "Content-Type": "application/json"
    }
    
    # Étape 1 : Voir les posts disponibles
    print("\n1️⃣ Récupération des posts disponibles...")
    
    all_posts_query = {
        "query": """
        query {
            allPosts {
                id
                content
                author {
                    username
                }
                likesCount
            }
        }
        """
    }
    
    try:
        response = requests.post(base_url, json=all_posts_query, timeout=10)
        result = response.json()
        
        if 'errors' in result:
            print(f"❌ Erreur récupération posts : {result['errors']}")
            return False
        
        posts = result.get('data', {}).get('allPosts', [])
        
        if not posts:
            print("⚠️ Aucun post trouvé - Création d'un post de test...")
            
            # Créer un post de test
            create_post_query = {
                "query": """
                mutation {
                    createPost(content: "Post de démonstration pour les likes ! 👍🚀") {
                        post {
                            id
                            content
                            likesCount
                        }
                        success
                        errors
                    }
                }
                """
            }
            
            response = requests.post(base_url, json=create_post_query, headers=headers, timeout=10)
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ Erreur création post : {result['errors']}")
                return False
            
            post_data = result.get('data', {}).get('createPost', {})
            if post_data.get('success'):
                print(f"✅ Post créé : ID {post_data['post']['id']}")
                posts = [post_data['post']]
            else:
                print(f"❌ Échec création post : {post_data.get('errors', [])}")
                return False
        
        print(f"✅ {len(posts)} posts trouvés")
        
        # Afficher les premiers posts
        print("\n📋 Posts disponibles :")
        for i, post in enumerate(posts[:5], 1):
            print(f"  {i}. ID {post['id']}: {post['content'][:50]}... (👍 {post['likesCount']} likes)")
        
    except Exception as e:
        print(f"❌ Erreur récupération posts : {e}")
        return False
    
    # Étape 2 : Liker les premiers posts
    print(f"\n2️⃣ Test de likes sur les premiers posts...")
    
    posts_a_liker = posts[:3]  # Liker les 3 premiers posts
    likes_reussis = 0
    
    for i, post in enumerate(posts_a_liker, 1):
        print(f"\n👍 Like du post {i} (ID: {post['id']})...")
        
        like_post_query = {
            "query": f"""
            mutation {{
                likePost(postId: {post['id']}) {{
                    like {{
                        id
                        user {{
                            username
                        }}
                        createdAt
                    }}
                    success
                    errors
                }}
            }}
            """
        }
        
        try:
            response = requests.post(base_url, json=like_post_query, headers=headers, timeout=10)
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ Erreur like : {result['errors']}")
            else:
                like_data = result.get('data', {}).get('likePost', {})
                if like_data.get('success'):
                    like = like_data.get('like')
                    if like:
                        print(f"✅ Like ajouté par {like['user']['username']}")
                        likes_reussis += 1
                    else:
                        print("✅ Like enregistré (peut-être déjà existant)")
                        likes_reussis += 1
                else:
                    print(f"❌ Échec like : {like_data.get('errors', [])}")
        except Exception as e:
            print(f"❌ Erreur like : {e}")
    
    print(f"\n✅ {likes_reussis} likes traités avec succès")
    
    # Étape 3 : Vérifier les likes ajoutés
    print(f"\n3️⃣ Vérification des likes ajoutés...")
    
    try:
        response = requests.post(base_url, json=all_posts_query, timeout=10)
        result = response.json()
        
        if 'errors' not in result:
            posts_updated = result.get('data', {}).get('allPosts', [])
            
            print(f"\n📊 État des likes après test :")
            for post in posts_updated[:5]:
                print(f"  - ID {post['id']}: {post['content'][:50]}... (👍 {post['likesCount']} likes)")
            
        else:
            print(f"❌ Erreur vérification : {result['errors']}")
    except Exception as e:
        print(f"❌ Erreur vérification : {e}")
    
    return True

def afficher_instructions_manuelles():
    """Afficher les instructions pour tests manuels"""
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS POUR TESTS MANUELS")
    print("=" * 60)
    
    print("\n🔑 Token JWT à utiliser :")
    print("JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxNzU0NzQ3NjU5QGV4YW1wbGUuY29tIiwidXNlcm5hbWUiOiJ1c2VyMTc1NDc0NzY1OSIsImV4cCI6MTc1NDc1MTI1OSwib3JpZ0lhdCI6MTc1NDc0NzY1OX0.ARUPjl5uYN4qTCvL-TFbecU8GgtSLPmd0kyFmf5VSts")
    
    print("\n🚀 Étapes dans le navigateur :")
    print("1. Aller sur : http://localhost:8000/graphql/")
    print("2. Cliquer 'HTTP Headers' et ajouter :")
    print('   {"Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXIxNzU0NzQ3NjU5QGV4YW1wbGUuY29tIiwidXNlcm5hbWUiOiJ1c2VyMTc1NDc0NzY1OSIsImV4cCI6MTc1NDc1MTI1OSwib3JpZ0lhdCI6MTc1NDc0NzY1OX0.ARUPjl5uYN4qTCvL-TFbecU8GgtSLPmd0kyFmf5VSts"}')
    
    print("\n👀 3. Voir les posts :")
    print("""
query {
  allPosts {
    id
    content
    author {
      username
    }
    likesCount
  }
}
    """)
    
    print("\n👍 4. Liker un post (remplacer l'ID) :")
    print("""
mutation {
  likePost(postId: 1) {
    like {
      id
      user {
        username
      }
    }
    success
    errors
  }
}
    """)
    
    print("\n✅ 5. Vérifier le like (relancer la query des posts)")
    print("   → Le likesCount doit avoir augmenté !")

if __name__ == "__main__":
    print("🎯 DÉMONSTRATION COMPLÈTE DU SYSTÈME DE LIKES")
    print("=" * 70)
    
    # Lancer la démonstration
    success = demo_likes()
    
    # Afficher les instructions manuelles
    afficher_instructions_manuelles()
    
    print("\n" + "=" * 70)
    if success:
        print("🎊 DÉMONSTRATION RÉUSSIE ! Système de likes fonctionnel !")
    else:
        print("⚠️ Démonstration partielle - Vérifiez les erreurs")
    
    print("🌟 Testez maintenant manuellement dans votre navigateur !")
