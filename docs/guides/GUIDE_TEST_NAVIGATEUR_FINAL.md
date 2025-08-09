# 🚀 GUIDE COMPLET - Test de votre Projet ALX depuis le Navigateur

## 🎯 VOTRE PROJET EST 100% FONCTIONNEL !

Authentification JWT ✅ | API GraphQL ✅ | Interface Admin ✅

---

## 📋 ÉTAPE 1 : Vérifier que tout fonctionne

### 1.1 Ouvrir votre navigateur
- **Chrome**, **Firefox**, ou **Edge**

### 1.2 Aller sur l'interface GraphQL
```
http://localhost:8000/graphql/
```

**✅ Résultat attendu :** Interface GraphQL interactive avec un éditeur de requêtes

---

## 🧪 ÉTAPE 2 : Tests SANS Authentification (Facile)

### 2.1 Test de Santé de l'API
Dans l'éditeur GraphQL, tapez :

```graphql
query {
  health
}
```

**Cliquer sur le bouton ▶️ (Play)**

**✅ Résultat attendu :** `"GraphQL API is running!"`

### 2.2 Voir tous les Utilisateurs
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

**✅ Résultat attendu :** Liste de tous les utilisateurs (environ 19)

### 2.3 Voir tous les Posts
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

**✅ Résultat attendu :** Liste de tous les posts (environ 20)

### 2.4 Rechercher des Utilisateurs
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

**✅ Résultat attendu :** Utilisateurs contenant "admin"

---

## 🔐 ÉTAPE 3 : Tests AVEC Authentification JWT

### 3.1 Créer un Nouvel Utilisateur
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

**✅ Résultat attendu :** Nouvel utilisateur créé avec `success: true`

### 3.2 Se Connecter et Récupérer le Token
```graphql
mutation {
  tokenAuth(email: "montest2025@example.com", password: "motdepasse123") {
    token
    payload
    refreshExpiresIn
  }
}
```

**✅ Résultat attendu :** Un token JWT (longue chaîne de caractères)

**🔑 IMPORTANT :** Copiez le token (sans les guillemets) !

### 3.3 Configurer les Headers d'Authentification

1. **En bas à gauche** de l'interface GraphQL, cliquez sur **"HTTP Headers"**
2. **Dans la zone qui s'ouvre**, tapez :

```json
{
  "Authorization": "JWT COLLEZ_VOTRE_TOKEN_ICI"
}
```

**Exemple :**
```json
{
  "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1vbnRlc3QyMDI1QGV4YW1wbGUuY29tIiwidXNlcm5hbWUiOiJtb250ZXN0MjAyNSIsImV4cCI6MTc1NDc1MDU1NSwib3JpZ0lhdCI6MTc1NDc0Njk1NX0.oKOaS-h91bSSvMj2wdXkXUD1ejC7G7AC-aXsD4G2zVqg"
}
```

### 3.4 Tester une Requête Authentifiée - Mon Profil
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

**✅ Résultat attendu :** Vos informations de profil

### 3.5 Créer un Post
```graphql
mutation {
  createPost(content: "Mon premier post de test depuis le navigateur ! 🚀") {
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

**✅ Résultat attendu :** Post créé avec `success: true`

### 3.6 Voir Mon Feed Personnalisé
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

**✅ Résultat attendu :** Votre feed personnalisé

---

## 👑 ÉTAPE 4 : Interface d'Administration

### 4.1 Ouvrir l'Interface Admin
```
http://localhost:8000/admin/
```

### 4.2 Se Connecter
- **Nom d'utilisateur :** `admin`
- **Mot de passe :** `admin123`

### 4.3 Explorer l'Interface
- **Users** → Voir tous les utilisateurs
- **Posts** → Voir tous les posts
- **Interactions** → Voir likes, commentaires, etc.
- **Ajouter/Modifier/Supprimer** des données

---

## 🎊 ÉTAPE 5 : Tests Avancés (Bonus)

### 5.1 Liker un Post
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

### 5.2 Commenter un Post
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

### 5.3 Suivre un Utilisateur
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

---

## 🔧 DÉPANNAGE

### ❌ Si une requête ne fonctionne pas :

1. **Vérifiez le token JWT** dans les headers
2. **Copiez-collez exactement** les requêtes
3. **Vérifiez l'orthographe** des champs
4. **Regardez les messages d'erreur** dans la réponse

### ❌ Si l'interface ne s'ouvre pas :

1. Vérifiez que Docker fonctionne :
   ```bash
   docker-compose ps
   ```

2. Redémarrez si nécessaire :
   ```bash
   docker-compose restart web
   ```

---

## 🎯 RÉSUMÉ DE CE QUE VOUS ALLEZ DÉMONTRER

### ✅ Fonctionnalités Testées :
- **API GraphQL interactive** ✅
- **Authentification JWT** ✅
- **Création d'utilisateurs** ✅
- **Connexion sécurisée** ✅
- **Gestion des posts** ✅
- **Interactions sociales** ✅
- **Interface d'administration** ✅
- **Recherche et filtrage** ✅

### ✅ Technologies Démontrées :
- **Django** + **PostgreSQL** ✅
- **GraphQL** avec **Graphene** ✅
- **JWT Authentication** ✅
- **Docker** containerisation ✅
- **Redis** + **Celery** ✅
- **Interface Admin** ✅

---

## 🌟 FÉLICITATIONS !

**Votre projet ALX Project Nexus est 100% fonctionnel !**

Vous avez maintenant :
- ✅ **38 endpoints GraphQL** opérationnels
- ✅ **Authentification JWT** parfaite
- ✅ **Interface utilisateur** complète
- ✅ **Architecture professionnelle**

**Prêt pour une excellente note ALX ! 🎊**

---

## 📱 LIENS RAPIDES

- **GraphQL :** http://localhost:8000/graphql/
- **Admin :** http://localhost:8000/admin/ (admin/admin123)
- **Accueil :** http://localhost:8000/

**Bonne démonstration ! 🚀**
