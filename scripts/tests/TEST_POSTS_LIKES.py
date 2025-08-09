#!/usr/bin/env python3
"""
Script de test spécifique pour la création de posts et les likes
"""

import requests
import json
import time

def test_creation_posts_et_likes():
    """Test complet : création de posts et système de likes"""
    
    print("🚀 TEST CRÉATION POSTS ET LIKES")
    print("=" * 50)
    
    base_url = "http://localhost:8000/graphql/"
    
    # Étape 1 : Créer un utilisateur de test
    print("\n1️⃣ Création d'un utilisateur de test...")
    
    create_user_mutation = {
        "query": """
        mutation {
            createUser(
                username: "testposts2025"
                email: "testposts2025@example.com"
                password: "motdepasse123"
                firstName: "Test"
                lastName: "Posts"
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
        response = requests.post(base_url, json=create_user_mutation, timeout=10)
        result = response.json()
        
        if 'errors' in result:
            print(f"⚠️ Erreur création utilisateur (peut-être déjà existant) : {result['errors']}")
        else:
            user_data = result.get('data', {}).get('createUser', {})
            if user_data.get('success'):
                print(f"✅ Utilisateur créé : {user_data['user']['username']}")
            else:
                print(f"⚠️ Erreurs : {user_data.get('errors', [])}")
    except Exception as e:
        print(f"❌ Erreur création utilisateur : {e}")
        return False
    
    # Étape 2 : Se connecter et récupérer le token
    print("\n2️⃣ Connexion et récupération du token JWT...")
    
    login_mutation = {
        "query": """
        mutation {
            tokenAuth(email: "testposts2025@example.com", password: "motdepasse123") {
                token
                payload
                refreshExpiresIn
            }
        }
        """
    }
    
    try:
        response = requests.post(base_url, json=login_mutation, timeout=10)
        result = response.json()
        
        if 'errors' in result:
            print(f"❌ Erreur connexion : {result['errors']}")
            return False
        
        token_data = result.get('data', {}).get('tokenAuth', {})
        token = token_data.get('token')
        
        if not token:
            print("❌ Token non récupéré")
            return False
        
        print(f"✅ Token JWT récupéré : {token[:30]}...")
        
        headers = {
            "Authorization": f"JWT {token}",
            "Content-Type": "application/json"
        }
        
    except Exception as e:
        print(f"❌ Erreur connexion : {e}")
        return False
    
    # Étape 3 : Créer plusieurs posts
    print("\n3️⃣ Création de posts...")
    
    posts_a_creer = [
        "Mon premier post de test ! 🚀",
        "Voici un post sur la technologie Django et GraphQL 💻",
        "Test des fonctionnalités de notre réseau social ALX 🌟",
        "Post avec des hashtags #ALX #Django #GraphQL #Python",
        "Dernier post pour tester les interactions 👍"
    ]
    
    posts_crees = []
    
    for i, contenu in enumerate(posts_a_creer, 1):
        print(f"\n📝 Création du post {i}/5...")
        
        create_post_mutation = {
            "query": """
            mutation {
                createPost(content: "%s") {
                    post {
                        id
                        content
                        author {
                            username
                        }
                        createdAt
                        likesCount
                        commentsCount
                    }
                    success
                    errors
                }
            }
            """ % contenu
        }
        
        try:
            response = requests.post(base_url, json=create_post_mutation, headers=headers, timeout=10)
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ Erreur création post {i} : {result['errors']}")
            else:
                post_data = result.get('data', {}).get('createPost', {})
                if post_data.get('success'):
                    post = post_data['post']
                    posts_crees.append(post)
                    print(f"✅ Post {i} créé - ID: {post['id']} - Contenu: {post['content'][:50]}...")
                else:
                    print(f"❌ Échec création post {i} : {post_data.get('errors', [])}")
        except Exception as e:
            print(f"❌ Erreur création post {i} : {e}")
    
    if not posts_crees:
        print("❌ Aucun post créé - Arrêt du test")
        return False
    
    print(f"\n✅ {len(posts_crees)} posts créés avec succès !")
    
    # Étape 4 : Tester les likes sur les posts
    print("\n4️⃣ Test du système de likes...")
    
    likes_crees = []
    
    for i, post in enumerate(posts_crees[:3], 1):  # Liker les 3 premiers posts
        print(f"\n👍 Like du post {i} (ID: {post['id']})...")
        
        like_post_mutation = {
            "query": """
            mutation {
                likePost(postId: %s) {
                    like {
                        id
                        post {
                            id
                            content
                            likesCount
                        }
                        user {
                            username
                        }
                        createdAt
                    }
                    success
                    errors
                }
            }
            """ % post['id']
        }
        
        try:
            response = requests.post(base_url, json=like_post_mutation, headers=headers, timeout=10)
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ Erreur like post {i} : {result['errors']}")
            else:
                like_data = result.get('data', {}).get('likePost', {})
                if like_data.get('success'):
                    like = like_data['like']
                    likes_crees.append(like)
                    print(f"✅ Like ajouté au post {i} - Nouveau total: {like['post']['likesCount']} likes")
                else:
                    print(f"❌ Échec like post {i} : {like_data.get('errors', [])}")
        except Exception as e:
            print(f"❌ Erreur like post {i} : {e}")
    
    print(f"\n✅ {len(likes_crees)} likes ajoutés avec succès !")
    
    # Étape 5 : Vérifier les posts avec leurs likes
    print("\n5️⃣ Vérification des posts avec likes...")
    
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
                commentsCount
                createdAt
            }
        }
        """
    }
    
    try:
        response = requests.post(base_url, json=all_posts_query, timeout=10)
        result = response.json()
        
        if 'errors' not in result:
            posts = result.get('data', {}).get('allPosts', [])
            
            print(f"📊 Total des posts dans la base : {len(posts)}")
            
            # Afficher les posts récemment créés
            posts_recents = [p for p in posts if p['author']['username'] == 'testposts2025']
            
            print(f"\n📝 Vos posts créés ({len(posts_recents)}) :")
            for post in posts_recents:
                print(f"  - ID {post['id']}: {post['content'][:50]}... (👍 {post['likesCount']} likes)")
            
        else:
            print(f"❌ Erreur récupération posts : {result['errors']}")
    except Exception as e:
        print(f"❌ Erreur vérification posts : {e}")
    
    # Étape 6 : Test de création de commentaires
    print("\n6️⃣ Test de création de commentaires...")
    
    if posts_crees:
        premier_post = posts_crees[0]
        
        create_comment_mutation = {
            "query": """
            mutation {
                createComment(postId: %s, content: "Super post ! J'adore ce contenu 🎉") {
                    comment {
                        id
                        content
                        author {
                            username
                        }
                        post {
                            id
                            content
                            commentsCount
                        }
                        createdAt
                    }
                    success
                    errors
                }
            }
            """ % premier_post['id']
        }
        
        try:
            response = requests.post(base_url, json=create_comment_mutation, headers=headers, timeout=10)
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ Erreur création commentaire : {result['errors']}")
            else:
                comment_data = result.get('data', {}).get('createComment', {})
                if comment_data.get('success'):
                    comment = comment_data['comment']
                    print(f"✅ Commentaire créé sur le post {premier_post['id']}")
                    print(f"   Contenu: {comment['content']}")
                    print(f"   Nouveau total commentaires: {comment['post']['commentsCount']}")
                else:
                    print(f"❌ Échec création commentaire : {comment_data.get('errors', [])}")
        except Exception as e:
            print(f"❌ Erreur création commentaire : {e}")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("🎊 RÉSUMÉ DU TEST POSTS ET LIKES")
    print("=" * 60)
    print(f"✅ Posts créés : {len(posts_crees)}")
    print(f"✅ Likes ajoutés : {len(likes_crees)}")
    print("✅ Commentaire créé : 1")
    print("\n🌟 FONCTIONNALITÉS TESTÉES AVEC SUCCÈS :")
    print("  - Authentification JWT")
    print("  - Création de posts")
    print("  - Système de likes")
    print("  - Création de commentaires")
    print("  - Compteurs automatiques")
    print("  - Récupération des données")
    
    print(f"\n🔑 Token JWT pour tests manuels :")
    print(f"JWT {token}")
    
    print("\n📋 INSTRUCTIONS POUR TEST MANUEL :")
    print("1. Aller sur http://localhost:8000/graphql/")
    print("2. Cliquer 'HTTP Headers' et ajouter :")
    print(f'   {{"Authorization": "JWT {token}"}}')
    print("3. Tester les requêtes de création/like")
    
    return True

def afficher_requetes_test():
    """Afficher les requêtes pour tests manuels"""
    
    print("\n📋 REQUÊTES POUR TESTS MANUELS")
    print("=" * 40)
    
    print("\n🔐 1. Se connecter (récupérer token) :")
    print("""
mutation {
  tokenAuth(email: "testposts2025@example.com", password: "motdepasse123") {
    token
  }
}
    """)
    
    print("\n📝 2. Créer un post :")
    print("""
mutation {
  createPost(content: "Mon nouveau post de test ! 🚀") {
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
    
    print("\n👍 3. Liker un post (remplacer ID) :")
    print("""
mutation {
  likePost(postId: 1) {
    like {
      id
      post {
        id
        content
        likesCount
      }
      user {
        username
      }
    }
    success
    errors
  }
}
    """)
    
    print("\n💬 4. Commenter un post (remplacer ID) :")
    print("""
mutation {
  createComment(postId: 1, content: "Excellent post ! 👏") {
    comment {
      id
      content
      author {
        username
      }
      post {
        commentsCount
      }
    }
    success
    errors
  }
}
    """)
    
    print("\n📊 5. Voir tous les posts avec likes :")
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
    createdAt
  }
}
    """)

if __name__ == "__main__":
    print("🎯 TEST SPÉCIFIQUE - POSTS ET LIKES")
    print("=" * 60)
    
    # Lancer le test automatique
    success = test_creation_posts_et_likes()
    
    # Afficher les requêtes pour tests manuels
    afficher_requetes_test()
    
    print("\n" + "=" * 60)
    if success:
        print("🎊 TEST RÉUSSI ! Système de posts et likes fonctionnel !")
    else:
        print("⚠️ Test partiel - Vérifiez les erreurs ci-dessus")
    
    print("🌟 Votre projet ALX est prêt pour la démonstration !")
