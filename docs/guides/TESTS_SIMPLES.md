# Tests Simples - ALX Project Nexus

## ETAPE 1: Demarrer le projet
```
docker-compose up -d
```

## ETAPE 2: Ouvrir le navigateur
Aller sur: http://localhost:8000/graphql/

## ETAPE 3: Creer un utilisateur
Copier-coller cette requete dans l'interface GraphQL:

```
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
    message
  }
}
```

## ETAPE 4: Se connecter
```
mutation {
  tokenAuth(username: "testuser1", password: "motdepasse123") {
    token
    user {
      id
      username
    }
    success
  }
}
```

IMPORTANT: Copier le token retourne!

## ETAPE 5: Configurer l'authentification
En bas de l'interface GraphQL, cliquer sur "HTTP Headers" et ajouter:
```
{
  "Authorization": "JWT VOTRE_TOKEN_ICI"
}
```

## ETAPE 6: Creer un post
```
mutation {
  createPost(content: "Mon premier post de test!") {
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

## ETAPE 7: Voir tous les posts
```
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

## ETAPE 8: Liker un post
```
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
    message
  }
}
```

## ETAPE 9: Commenter un post
```
mutation {
  createComment(postId: 1, content: "Super post!") {
    comment {
      id
      content
      author {
        username
      }
    }
    success
  }
}
```

## ETAPE 10: Tester l'admin
Aller sur: http://localhost:8000/admin/
Login: admin
Mot de passe: admin123

Verifier que vous voyez:
- Users
- Posts  
- Comments
- Likes

## RESULTAT ATTENDU
Si tous les tests passent, votre projet ALX est 100% fonctionnel!

## EN CAS DE PROBLEME
```
docker-compose logs web
docker-compose restart web
```

## INTERFACES PRINCIPALES
- GraphQL: http://localhost:8000/graphql/
- Admin: http://localhost:8000/admin/
- Accueil: http://localhost:8000/
