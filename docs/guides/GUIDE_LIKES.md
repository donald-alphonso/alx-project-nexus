# 👍 GUIDE COMPLET - Comment Faire des LIKES

## 🎯 PRÉREQUIS

Avant de faire des likes, vous devez :

1. **Avoir un token JWT valide** (utilisez `GENERER_TOKEN_FRAIS.py`)
2. **Connaître l'ID d'un post** à liker
3. **Être connecté** avec vos headers d'authentification

---

## 🔍 ÉTAPE 1 : Trouver un Post à Liker

### Voir tous les posts disponibles :
```graphql
query {
  allPosts {
    id
    content
    author {
      username
    }
    likesCount
    createdAt
  }
}
```

**✅ Résultat :** Liste des posts avec leurs IDs

**📝 Notez l'ID du post** que vous voulez liker (ex: `id: "1"`)

---

## 👍 ÉTAPE 2 : Faire un Like

### Mutation pour liker un post :
```graphql
mutation {
  likePost(postId: 1) {
    like {
      id
      user {
        username
      }
      createdAt
    }
    success
    errors
  }
}
```

**⚠️ IMPORTANT :** Remplacez `postId: 1` par l'ID réel du post !

**✅ Résultat attendu :**
```json
{
  "data": {
    "likePost": {
      "like": {
        "id": "123",
        "user": {
          "username": "votre_username"
        },
        "createdAt": "2025-01-09T15:57:00Z"
      },
      "success": true,
      "errors": []
    }
  }
}
```

---

## 🔄 ÉTAPE 3 : Vérifier le Like

### Voir le post avec le nouveau like :
```graphql
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
```

**✅ Le `likesCount` du post doit avoir augmenté de 1 !**

---

## 🚀 EXEMPLE COMPLET ÉTAPE PAR ÉTAPE

### 1. Configurer l'authentification
Dans GraphQL, cliquer "HTTP Headers" et ajouter :
```json
{"Authorization": "JWT VOTRE_TOKEN_ICI"}
```

### 2. Créer un post à liker
```graphql
mutation {
  createPost(content: "Post à liker ! 👍") {
    post {
      id
      content
      likesCount
    }
    success
  }
}
```
**→ Notez l'ID retourné (ex: `"id": "85"`)**

### 3. Liker ce post
```graphql
mutation {
  likePost(postId: 85) {
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
```
**→ Remplacez `85` par l'ID réel !**

### 4. Vérifier le résultat
```graphql
query {
  allPosts {
    id
    content
    likesCount
  }
}
```
**→ Le post doit maintenant avoir `likesCount: 1` !**

---

## 🔧 DÉPANNAGE

### ❌ Erreur "Post not found"
- **Cause :** L'ID du post n'existe pas
- **Solution :** Vérifiez l'ID avec la query `allPosts`

### ❌ Erreur "Error decoding signature"
- **Cause :** Token JWT invalide ou expiré
- **Solution :** Générez un nouveau token avec `GENERER_TOKEN_FRAIS.py`

### ❌ Erreur "You do not have permission"
- **Cause :** Headers d'authentification manquants
- **Solution :** Vérifiez vos headers HTTP

### ⚠️ Le like ne s'ajoute pas deux fois
- **Normal :** Un utilisateur ne peut liker qu'une fois le même post
- **Résultat :** `success: true` mais pas de nouveau like

---

## 🎯 REQUÊTES PRÊTES À COPIER-COLLER

### 👀 Voir les posts avec leurs likes :
```graphql
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
```

### 👍 Liker le post ID 1 :
```graphql
mutation {
  likePost(postId: 1) {
    like {
      id
      user {
        username
      }
      createdAt
    }
    success
    errors
  }
}
```

### 👍 Liker le post ID 2 :
```graphql
mutation {
  likePost(postId: 2) {
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
```

### 👍 Liker le post ID 3 :
```graphql
mutation {
  likePost(postId: 3) {
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
```

---

## 🎊 FONCTIONNALITÉS AVANCÉES

### 🔍 Voir tous les likes d'un utilisateur :
```graphql
query {
  me {
    username
    # Note: Cette query peut nécessiter une extension du schéma
  }
}
```

### 📊 Statistiques des likes :
```graphql
query {
  allPosts {
    id
    content
    likesCount
    author {
      username
    }
  }
}
```

---

## 🌟 RÉSUMÉ

**Pour faire un like :**

1. **Token JWT** configuré dans les headers ✅
2. **Trouver l'ID** du post avec `allPosts` ✅
3. **Utiliser** `likePost(postId: ID)` ✅
4. **Vérifier** que `likesCount` a augmenté ✅

**Votre système de likes fonctionne parfaitement ! 🎉**

---

## 🔗 LIENS UTILES

- **GraphQL Interface :** http://localhost:8000/graphql/
- **Admin Interface :** http://localhost:8000/admin/
- **Générer nouveau token :** `python GENERER_TOKEN_FRAIS.py`

**Bon test des likes ! 👍🚀**
