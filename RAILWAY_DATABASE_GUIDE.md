# 🗄️ Comment Ajouter PostgreSQL sur Railway

## 🎯 **ÉTAPES SIMPLES (5 minutes)**

### **1. Dans ton projet Railway :**
- Tu vois ton service Django qui se déploie
- À côté, il y a un bouton **"New Service"** ou **"+"**

### **2. Ajouter PostgreSQL :**
1. **Clique** sur **"New Service"** (bouton + ou Add Service)
2. **Sélectionne** : **"Database"**
3. **Choisis** : **"PostgreSQL"**
4. **Clique** : **"Add PostgreSQL"**

### **3. Railway va automatiquement :**
- ✅ Créer une base de données PostgreSQL
- ✅ Générer une `DATABASE_URL`
- ✅ La connecter à ton projet

### **4. Récupérer l'URL de la base :**
1. **Clique** sur le service **PostgreSQL** (nouveau bloc créé)
2. **Onglet** : **"Variables"**
3. **Tu vois** : `DATABASE_URL=postgresql://...`
4. **Cette URL est automatiquement disponible** pour ton app Django

### **5. Pareil pour Redis :**
1. **"New Service"** → **"Database"** → **"Redis"**
2. Railway génère automatiquement `REDIS_URL`

## 🔗 **CONNEXION AUTOMATIQUE**

### **✅ Railway fait tout automatiquement :**
- Les services sont **connectés entre eux**
- Ton Django **voit automatiquement** `DATABASE_URL` et `REDIS_URL`
- **Pas besoin de configuration manuelle**

### **📋 Dans ton service Django, tu verras :**
```
Variables d'environnement :
├── DATABASE_URL (auto-généré par PostgreSQL)
├── REDIS_URL (auto-généré par Redis)  
├── SECRET_KEY (que tu ajoutes)
├── DEBUG=False (que tu ajoutes)
└── ALLOWED_HOSTS=*.railway.app (que tu ajoutes)
```

## 🎯 **ORDRE RECOMMANDÉ :**

### **1. Créer le projet Django** ✅ (déjà fait)
### **2. Ajouter PostgreSQL** ← **TU ES ICI**
### **3. Ajouter Redis**
### **4. Configurer les variables**
### **5. Déployer**

## 📸 **À QUOI ÇA RESSEMBLE :**

```
Ton Projet Railway :
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Django App    │  │   PostgreSQL    │  │     Redis       │
│   (ton code)    │  │   (database)    │  │   (cache)       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
        ↑                      ↑                      ↑
        └──────────────────────┴──────────────────────┘
                    Connectés automatiquement
```

## 🆘 **SI TU NE VOIS PAS "NEW SERVICE" :**

### **Option 1 :** Bouton "+" en haut à droite
### **Option 2 :** Menu "Add Service" 
### **Option 3 :** Clique dans l'espace vide du projet

## ✅ **RÉSULTAT FINAL :**
- 3 services dans ton projet Railway
- Base de données PostgreSQL connectée
- Cache Redis connecté  
- Tout fonctionne ensemble automatiquement

---

**🎯 PROCHAINE ÉTAPE : Une fois PostgreSQL ajouté, configure tes variables d'environnement !**
