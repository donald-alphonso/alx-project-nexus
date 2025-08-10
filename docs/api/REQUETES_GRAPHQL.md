# Requêtes GraphQL Corrigées - ALX Project Nexus

## 🚀 Interface GraphQL
Ouvrir : http://localhost:8000/graphql/

## 1. CRÉER UN UTILISATEUR
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
      firstName
      lastName
    }
    success
    errors
  }
}
```

## 2. SE CONNECTER (OBTENIR TOKEN)
```graphql
mutation {
  tokenAuth(email: "test1@example.com", password: "motdepasse123") {
    token
    payload
    refreshExpiresIn
  }
}
```

**IMPORTANT** : Copier le token retourné !

## 3. CONFIGURER L'AUTHENTIFICATION
En bas de l'interface GraphQL, cliquer sur "HTTP Headers" et ajouter :
```json
{
  "Authorization": "JWT VOTRE_TOKEN_ICI"
}
```

## 4. CRÉER UN POST
```graphql
mutation {
  createPost(content: "Mon premier post de test! 🚀") {
    post {
      id
      content
      author {
        username
        firstName
      }
      createdAt
      likesCount
      commentsCount
    }
    success
    errors
  }
}
```

## 5. VOIR TOUS LES POSTS
```graphql
query {
  allPosts {
    id
    content
    author {
      username
      firstName
      lastName
    }
    createdAt
    likesCount
    commentsCount
    visibility
  }
}
```

## 6. LIKER UN POST
```graphql
mutation {
  likePost(postId: 1) {
    like {
      id
      user {
        username
      }
      post {
        id
        likesCount
      }
    }
    success
    errors
  }
}
```

## 7. COMMENTER UN POST
```graphql
mutation {
  createComment(postId: 1, content: "Excellent post! 👍") {
    comment {
      id
      content
      author {
        username
      }
      post {
        id
        commentsCount
      }
      createdAt
    }
    success
    errors
  }
}
```

## 8. CRÉER UN DEUXIÈME UTILISATEUR
```graphql
mutation {
  createUser(
    username: "testuser2"
    email: "test2@example.com"
    password: "motdepasse123"
    firstName: "Second"
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

## 9. SUIVRE UN UTILISATEUR
```graphql
mutation {
  followUser(userId: 2) {
    follow {
      id
      follower {
        username
      }
      following {
        username
      }
    }
    success
    errors
  }
}
```

## 10. VOIR MON PROFIL
```graphql
query {
  me {
    id
    username
    email
    firstName
    lastName
    followersCount
    followingCount
    postsCount
    bio
    createdAt
  }
}
```

## 11. FEED PERSONNALISÉ
```graphql
query {
  userFeed {
    edges {
      node {
        id
        content
        author {
          username
          firstName
        }
        createdAt
        likesCount
        commentsCount
      }
    }
  }
}
```

## 12. RECHERCHER DES UTILISATEURS
```graphql
query {
  searchUsers(query: "test") {
    id
    username
    firstName
    lastName
    email
    followersCount
  }
}
```

## 13. RECHERCHER DES POSTS
```graphql
query {
  searchPosts(query: "test") {
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

## 🔧 INTERFACES UTILES

### GraphQL Interface
- **URL** : http://localhost:8000/graphql/
- **Documentation** : Cliquer sur "Docs" à droite dans l'interface

### Administration Django
- **URL** : http://localhost:8000/admin/
- **Login** : admin
- **Password** : admin123

## ✅ RÉSULTAT ATTENDU

Si toutes ces requêtes fonctionnent :
- ✅ Votre projet ALX est 100% opérationnel
- ✅ Toutes les fonctionnalités sociales marchent
- ✅ Prêt pour la présentation ALX

## 🚨 EN CAS DE PROBLÈME

```bash
# Vérifier les logs
docker-compose logs web

# Redémarrer
docker-compose restart web

# Redémarrage complet
docker-compose down
docker-compose up -d
```
