# Requêtes GraphQL Essentielles - CORRIGÉES

## 🚀 Ouvrir : http://localhost:8000/graphql/

## ✅ 1. CRÉER UN UTILISATEUR
```graphql
mutation {
  createUser(
    username: "testuser1"
    email: "test1@example.com"
    password: "motdepasse123"
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
```

## ✅ 2. SE CONNECTER (CORRIGÉ)
```graphql
mutation {
  tokenAuth(email: "test1@example.com", password: "motdepasse123") {
    token
    payload
    refreshExpiresIn
  }
}
```

**COPIER LE TOKEN !**

## ✅ 3. CONFIGURER L'AUTHENTIFICATION
En bas de l'interface GraphQL, cliquer sur "HTTP Headers" :
```json
{
  "Authorization": "JWT VOTRE_TOKEN_ICI"
}
```

## ✅ 4. CRÉER UN POST
```graphql
mutation {
  createPost(content: "Mon premier post! 🚀") {
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
```

## ✅ 5. VOIR TOUS LES POSTS
```graphql
query {
  allPosts {
        id
        content
        author {
          username
        }
        createdAt
        likesCount
      }
}
```

## ✅ 6. LIKER UN POST
```graphql
mutation {
  likePost(postId: 1) {
    like {
      id
      user {
        username
      }
      post {
        likesCount
      }
    }
    success
    errors
  }
}
```

## ✅ 7. VOIR MON PROFIL
```graphql
query {
  me {
    id
    username
    email
    firstName
    lastName
    postsCount
    followersCount
    followingCount
  }
}
```

## 🎯 ORDRE DE TEST RECOMMANDÉ

1. **Créer utilisateur** (requête 1)
2. **Se connecter** (requête 2) → Copier le token
3. **Configurer headers** (étape 3)
4. **Voir mon profil** (requête 7) → Vérifier que l'auth marche
5. **Créer un post** (requête 4)
6. **Voir les posts** (requête 5)
7. **Liker le post** (requête 6)

## ✅ RÉSULTAT ATTENDU

Si ces 7 requêtes fonctionnent → **Votre projet ALX est 100% opérationnel !**

## 🚨 EN CAS D'ERREUR

```bash
# Vérifier les logs
docker-compose logs web

# Redémarrer si nécessaire
docker-compose restart web
```

## 📱 INTERFACES UTILES

- **GraphQL** : http://localhost:8000/graphql/
- **Admin** : http://localhost:8000/admin/ (admin/admin123)
