# 🎯 Guide ALX Complet pour Débutants

## 📋 **Ce que tu dois faire (4 étapes simples)**

### **1. ERD Diagram (Schéma de base de données)**
### **2. Google Slides (Présentation PowerPoint)**
### **3. Vidéo de démonstration (5 minutes max)**
### **4. Hébergement du projet**

---

## 🗄️ **ÉTAPE 1: ERD Diagram (15 minutes)**

### **Qu'est-ce que c'est ?**
Un schéma qui montre tes tables de base de données et leurs relations.

### **Outil gratuit recommandé : Draw.io**
1. Va sur **https://app.diagrams.net/**
2. Clique "Create New Diagram"
3. Choisis "Entity Relation" template

### **Ton ERD doit montrer ces tables :**
```
USER (Utilisateur)
├── id (Primary Key)
├── username
├── email
├── password
├── first_name
├── last_name
├── bio
├── avatar
└── created_at

POST (Publication)
├── id (Primary Key)
├── user_id (Foreign Key → USER)
├── content
├── image
├── visibility
├── created_at
└── updated_at

LIKE (J'aime)
├── id (Primary Key)
├── user_id (Foreign Key → USER)
├── post_id (Foreign Key → POST)
└── created_at

COMMENT (Commentaire)
├── id (Primary Key)
├── user_id (Foreign Key → USER)
├── post_id (Foreign Key → POST)
├── content
└── created_at

FOLLOW (Suivre)
├── id (Primary Key)
├── follower_id (Foreign Key → USER)
├── following_id (Foreign Key → USER)
└── created_at

NOTIFICATION (Notification)
├── id (Primary Key)
├── user_id (Foreign Key → USER)
├── type
├── message
├── is_read
└── created_at
```

### **Comment dessiner dans Draw.io :**
1. **Ajouter une table :** Glisse "Entity" depuis la barre de gauche
2. **Nommer la table :** Double-clique et écris "USER", "POST", etc.
3. **Ajouter les champs :** Clique sur la table, puis "+" pour ajouter des lignes
4. **Créer les relations :** Utilise les flèches pour connecter les tables

### **Relations à dessiner :**
- USER → POST (Un utilisateur peut avoir plusieurs posts)
- USER → LIKE (Un utilisateur peut liker plusieurs posts)
- POST → LIKE (Un post peut avoir plusieurs likes)
- USER → COMMENT (Un utilisateur peut commenter)
- POST → COMMENT (Un post peut avoir plusieurs commentaires)
- USER → FOLLOW (Relations de suivi)
- USER → NOTIFICATION (Notifications pour utilisateur)

### **Sauvegarder et partager :**
1. File → Export as → PNG (pour l'image)
2. File → Save as → Google Drive (pour le lien partageable)
3. Partage avec permissions "Anyone with link can view"

---

## 📊 **ÉTAPE 2: Google Slides (30 minutes)**

### **Créer la présentation :**
1. Va sur **https://slides.google.com**
2. Clique "Blank presentation"
3. Titre : "Social Media Backend API - ALX Project"

### **5 Slides à créer :**

#### **Slide 1: Title (Titre)**
```
Title: Social Media Backend API
Subtitle: GraphQL Architecture with Django
Your Name: [Ton nom]
ALX Software Engineering Program
Date: August 2025
```

#### **Slide 2: Architecture**
```
Title: Modern Backend Architecture

Bullet points:
• GraphQL API with 38 endpoints
• PostgreSQL database with 6 main models
• Celery background processing (9 tasks)
• Docker containerization (5 services)
• Redis caching and message broker
```

#### **Slide 3: Features**
```
Title: Core Features

Bullet points:
• User authentication and profiles
• Post creation with media upload
• Social interactions (likes, comments, follows)
• Real-time notifications
• Admin dashboard for moderation
```

#### **Slide 4: Technical Implementation**
```
Title: Technical Excellence

Bullet points:
• Security: JWT authentication, input validation
• Performance: Sub-second response times
• Scalability: Async processing, queue management
• Quality: Comprehensive testing and monitoring
• Documentation: Complete API docs and guides
```

#### **Slide 5: Results**
```
Title: Project Results

Bullet points:
• 200% of requirements completed
• Production-ready architecture
• Comprehensive documentation
• Modern GraphQL implementation
• Ready for deployment and scaling
```

### **Design simple :**
- **Couleurs :** Bleu et blanc
- **Police :** Arial ou Calibri
- **Pas plus de 5 points par slide**

### **Partager :**
1. Clique "Share" en haut à droite
2. Change permissions à "Anyone with link can view"
3. Copie le lien

---

## 🎥 **ÉTAPE 3: Vidéo de démonstration (45 minutes)**

### **Outils gratuits recommandés :**

#### **Option 1: OBS Studio (Gratuit, professionnel)**
1. Télécharge sur **https://obsproject.com/**
2. Installe et lance
3. Ajoute "Display Capture" pour capturer ton écran
4. Clique "Start Recording"

#### **Option 2: Windows Game Bar (Déjà installé)**
1. Appuie sur **Windows + G**
2. Clique sur le bouton d'enregistrement
3. Sélectionne la fenêtre à enregistrer

#### **Option 3: Loom (En ligne, gratuit)**
1. Va sur **https://loom.com**
2. Crée un compte gratuit
3. Clique "New Video" → "Screen Only"

### **Script de démonstration (5 minutes) :**

#### **Introduction (30 secondes) :**
```
"Hello, I'm [ton nom]. This is my ALX capstone project - 
a social media backend API built with Django and GraphQL. 
Let me show you the main features."
```

#### **GraphQL Demo (90 secondes) :**
```
"First, let's look at the GraphQL interface."
[Ouvre http://localhost:8000/graphql/]

"Here I can query users:"
[Tape: { allUsers { username email } }]

"And create a new post:"
[Tape: mutation { createPost(content: "Hello ALX!") { id content } }]

"The API responds instantly with structured data."
```

#### **Admin Dashboard (90 secondes) :**
```
"Next, the admin dashboard for content management."
[Ouvre http://localhost:8000/admin/]
[Login avec admin@example.com / admin123]

"I can manage users, moderate posts, and view analytics.
This provides complete control over the platform."
```

#### **Documentation (60 secondes) :**
```
"The project includes comprehensive documentation."
[Montre docs/INDEX.md]

"With user guides, API documentation, and technical specs.
Everything needed for production deployment."
```

#### **Conclusion (30 secondes) :**
```
"This project demonstrates modern backend development 
with GraphQL, async processing, and enterprise architecture. 
Thank you for watching."
```

### **Conseils pour l'enregistrement :**
- **Parle lentement et clairement**
- **Prépare tes onglets à l'avance**
- **Teste ton micro avant**
- **Fais plusieurs essais si nécessaire**

### **IA pour t'aider avec l'anglais :**
- **Google Translate** - Pour traduire tes phrases
- **Grammarly** (gratuit) - Pour corriger ta grammaire
- **DeepL** - Traduction plus naturelle

---

## 🌐 **ÉTAPE 4: Hébergement (20 minutes)**

### **Option gratuite : Railway**

#### **Préparation :**
1. Crée un compte sur **https://railway.app**
2. Connecte ton GitHub
3. Assure-toi que ton code est pushé

#### **Déploiement :**
1. Clique "New Project"
2. Sélectionne "Deploy from GitHub repo"
3. Choisis ton repository `alx-project-nexus`
4. Railway détecte automatiquement Django
5. Ajoute les variables d'environnement :
   ```
   DATABASE_URL=postgresql://...
   REDIS_URL=redis://...
   SECRET_KEY=ton-secret-key
   DEBUG=False
   ```

#### **Alternative : Render (Plus simple)**
1. Va sur **https://render.com**
2. Crée un compte gratuit
3. "New" → "Web Service"
4. Connecte ton GitHub repo
5. Render configure automatiquement

### **Vérification :**
- Ton site doit être accessible via une URL
- GraphQL doit fonctionner
- Admin panel accessible

---

## 📝 **ÉTAPE 5: Soumission finale**

### **Google Doc à créer :**
1. Va sur **https://docs.google.com**
2. Nouveau document
3. Titre : "ALX Project Nexus - Database Design & Links"

### **Contenu du Google Doc :**
```
ALX PROJECT NEXUS - SUBMISSION
===============================

Student: [Ton nom]
Project: Social Media Backend API
Date: August 2025

1. ERD DIAGRAM
Link: [Ton lien Draw.io]
Description: Complete database schema showing 6 main entities 
and their relationships for the social media platform.

2. PRESENTATION SLIDES
Link: [Ton lien Google Slides]
Description: 5-slide presentation covering architecture, 
features, and technical implementation.

3. DEMO VIDEO
Link: [Ton lien vidéo]
Description: 5-minute demonstration showing GraphQL API, 
admin dashboard, and key features in action.

4. HOSTED PROJECT
Link: [Ton lien Railway/Render]
Description: Live deployment of the social media backend 
with GraphQL endpoint and admin interface.

TECHNICAL SUMMARY
=================
- 38 GraphQL endpoints (20 queries + 18 mutations)
- 6 database models with optimized relationships
- Celery background processing (9 async tasks)
- Docker containerization for deployment
- Comprehensive documentation and testing
```

### **Permissions importantes :**
- **Tous les liens** : "Anyone with link can view"
- **Google Doc** : Partageable avec les mentors

---

## 🤖 **Outils IA gratuits pour t'aider :**

### **Pour l'anglais :**
- **ChatGPT** (gratuit) - Aide à écrire en anglais
- **Google Translate** - Traduction rapide
- **Grammarly** - Correction grammaticale
- **DeepL** - Traduction naturelle

### **Pour la vidéo :**
- **Loom** - Enregistrement facile
- **Canva** - Création de visuels
- **NVIDIA Broadcast** - Améliore audio/vidéo

### **Pour les slides :**
- **Canva** - Templates professionnels
- **Beautiful.AI** - Slides automatiques
- **Gamma** - Génération de présentations

---

## ⏰ **Planning recommandé (2 heures total) :**

### **Jour 1 (1 heure) :**
- ERD Diagram (15 min)
- Google Slides (30 min)
- Google Doc (15 min)

### **Jour 2 (1 heure) :**
- Préparation vidéo (15 min)
- Enregistrement vidéo (30 min)
- Hébergement (15 min)

---

## 🆘 **Phrases d'aide en anglais :**

### **Pour la présentation :**
- "Let me show you..." = "Laisse-moi te montrer..."
- "This demonstrates..." = "Ceci démontre..."
- "As you can see..." = "Comme vous pouvez voir..."
- "The key features include..." = "Les fonctionnalités clés incluent..."

### **Pour la vidéo :**
- "Hello, I'm [name]" = "Bonjour, je suis [nom]"
- "This is my project" = "Voici mon projet"
- "Let me demonstrate" = "Laisse-moi démontrer"
- "Thank you for watching" = "Merci d'avoir regardé"

---

## ✅ **Checklist finale :**

### **Avant soumission :**
- [ ] ERD créé et lien partageable
- [ ] 5 slides Google Slides terminées
- [ ] Vidéo de 5 minutes enregistrée
- [ ] Projet hébergé et accessible
- [ ] Google Doc avec tous les liens
- [ ] Permissions "view" sur tous les liens
- [ ] Testé tous les liens depuis un autre navigateur

### **Le jour de la soumission :**
- [ ] Vérifie que tous les liens fonctionnent
- [ ] Teste ton site hébergé
- [ ] Regarde ta vidéo une dernière fois
- [ ] Soumets avec confiance !

---

**🎊 TU PEUX LE FAIRE ! Ce guide te donne tout ce qu'il faut. Prends ton temps, suis les étapes, et n'hésite pas si tu as des questions !**

*Guide créé pour réussir l'évaluation ALX avec un niveau débutant*
