# 🚀 Guide de Déploiement Production - ALX Project Nexus

## 📋 **PLATEFORMES DE DÉPLOIEMENT RECOMMANDÉES**

### **🆓 Options Gratuites pour ALX :**

#### **1. Railway (Recommandé)**
- **URL :** https://railway.app/
- **Avantages :** Déploiement automatique, PostgreSQL inclus, SSL gratuit
- **Limite :** 500h/mois gratuit
- **Parfait pour :** Démonstration ALX

#### **2. Render**
- **URL :** https://render.com/
- **Avantages :** Déploiement Git, base de données gratuite
- **Limite :** Hibernation après 15min d'inactivité
- **Parfait pour :** Projets étudiants

#### **3. Heroku (Alternative)**
- **URL :** https://heroku.com/
- **Avantages :** Très populaire, documentation extensive
- **Limite :** Dynos gratuits limités
- **Note :** Plus complexe à configurer

---

## 🛠️ **PRÉPARATION POUR LE DÉPLOIEMENT**

### **✅ Fichiers Nécessaires :**

#### **1. requirements.txt (Production)**
```txt
Django==4.2.7
djangorestframework==3.14.0
django-graphene==3.0.0
graphene-django==3.0.0
django-cors-headers==4.3.1
django-filter==23.3
psycopg2-binary==2.9.7
redis==5.0.1
celery==5.3.4
django-celery-beat==2.5.0
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
django-extensions==3.2.3
drf-spectacular==0.26.5
Pillow==10.1.0
```

#### **2. Procfile (Pour Heroku/Railway)**
```
web: gunicorn social_media_backend.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A social_media_backend worker --loglevel=info
beat: celery -A social_media_backend beat --loglevel=info
```

#### **3. runtime.txt**
```
python-3.11.6
```

#### **4. .env.production (Template)**
```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Django
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Redis/Celery
REDIS_URL=redis://user:password@host:port/0

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
```

---

## 🚀 **DÉPLOIEMENT SUR RAILWAY (RECOMMANDÉ)**

### **📋 Étapes Détaillées :**

#### **1. Préparation du Code**
```bash
# Créer les fichiers de déploiement
echo "web: gunicorn social_media_backend.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile
echo "python-3.11.6" > runtime.txt

# Commit les changements
git add .
git commit -m "Add production deployment files"
git push origin feature/deployment-production
```

#### **2. Configuration Railway**
1. **Créer un compte :** https://railway.app/
2. **Nouveau projet :** "Deploy from GitHub repo"
3. **Sélectionner :** ton repo ALX Project Nexus
4. **Branch :** feature/deployment-production

#### **3. Variables d'Environnement**
```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DATABASE_URL=postgresql://... (auto-généré)
REDIS_URL=redis://... (auto-généré)
```

#### **4. Services à Ajouter**
- **PostgreSQL :** Base de données principale
- **Redis :** Cache et broker Celery
- **Web Service :** Application Django
- **Worker Service :** Celery worker (optionnel)

---

## 🔧 **CONFIGURATION PRODUCTION**

### **📁 settings/production.py**
```python
from .base import *
import dj_database_url
from decouple import config

# Security
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security headers
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
]

# Celery
CELERY_BROKER_URL = config('REDIS_URL')
CELERY_RESULT_BACKEND = config('REDIS_URL')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

## 📊 **CHECKLIST DÉPLOIEMENT**

### **✅ Avant le Déploiement :**
- [ ] Tests locaux passent
- [ ] Docker fonctionne localement
- [ ] Variables d'environnement configurées
- [ ] Base de données migrée
- [ ] Fichiers statiques collectés
- [ ] SSL/HTTPS configuré

### **✅ Après le Déploiement :**
- [ ] Application accessible
- [ ] GraphQL endpoint fonctionne
- [ ] Admin dashboard accessible
- [ ] API documentation visible
- [ ] Base de données connectée
- [ ] Celery worker actif (si configuré)

---

## 🎯 **URLS POUR ALX SUBMISSION**

### **📋 Liens à Fournir :**
```
🌐 Application Live: https://your-app.railway.app/
📊 GraphQL API: https://your-app.railway.app/graphql/
📚 API Docs: https://your-app.railway.app/api/docs/
🔧 Admin: https://your-app.railway.app/admin/
📖 GitHub Repo: https://github.com/your-username/alx-project-nexus
```

---

## 🚨 **DÉPANNAGE COURANT**

### **❌ Problèmes Fréquents :**

#### **1. Erreur 500 - Internal Server Error**
```bash
# Vérifier les logs
railway logs

# Solutions courantes:
- Vérifier SECRET_KEY
- Vérifier DATABASE_URL
- Vérifier ALLOWED_HOSTS
```

#### **2. Static Files Non Chargés**
```python
# Dans settings/production.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Dans requirements.txt
whitenoise==6.6.0
```

#### **3. Database Connection Error**
```bash
# Vérifier la variable DATABASE_URL
echo $DATABASE_URL

# Migrer la base de données
python manage.py migrate --settings=social_media_backend.settings.production
```

---

## 🎊 **DÉPLOIEMENT RÉUSSI !**

### **✅ Une fois déployé, tu auras :**
- **Application live** accessible 24/7
- **URL publique** pour la soumission ALX
- **Base de données** PostgreSQL en production
- **API GraphQL** fonctionnelle
- **Documentation** accessible en ligne
- **Interface admin** pour la démonstration

### **🏆 Pour ALX, tu pourras dire :**
- *"Application deployed on Railway with PostgreSQL"*
- *"Live GraphQL API accessible at [URL]"*
- *"Production-ready with SSL and security headers"*
- *"Scalable architecture with Docker support"*

---

**🚀 PRÊT POUR LE DÉPLOIEMENT PRODUCTION !**
