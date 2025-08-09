# 🌐 Guide de Test Navigateur - ALX Project Nexus

## 🎯 Objectif
Tester toutes les fonctionnalités du projet depuis votre navigateur web, de l'authentification aux interactions sociales.

## 🚀 Étape 1 : Démarrage du Projet

```bash
# Dans le dossier du projet
docker-compose up -d

# Attendre 30 secondes pour que tout démarre
```

## 🔍 Étape 2 : Vérification des Accès

Ouvrez votre navigateur et testez ces URLs dans l'ordre :

### 2.1 Test de Base
- **GraphQL Interface** : http://localhost:8000/graphql/
  - ✅ Devrait afficher l'interface GraphQL interactive
  - ✅ Vous devriez voir un éditeur de requêtes

### 2.2 Interface d'Administration
- **Admin Django** : http://localhost:8000/admin/
  - ✅ Devrait afficher la page de connexion admin
  - 🔑 Identifiants : `admin` / `admin123`

### 2.3 Interface Swagger (si disponible)
- **Swagger UI** : http://localhost:8000/api/docs/
- **API Health** : http://localhost:8000/api/health/

## 🧪 Étape 3 : Tests via GraphQL

### 3.1 Connexion à GraphQL
1. Allez sur http://localhost:8000/graphql/
2. Vous devriez voir l'interface GraphiQL

### 3.2 Test 1 : Créer un Utilisateur
```graphql
mutation {
  createUser(
    username: "testuser"
    email: "test@example.com"
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
    message
  }
}
```

### 3.3 Test 2 : Connexion Utilisateur
```graphql
mutation {
  tokenAuth(username: "testuser", password: "motdepasse123") {
    token
    user {
      id
      username
    }
    success
  }
}
```

### 3.4 Test 3 : Créer un Post
```graphql
mutation {
  createPost(content: "Mon premier post de test !") {
    post {
      id
      content
      author {
        username
      }
      createdAt
    }
    success
    message
  }
}
```

### 3.5 Test 4 : Lister les Posts
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
        commentsCount
      }
}
```

### 3.6 Test 5 : Liker un Post
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
    message
  }
}
```

### 3.7 Test 6 : Commenter un Post
```graphql
mutation {
  createComment(postId: 1, content: "Super post !") {
    comment {
      id
      content
      author {
        username
      }
      post {
        id
      }
    }
    success
  }
}
```

### 3.8 Test 7 : Suivre un Utilisateur
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
    message
  }
}
```

### 3.9 Test 8 : Feed Personnalisé
```graphql
query {
  userFeed {
    edges {
      node {
        id
        content
        author {
          username
        }
        createdAt
        likesCount
      }
    }
  }
}
```

## 📊 Étape 4 : Tests d'Administration

### 4.1 Connexion Admin
1. Allez sur http://localhost:8000/admin/
2. Connectez-vous avec `admin` / `admin123`

### 4.2 Vérifications Admin
- ✅ **Users** : Voir la liste des utilisateurs
- ✅ **Posts** : Voir la liste des posts
- ✅ **Comments** : Voir les commentaires
- ✅ **Likes** : Voir les likes
- ✅ **Follows** : Voir les relations de suivi

## 🎯 Étape 5 : Checklist de Fonctionnalités

Cochez chaque fonctionnalité testée :

### Authentification
- [ ] Création d'utilisateur
- [ ] Connexion utilisateur
- [ ] Interface admin accessible

### Posts
- [ ] Création de post
- [ ] Affichage des posts
- [ ] Compteur de likes
- [ ] Compteur de commentaires

### Interactions
- [ ] Liker un post
- [ ] Commenter un post
- [ ] Suivre un utilisateur

### Feed
- [ ] Feed personnalisé
- [ ] Tri chronologique
- [ ] Affichage des informations complètes

### Administration
- [ ] Interface admin fonctionnelle
- [ ] Gestion des utilisateurs
- [ ] Gestion des contenus

## 🚨 En Cas de Problème

### Problème : GraphQL ne se charge pas
```bash
# Vérifier les logs
docker-compose logs web

# Redémarrer
docker-compose restart web
```

### Problème : Erreur de base de données
```bash
# Recréer la base
docker-compose down
docker-compose up -d
```

### Problème : Port occupé
```bash
# Vérifier les processus
netstat -ano | findstr :8000

# Changer de port si nécessaire
# Modifier docker-compose.yml : "8001:8000"
```

## 🎊 Validation Finale

Si tous les tests passent :
- ✅ **Votre projet ALX est fonctionnel !**
- ✅ **Toutes les fonctionnalités sociales marchent**
- ✅ **Prêt pour la présentation**

## 📝 Notes pour la Présentation

- **GraphQL** : Interface moderne et flexible
- **Admin Django** : Gestion complète des données
- **Architecture Docker** : Déploiement facile
- **Base PostgreSQL** : Robuste et scalable
- **Celery** : Tâches asynchrones
- **Redis** : Cache et broker de messages

---

**🎯 Objectif atteint : Projet social media backend complet et testable !**
