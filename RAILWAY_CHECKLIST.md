# 📋 Checklist Déploiement Railway - ALX Project Nexus

## ✅ AVANT DE COMMENCER
- [ ] Compte GitHub avec le projet ALX
- [ ] Branche `feature/deployment-production` active
- [ ] Tous les fichiers de déploiement présents
- [ ] 30 minutes de temps libre

## 🚀 ÉTAPES RAILWAY (Dans l'ordre)

### 1. Création du Compte
- [ ] Aller sur https://railway.app/
- [ ] S'inscrire avec GitHub
- [ ] Autoriser l'accès aux repos

### 2. Nouveau Projet
- [ ] "New Project" → "Deploy from GitHub repo"
- [ ] Sélectionner `alx-project-nexus`
- [ ] Branche: `feature/deployment-production`
- [ ] Cliquer "Deploy Now"

### 3. Ajouter PostgreSQL
- [ ] "New Service" → "Database" → "PostgreSQL"
- [ ] Copier `DATABASE_URL` depuis Variables

### 4. Ajouter Redis
- [ ] "New Service" → "Database" → "Redis"
- [ ] Copier `REDIS_URL` depuis Variables

### 5. Variables d'Environnement
- [ ] Service Django → Onglet "Variables"
- [ ] Ajouter toutes les variables du fichier `.env.railway`
- [ ] ⚠️ NE PAS ajouter DATABASE_URL et REDIS_URL (auto-générées)

### 6. Redéploiement
- [ ] Attendre le déploiement automatique
- [ ] Vérifier les logs (onglet "Logs")
- [ ] Pas d'erreurs critiques

### 7. Migrations
- [ ] Console → `python manage.py migrate --settings=social_media_backend.settings.production`
- [ ] Console → `python manage.py collectstatic --noinput --settings=social_media_backend.settings.production`

### 8. Superuser
- [ ] Console → `python manage.py shell --settings=social_media_backend.settings.production`
- [ ] Créer admin avec le script fourni

### 9. Tests Finaux
- [ ] https://ton-app.railway.app/ → Page d'accueil
- [ ] https://ton-app.railway.app/admin/ → Login admin/admin123
- [ ] https://ton-app.railway.app/graphql/ → Interface GraphQL
- [ ] https://ton-app.railway.app/api/docs/ → Documentation Swagger

## 🎯 URLS POUR ALX
```
Application: https://ton-app.railway.app/
GraphQL: https://ton-app.railway.app/graphql/
API Docs: https://ton-app.railway.app/api/docs/
Admin: https://ton-app.railway.app/admin/
GitHub: https://github.com/ton-username/alx-project-nexus
```

## 🆘 EN CAS DE PROBLÈME
1. Vérifier les logs Railway
2. Vérifier les variables d'environnement
3. Redémarrer le service
4. Consulter le guide complet: docs/deployment/RAILWAY_GUIDE_COMPLET.md

---
**Créé le 10/08/2025 à 17:16**
**🚀 Bon déploiement !**
