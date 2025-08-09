# 📋 REQUÊTES PRÊTES À COPIER-COLLER

## 🌐 Interface : http://localhost:8000/graphql/

---

## 🔓 REQUÊTES SANS AUTHENTIFICATION

### 1. Test de Santé
```graphql
query {
  health
}
```

### 2. Tous les Utilisateurs
```graphql
query {
  allUsers {
    id
    username
    email
    firstName
    lastName
    postsCount
    followersCount
  }
}
```

### 3. Tous les Posts
```graphql
query {
  allPosts {
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
```

### 4. Rechercher Utilisateurs
```graphql
query {
  searchUsers(query: "admin") {
    id
    username
    firstName
    lastName
    email
  }
}
```

### 5. Voir un Utilisateur Spécifique
```graphql
query {
  user(id: 1) {
    id
    username
    email
    firstName
    lastName
    bio
    postsCount
    followersCount
    followingCount
  }
}
```

---

## 🔐 REQUÊTES AVEC AUTHENTIFICATION

### 6. Créer un Utilisateur
```graphql
mutation {
  createUser(
    username: "montest2025"
    email: "montest2025@example.com"
    password: "motdepasse123"
    firstName: "Mon"
    lastName: "Test"
  ) {
    user {
      id
      username
      email
      firstName
    }
    success
    errors
  }
}
```

### 7. Se Connecter (Récupérer Token)
```graphql
mutation {
  tokenAuth(email: "montest2025@example.com", password: "motdepasse123") {
    token
    payload
    refreshExpiresIn
  }
}
```

**🔑 APRÈS AVOIR RÉCUPÉRÉ LE TOKEN :**
1. Cliquer "HTTP Headers" en bas à gauche
2. Ajouter :
```json
{
  "Authorization": "JWT VOTRE_TOKEN_ICI"
}
```

### 8. Mon Profil
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

### 9. Créer un Post
```graphql
mutation {
  createPost(content: "Mon premier post depuis le navigateur ! 🚀") {
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

### 10. Mon Feed Personnalisé
```graphql
query {
  feed {
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

### 11. Liker un Post
```graphql
mutation {
  likePost(postId: 1) {
    like {
      id
      post {
        content
      }
      user {
        username
      }
    }
    success
    errors
  }
}
```

### 12. Commenter un Post
```graphql
mutation {
  createComment(postId: 1, content: "Super post ! 👍") {
    comment {
      id
      content
      author {
        username
      }
      post {
        content
      }
    }
    success
    errors
  }
}
```

### 13. Suivre un Utilisateur
```graphql
mutation {
  followUser(userId: 1) {
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

### 14. Mettre à Jour Mon Profil
```graphql
mutation {
  updateProfile(
    firstName: "Nouveau"
    lastName: "Nom"
    bio: "Ma nouvelle bio !"
  ) {
    user {
      id
      username
      firstName
      lastName
      bio
    }
    success
    errors
  }
}
```

---

## 🎯 ORDRE DE TEST RECOMMANDÉ

### Phase 1 - Tests de Base (5 min)
1. **Test de santé** (requête 1)
2. **Tous les utilisateurs** (requête 2)
3. **Tous les posts** (requête 3)

### Phase 2 - Authentification (5 min)
4. **Créer utilisateur** (requête 6)
5. **Se connecter** (requête 7)
6. **Configurer headers JWT**
7. **Mon profil** (requête 8)

### Phase 3 - Interactions (5 min)
8. **Créer post** (requête 9)
9. **Mon feed** (requête 10)
10. **Liker/Commenter** (requêtes 11-12)

### Phase 4 - Interface Admin (5 min)
11. **Aller sur** http://localhost:8000/admin/
12. **Login** : admin / admin123
13. **Explorer** les données

---

## 🎊 RÉSULTAT ATTENDU

Si toutes ces requêtes fonctionnent → **Votre projet ALX est parfait ! 🌟**

Vous avez démontré :
- ✅ **API GraphQL complète**
- ✅ **Authentification JWT**
- ✅ **Gestion des utilisateurs**
- ✅ **Système de posts**
- ✅ **Interactions sociales**
- ✅ **Interface d'administration**

**Prêt pour une excellente note ALX ! 🚀**
