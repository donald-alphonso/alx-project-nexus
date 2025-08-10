# 🔧 RAILWAY VARIABLES SETUP - ACTION IMMÉDIATE

## 🚨 PROBLÈME IDENTIFIÉ
Les variables Railway ne sont pas propagées au service web.

## ✅ SOLUTION ÉTAPE PAR ÉTAPE

### 1. RÉCUPÉRER DATABASE_URL
1. **Clique sur le service PostgreSQL** (pas web)
2. **Onglet "Connect"**
3. **Copie** la `DATABASE_URL` complète
   - Format : `postgresql://postgres:password@host:port/database`

### 2. AJOUTER MANUELLEMENT AU SERVICE WEB
1. **Clique sur le service web**
2. **Onglet "Variables"**
3. **+ New Variable**
4. **Nom** : `DATABASE_URL`
5. **Valeur** : Colle l'URL PostgreSQL
6. **Save**

### 3. AJOUTER REDIS_URL (MÊME PROCESSUS)
1. **Clique sur le service Redis**
2. **Onglet "Connect"**
3. **Copie** la `REDIS_URL`
4. **Ajoute** au service web

### 4. VARIABLES OBLIGATOIRES À AJOUTER
```
SECRET_KEY=django-insecure-alx-project-nexus-2025-change-this-in-real-production
DEBUG=False
DJANGO_SETTINGS_MODULE=social_media_backend.settings.production
ALLOWED_HOSTS=*.railway.app
```

### 5. FORCER REDÉPLOIEMENT
- **Settings** → **Redeploy**
- Ou attendre que le nouveau push se déploie

## 🎯 RÉSULTAT ATTENDU
Une fois les variables ajoutées, tu devrais voir dans les logs :
```
DATABASE_URL: postgresql://postgres:...
REDIS_URL: redis://default:...
```

## ⚠️ IMPORTANT
Les variables doivent être dans le **SERVICE WEB**, pas dans PostgreSQL ou Redis.
