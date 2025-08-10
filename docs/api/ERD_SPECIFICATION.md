# 📊 ERD (Entity Relationship Diagram) Specification
## Social Media Backend - ALX Project Nexus

### 🎯 **Instructions pour créer l'ERD**

**Outils recommandés :**
- **Lucidchart** : https://lucidchart.com (Recommandé)
- **Draw.io** : https://draw.io (Gratuit)
- **dbdiagram.io** : https://dbdiagram.io (Spécialisé pour les bases de données)

---

## 📋 **ENTITÉS (TABLES) À CRÉER**

### 1. **👤 USER (users)**
**Champs principaux :**
- `id` (PK) - Integer, Auto-increment
- `username` - VARCHAR(150), Unique
- `email` - VARCHAR(254), Unique
- `first_name` - VARCHAR(150)
- `last_name` - VARCHAR(150)
- `bio` - TEXT(500)
- `avatar` - VARCHAR(100) (Image path)
- `birth_date` - DATE
- `location` - VARCHAR(100)
- `website` - URL
- `is_verified` - BOOLEAN
- `followers_count` - INTEGER
- `following_count` - INTEGER
- `posts_count` - INTEGER
- `created_at` - DATETIME
- `updated_at` - DATETIME

### 2. **👥 FOLLOW (follows)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `follower_id` (FK) → User.id
- `following_id` (FK) → User.id
- `created_at` - DATETIME

**Contrainte :** UNIQUE(follower_id, following_id)

### 3. **📝 POST (posts)**
**Champs principaux :**
- `id` (PK) - Integer, Auto-increment
- `author_id` (FK) → User.id
- `content` - TEXT(2200)
- `image` - VARCHAR(100) (Image path)
- `video` - VARCHAR(100) (Video path)
- `visibility` - VARCHAR(10) ['public', 'followers', 'private']
- `is_pinned` - BOOLEAN
- `likes_count` - INTEGER
- `comments_count` - INTEGER
- `shares_count` - INTEGER
- `views_count` - INTEGER
- `created_at` - DATETIME
- `updated_at` - DATETIME

### 4. **💬 COMMENT (comments)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `post_id` (FK) → Post.id
- `author_id` (FK) → User.id
- `parent_id` (FK) → Comment.id (Self-reference for replies)
- `content` - TEXT(1000)
- `likes_count` - INTEGER
- `created_at` - DATETIME
- `updated_at` - DATETIME

### 5. **🏷️ HASHTAG (hashtags)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `name` - VARCHAR(100), Unique
- `posts_count` - INTEGER
- `created_at` - DATETIME

### 6. **🔗 POST_HASHTAG (post_hashtags)**
**Table de liaison Many-to-Many**
- `id` (PK) - Integer, Auto-increment
- `post_id` (FK) → Post.id
- `hashtag_id` (FK) → Hashtag.id
- `created_at` - DATETIME

**Contrainte :** UNIQUE(post_id, hashtag_id)

### 7. **❤️ LIKE (likes)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `user_id` (FK) → User.id
- `content_type_id` (FK) → ContentType.id (Generic FK)
- `object_id` - INTEGER (Generic FK)
- `created_at` - DATETIME

**Contrainte :** UNIQUE(user_id, content_type_id, object_id)

### 8. **🔄 SHARE (shares)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `user_id` (FK) → User.id
- `post_id` (FK) → Post.id
- `share_type` - VARCHAR(10) ['repost', 'quote', 'share']
- `comment` - TEXT(500)
- `created_at` - DATETIME

**Contrainte :** UNIQUE(user_id, post_id)

### 9. **🔖 BOOKMARK (bookmarks)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `user_id` (FK) → User.id
- `post_id` (FK) → Post.id
- `created_at` - DATETIME

**Contrainte :** UNIQUE(user_id, post_id)

### 10. **🔔 NOTIFICATION (notifications)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `recipient_id` (FK) → User.id
- `sender_id` (FK) → User.id
- `notification_type` - VARCHAR(10) ['like', 'comment', 'share', 'follow', 'mention', 'reply']
- `message` - TEXT(255)
- `is_read` - BOOLEAN
- `content_type_id` (FK) → ContentType.id (Generic FK)
- `object_id` - INTEGER (Generic FK)
- `created_at` - DATETIME

### 11. **🚨 REPORT (reports)**
**Champs :**
- `id` (PK) - Integer, Auto-increment
- `reporter_id` (FK) → User.id
- `reason` - VARCHAR(15) ['spam', 'harassment', 'hate_speech', 'violence', 'inappropriate', 'copyright', 'other']
- `description` - TEXT(1000)
- `status` - VARCHAR(10) ['pending', 'reviewed', 'resolved', 'dismissed']
- `content_type_id` (FK) → ContentType.id (Generic FK)
- `object_id` - INTEGER (Generic FK)
- `created_at` - DATETIME
- `updated_at` - DATETIME

---

## 🔗 **RELATIONS À DESSINER**

### **Relations One-to-Many (1:N)**
1. **User** → **Post** (1:N)
   - Un utilisateur peut avoir plusieurs posts
   - `User.id` ← `Post.author_id`

2. **User** → **Comment** (1:N)
   - Un utilisateur peut avoir plusieurs commentaires
   - `User.id` ← `Comment.author_id`

3. **Post** → **Comment** (1:N)
   - Un post peut avoir plusieurs commentaires
   - `Post.id` ← `Comment.post_id`

4. **Comment** → **Comment** (1:N - Self-reference)
   - Un commentaire peut avoir des réponses
   - `Comment.id` ← `Comment.parent_id`

5. **User** → **Share** (1:N)
   - Un utilisateur peut partager plusieurs posts
   - `User.id` ← `Share.user_id`

6. **Post** → **Share** (1:N)
   - Un post peut être partagé plusieurs fois
   - `Post.id` ← `Share.post_id`

7. **User** → **Bookmark** (1:N)
   - Un utilisateur peut sauvegarder plusieurs posts
   - `User.id` ← `Bookmark.user_id`

8. **Post** → **Bookmark** (1:N)
   - Un post peut être sauvegardé par plusieurs utilisateurs
   - `Post.id` ← `Bookmark.post_id`

9. **User** → **Notification** (1:N) - Recipient
   - Un utilisateur peut recevoir plusieurs notifications
   - `User.id` ← `Notification.recipient_id`

10. **User** → **Notification** (1:N) - Sender
    - Un utilisateur peut envoyer plusieurs notifications
    - `User.id` ← `Notification.sender_id`

11. **User** → **Report** (1:N)
    - Un utilisateur peut faire plusieurs signalements
    - `User.id` ← `Report.reporter_id`

### **Relations Many-to-Many (M:N)**
1. **User** ↔ **User** (Follow relationship)
   - Via la table **Follow**
   - `User.id` ← `Follow.follower_id`
   - `User.id` ← `Follow.following_id`

2. **Post** ↔ **Hashtag**
   - Via la table **PostHashtag**
   - `Post.id` ← `PostHashtag.post_id`
   - `Hashtag.id` ← `PostHashtag.hashtag_id`

### **Relations Polymorphes (Generic Foreign Keys)**
1. **Like** → **Post/Comment**
   - Via `content_type_id` + `object_id`
   - Peut pointer vers Post ou Comment

2. **Notification** → **Post/Comment/User**
   - Via `content_type_id` + `object_id`
   - Peut pointer vers différents objets

3. **Report** → **Post/Comment**
   - Via `content_type_id` + `object_id`
   - Peut signaler Post ou Comment

---

## 🎨 **CONSEILS POUR LE DESIGN ERD**

### **Couleurs suggérées :**
- **User/Auth** : Bleu (#3498db)
- **Content (Post/Comment)** : Vert (#2ecc71)
- **Interactions (Like/Share/Bookmark)** : Orange (#f39c12)
- **System (Notification/Report)** : Rouge (#e74c3c)
- **Metadata (Hashtag)** : Violet (#9b59b6)

### **Légende :**
- **PK** = Primary Key (Clé primaire)
- **FK** = Foreign Key (Clé étrangère)
- **1:N** = One-to-Many (Un vers plusieurs)
- **M:N** = Many-to-Many (Plusieurs vers plusieurs)

### **Disposition recommandée :**
```
[User] ← Centre du diagramme
   ↓
[Follow] [Post] [Comment] [Like] [Share] [Bookmark]
   ↓       ↓
[Hashtag] [PostHashtag]
   ↓
[Notification] [Report]
```

---

## 📝 **ÉTAPES DE CRÉATION**

1. **Créer les entités** (rectangles) avec leurs champs
2. **Ajouter les clés primaires** (PK) en gras
3. **Dessiner les relations** avec des lignes
4. **Ajouter les cardinalités** (1:N, M:N)
5. **Colorer selon les groupes fonctionnels**
6. **Ajouter une légende**
7. **Exporter en PNG/PDF**

---

## 🔗 **LIENS UTILES**

- **Lucidchart Tutorial** : https://www.lucidchart.com/pages/er-diagrams
- **Draw.io Templates** : https://app.diagrams.net/?libs=er
- **ERD Best Practices** : https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/

---

**Une fois l'ERD créé, ajoutez le lien dans un Google Doc et partagez-le pour la présentation ALX !** 🎯
