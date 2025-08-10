# 🗄️ Guide ERD - Étape par Étape (15 minutes)

## 🎯 **Objectif : Créer ton schéma de base de données**

Tu vas créer un diagramme qui montre tes 6 tables principales et leurs relations.

---

## 🚀 **ÉTAPE 1: Ouvrir Draw.io (2 minutes)**

### **Actions :**
1. Va sur **https://app.diagrams.net/**
2. Clique **"Create New Diagram"**
3. Choisis **"Entity Relation"** dans les templates
4. Clique **"Create"**
5. Nomme ton fichier : **"Social Media Backend ERD"**

---

## 📊 **ÉTAPE 2: Créer les 6 tables (8 minutes)**

### **Table 1: USER**
1. **Ajouter la table :** Glisse "Entity" depuis la barre de gauche
2. **Renommer :** Double-clique et écris **"USER"**
3. **Ajouter les champs :** Clique sur la table, puis "+" pour chaque ligne :
   ```
   🔑 id (PK)
   username
   email  
   password
   first_name
   last_name
   bio
   avatar
   created_at
   ```

### **Table 2: POST**
1. **Nouvelle entité :** Glisse une autre "Entity"
2. **Nom :** **"POST"**
3. **Champs :**
   ```
   🔑 id (PK)
   🔗 user_id (FK)
   content
   image
   visibility
   created_at
   updated_at
   ```

### **Table 3: LIKE**
1. **Nouvelle entité :** **"LIKE"**
2. **Champs :**
   ```
   🔑 id (PK)
   🔗 user_id (FK)
   🔗 post_id (FK)
   created_at
   ```

### **Table 4: COMMENT**
1. **Nouvelle entité :** **"COMMENT"**
2. **Champs :**
   ```
   🔑 id (PK)
   🔗 user_id (FK)
   🔗 post_id (FK)
   content
   created_at
   ```

### **Table 5: FOLLOW**
1. **Nouvelle entité :** **"FOLLOW"**
2. **Champs :**
   ```
   🔑 id (PK)
   🔗 follower_id (FK)
   🔗 following_id (FK)
   created_at
   ```

### **Table 6: NOTIFICATION**
1. **Nouvelle entité :** **"NOTIFICATION"**
2. **Champs :**
   ```
   🔑 id (PK)
   🔗 user_id (FK)
   type
   message
   is_read
   created_at
   ```

---

## 🔗 **ÉTAPE 3: Créer les relations (3 minutes)**

### **Comment faire une relation :**
1. Clique sur l'outil **"Connector"** (flèche) dans la barre d'outils
2. Clique sur la table source
3. Glisse vers la table destination
4. Relâche pour créer la relation

### **Relations à créer :**

#### **USER → POST (Un-à-Plusieurs)**
- De **USER.id** vers **POST.user_id**
- Type : **1:N** (Un utilisateur, plusieurs posts)

#### **USER → LIKE (Un-à-Plusieurs)**
- De **USER.id** vers **LIKE.user_id**
- Type : **1:N** (Un utilisateur, plusieurs likes)

#### **POST → LIKE (Un-à-Plusieurs)**
- De **POST.id** vers **LIKE.post_id**
- Type : **1:N** (Un post, plusieurs likes)

#### **USER → COMMENT (Un-à-Plusieurs)**
- De **USER.id** vers **COMMENT.user_id**
- Type : **1:N** (Un utilisateur, plusieurs commentaires)

#### **POST → COMMENT (Un-à-Plusieurs)**
- De **POST.id** vers **COMMENT.post_id**
- Type : **1:N** (Un post, plusieurs commentaires)

#### **USER → FOLLOW (Deux relations)**
- De **USER.id** vers **FOLLOW.follower_id**
- De **USER.id** vers **FOLLOW.following_id**
- Type : **1:N** pour chaque

#### **USER → NOTIFICATION (Un-à-Plusieurs)**
- De **USER.id** vers **NOTIFICATION.user_id**
- Type : **1:N** (Un utilisateur, plusieurs notifications)

---

## 🎨 **ÉTAPE 4: Améliorer l'apparence (2 minutes)**

### **Organiser les tables :**
1. **USER** au centre (table principale)
2. **POST** à droite de USER
3. **LIKE** et **COMMENT** en dessous de POST
4. **FOLLOW** à gauche de USER
5. **NOTIFICATION** en haut de USER

### **Couleurs recommandées :**
- **USER** : Bleu foncé (table principale)
- **POST** : Vert (contenu)
- **LIKE, COMMENT** : Orange (interactions)
- **FOLLOW** : Violet (relations sociales)
- **NOTIFICATION** : Rouge (alertes)

### **Pour changer les couleurs :**
1. Sélectionne une table
2. Clique sur l'icône de couleur dans la barre d'outils
3. Choisis ta couleur

---

## 💾 **ÉTAPE 5: Sauvegarder et partager**

### **Sauvegarder :**
1. **File** → **Save As**
2. Choisis **"Google Drive"**
3. Nomme : **"ALX Project Nexus - ERD"**
4. Sauvegarde

### **Exporter l'image :**
1. **File** → **Export as** → **PNG**
2. Résolution : **300 DPI**
3. Télécharge l'image

### **Créer le lien partageable :**
1. **File** → **Share**
2. Ou va dans ton Google Drive
3. Clique droit sur le fichier → **Share**
4. Change permissions : **"Anyone with the link can view"**
5. **Copie le lien** (tu en auras besoin pour la soumission)

---

## ✅ **Vérification finale**

### **Ton ERD doit avoir :**
- [ ] 6 tables bien nommées
- [ ] Tous les champs listés pour chaque table
- [ ] PK (Primary Key) marquées avec 🔑
- [ ] FK (Foreign Key) marquées avec 🔗
- [ ] 7 relations connectées avec des flèches
- [ ] Couleurs différentes pour chaque table
- [ ] Layout organisé et lisible

### **Test de qualité :**
- [ ] Quelqu'un peut comprendre ton schéma sans explication
- [ ] Les relations sont logiques
- [ ] Toutes les tables sont connectées
- [ ] L'image est claire et professionnelle

---

## 📝 **Description pour ton Google Doc**

**Copie-colle ce texte dans ton Google Doc :**

```
DATABASE DESIGN (ERD)
====================
Link: [TON LIEN DRAW.IO ICI]

Description:
Complete Entity Relationship Diagram for the social media backend system. 
The design includes 6 main entities with optimized relationships:

• USER - User authentication and profile management
• POST - Content creation and media handling
• LIKE - User engagement tracking  
• COMMENT - Discussion and interaction system
• FOLLOW - Social relationship management
• NOTIFICATION - Real-time user alerts

The schema implements proper normalization, foreign key relationships, 
and scalable design patterns suitable for a production social media platform.

Key Design Features:
- Normalized database structure
- Efficient relationship modeling
- Scalable for high user volumes
- Supports complex social interactions
- Optimized for GraphQL queries
```

---

## 🆘 **Si tu es bloqué**

### **Problème : Je ne trouve pas "Entity" dans Draw.io**
**Solution :** Cherche dans la barre de gauche, section "Entity Relation" ou "General"

### **Problème : Les relations ne se connectent pas**
**Solution :** 
1. Utilise l'outil "Connector" (flèche)
2. Clique exactement sur le bord de la table
3. Glisse vers le bord de l'autre table

### **Problème : Mon diagramme est moche**
**Solution :**
1. Sélectionne tout (Ctrl+A)
2. Va dans "Arrange" → "Layout" → "Hierarchical"
3. Ajuste manuellement après

### **Problème : Je ne peux pas partager**
**Solution :**
1. Sauvegarde d'abord dans Google Drive
2. Va dans Drive, trouve ton fichier
3. Clique droit → Share → Anyone with link

---

## ⏰ **Si tu manques de temps**

### **Version rapide (5 minutes) :**
1. **Crée juste 3 tables :** USER, POST, LIKE
2. **Relations simples :** USER→POST, USER→LIKE, POST→LIKE
3. **Pas de couleurs,** juste fonctionnel
4. **Sauvegarde et partage** rapidement

### **L'important c'est :**
- Que ça montre tes tables principales
- Que les relations soient logiques
- Que le lien soit partageable

---

**🎯 MAINTENANT, LANCE-TOI ! Ouvre Draw.io et commence. En 15 minutes, tu auras un ERD professionnel ! 💪**
