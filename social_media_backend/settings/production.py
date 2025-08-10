"""
Production settings for ALX Project Nexus
Optimized for Railway, Render, or Heroku deployment
"""

import os
from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'graphene_django',
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'django_celery_beat',
    
    # Local apps
    'social_media_backend.apps.SocialMediaBackendConfig',
    'users',
    'posts',
    'interactions',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Try to import dj_database_url, fallback to manual parsing
try:
    import dj_database_url
    HAS_DJ_DATABASE_URL = True
except ImportError:
    HAS_DJ_DATABASE_URL = False
    import urllib.parse as urlparse
    
    def parse_database_url(url):
        parsed = urlparse.urlparse(url)
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path[1:],
            'USER': parsed.username,
            'PASSWORD': parsed.password,
            'HOST': parsed.hostname,
            'PORT': parsed.port or 5432,
        }

# Security
DEBUG = False
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# ALLOWED_HOSTS - Accept all hosts for Railway deployment
ALLOWED_HOSTS = ['*']

# URL Configuration
ROOT_URLCONF = 'social_media_backend.urls'
WSGI_APPLICATION = 'social_media_backend.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database - PostgreSQL only
# Get DATABASE_URL with fallback for Railway
database_url = config('DATABASE_URL', default=None)

if not database_url:
    # Fallback: Try Railway's internal PostgreSQL connection
    database_url = config('PGDATABASE', default=None)
    if database_url:
        # Construct URL from Railway PostgreSQL variables
        pg_user = config('PGUSER', default='postgres')
        pg_password = config('PGPASSWORD', default='')
        pg_host = config('PGHOST', default='localhost')
        pg_port = config('PGPORT', default='5432')
        database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{database_url}"

if HAS_DJ_DATABASE_URL and database_url:
    DATABASES = {
        'default': dj_database_url.parse(database_url)
    }
elif database_url:
    DATABASES = {
        'default': parse_database_url(database_url)
    }
else:
    # Ultimate fallback - SQLite for testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000 if config('SECURE_SSL_REDIRECT', default=False, cast=bool) else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS settings
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# Redis/Celery configuration
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Cache configuration with fallback
redis_url = config('REDIS_URL', default=None)

if redis_url and HAS_DJ_DATABASE_URL:  # Si Redis disponible et django-redis installé
    try:
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': redis_url,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                }
            }
        }
    except Exception:
        # Fallback vers cache local
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }
else:
    # Cache local par défaut
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# Email configuration (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@alxprojectnexus.com')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'social_media_backend': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# GraphQL settings
GRAPHENE = {
    'SCHEMA': 'social_media_backend.schema.schema',
    'MIDDLEWARE': [
        'social_media_backend.middleware.graphql_middleware.GraphQLAuthMiddleware',
        'social_media_backend.middleware.graphql_middleware.GraphQLErrorMiddleware',
    ],
}

# DRF Spectacular settings for production
SPECTACULAR_SETTINGS = {
    'TITLE': 'ALX Project Nexus API',
    'DESCRIPTION': 'A comprehensive social media backend with GraphQL and REST APIs',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': '/api/',
    'SERVERS': [
        {
            'url': config('API_BASE_URL', default='https://your-app.railway.app'),
            'description': 'Production server'
        }
    ],
}

# Performance optimizations
CONN_MAX_AGE = 60

# Session configuration
SESSION_COOKIE_SECURE = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Additional security headers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

print("🚀 Production settings loaded successfully!")
print(f"📊 Debug mode: {DEBUG}")
print(f"🔒 SSL redirect: {SECURE_SSL_REDIRECT}")
print(f"🌐 Allowed hosts: {ALLOWED_HOSTS}")
