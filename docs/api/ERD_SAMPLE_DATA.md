# 📊 EXEMPLES DE DONNÉES POUR L'ERD
## Comprendre les relations avec des exemples concrets

---

## 👤 **EXEMPLE DE DONNÉES**

### **Table USER**
```
ID | Username | Email           | Bio                    | Followers | Following | Posts
1  | alice    | alice@mail.com  | "Love photography"     | 150       | 75        | 12
2  | bob      | bob@mail.com    | "Tech enthusiast"      | 89        | 120       | 8
3  | charlie  | charlie@mail.com| "Travel blogger"       | 200       | 95        | 25
```

### **Table FOLLOW**
```
ID | Follower_ID | Following_ID | Created_at
1  | 2           | 1            | 2025-01-01
2  | 3           | 1            | 2025-01-02
3  | 1           | 3            | 2025-01-03
```
**Signification :**
- Bob (ID:2) suit Alice (ID:1)
- Charlie (ID:3) suit Alice (ID:1)
- Alice (ID:1) suit Charlie (ID:3)

### **Table POST**
```
ID | Author_ID | Content                    | Visibility | Likes | Comments | Shares
1  | 1         | "Beautiful sunset today!"  | public     | 25    | 5        | 3
2  | 2         | "New tech trends in 2025"  | public     | 18    | 8        | 2
3  | 3         | "My trip to Paris #travel" | followers  | 45    | 12       | 7
```

### **Table HASHTAG**
```
ID | Name     | Posts_Count | Created_at
1  | travel   | 150         | 2025-01-01
2  | tech     | 89          | 2025-01-01
3  | photo    | 200         | 2025-01-01
```

### **Table POST_HASHTAG (Relation M:N)**
```
ID | Post_ID | Hashtag_ID | Created_at
1  | 1       | 3          | 2025-01-01  # Post "sunset" → #photo
2  | 2       | 2          | 2025-01-02  # Post "tech trends" → #tech
3  | 3       | 1          | 2025-01-03  # Post "Paris trip" → #travel
```

### **Table COMMENT**
```
ID | Post_ID | Author_ID | Parent_ID | Content              | Likes
1  | 1       | 2         | NULL      | "Amazing shot!"      | 5
2  | 1       | 3         | 1         | "I agree with Bob!"  | 2
3  | 2       | 1         | NULL      | "Great insights!"    | 3
```
**Signification :**
- Comment 1 : Bob commente le post d'Alice
- Comment 2 : Charlie répond au commentaire de Bob (parent_id = 1)
- Comment 3 : Alice commente le post de Bob

### **Table LIKE (Polymorphe)**
```
ID | User_ID | Content_Type | Object_ID | Created_at
1  | 2       | post         | 1         | 2025-01-01  # Bob like le post 1
2  | 3       | post         | 1         | 2025-01-01  # Charlie like le post 1
3  | 1       | comment      | 1         | 2025-01-02  # Alice like le comment 1
```

### **Table SHARE**
```
ID | User_ID | Post_ID | Share_Type | Comment           | Created_at
1  | 2       | 1       | repost     | NULL              | 2025-01-01
2  | 3       | 2       | quote      | "So true!"        | 2025-01-02
```

### **Table BOOKMARK**
```
ID | User_ID | Post_ID | Created_at
1  | 2       | 3       | 2025-01-01  # Bob sauvegarde le post de Charlie
2  | 1       | 2       | 2025-01-02  # Alice sauvegarde le post de Bob
```

### **Table NOTIFICATION**
```
ID | Recipient_ID | Sender_ID | Type    | Message                    | Is_Read | Object_ID
1  | 1            | 2         | like    | "Bob liked your post"      | false   | 1
2  | 1            | 3         | comment | "Charlie commented on..."  | false   | 1
3  | 2            | 1         | follow  | "Alice started following"  | true    | NULL
```

### **Table REPORT**
```
ID | Reporter_ID | Reason      | Description        | Status  | Object_ID | Content_Type
1  | 1           | spam        | "Promotional spam" | pending | 2         | post
2  | 2           | harassment  | "Offensive comment"| reviewed| 3         | comment
```

---

## 🔗 **RELATIONS EXPLIQUÉES**

### **1. User → Post (1:N)**
- Alice (ID:1) a créé le post "Beautiful sunset" (ID:1)
- Bob (ID:2) a créé le post "Tech trends" (ID:2)
- Un utilisateur peut avoir plusieurs posts

### **2. User ↔ User via Follow (M:N)**
- Bob suit Alice
- Charlie suit Alice
- Alice suit Charlie
- Relation bidirectionnelle via table Follow

### **3. Post ↔ Hashtag via PostHashtag (M:N)**
- Post "sunset" est lié à #photo
- Post "tech trends" est lié à #tech
- Un post peut avoir plusieurs hashtags, un hashtag peut être dans plusieurs posts

### **4. Comment → Comment (Self-reference)**
- Comment 2 répond au Comment 1 (parent_id = 1)
- Permet les fils de discussion

### **5. Like → Post/Comment (Polymorphe)**
- Like 1 et 2 pointent vers le Post 1
- Like 3 pointe vers le Comment 1
- Une seule table pour liker différents types d'objets

---

## 📈 **CARDINALITÉS**

```
User (1) ←→ (N) Post          # Un user, plusieurs posts
User (1) ←→ (N) Comment       # Un user, plusieurs comments
Post (1) ←→ (N) Comment       # Un post, plusieurs comments
User (M) ←→ (N) User          # Many-to-many via Follow
Post (M) ←→ (N) Hashtag       # Many-to-many via PostHashtag
User (1) ←→ (N) Like          # Un user, plusieurs likes
User (1) ←→ (N) Share         # Un user, plusieurs shares
User (1) ←→ (N) Bookmark      # Un user, plusieurs bookmarks
User (1) ←→ (N) Notification  # Un user, plusieurs notifications
User (1) ←→ (N) Report        # Un user, plusieurs reports
```

---

## 🎯 **POINTS CLÉS POUR L'ERD**

1. **Clés primaires** : Toujours ID auto-increment
2. **Clés étrangères** : Suffixe "_id" pour clarté
3. **Tables de liaison** : Pour relations M:N (Follow, PostHashtag)
4. **Relations polymorphes** : content_type_id + object_id
5. **Self-references** : parent_id dans Comment
6. **Contraintes uniques** : Éviter les doublons (user+post dans Like)

---

**Ces exemples vous aideront à comprendre comment dessiner les relations dans votre ERD !** 🎨
