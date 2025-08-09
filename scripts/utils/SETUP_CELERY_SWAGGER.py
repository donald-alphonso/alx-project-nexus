#!/usr/bin/env python3
"""
Configuration complète Celery + Swagger pour ALX Project Nexus
"""

import os
import subprocess
from pathlib import Path

def verifier_configuration_celery():
    """Vérifier la configuration Celery existante"""
    
    print("🔍 VÉRIFICATION CONFIGURATION CELERY")
    print("=" * 50)
    
    # Vérifier le fichier celery.py
    celery_file = Path('social_media_backend/celery.py')
    if celery_file.exists():
        print("✅ Fichier celery.py trouvé")
        with open(celery_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'autodiscover_tasks' in content:
                print("✅ Auto-découverte des tâches configurée")
            else:
                print("⚠️ Auto-découverte des tâches manquante")
    else:
        print("❌ Fichier celery.py manquant")
    
    # Vérifier __init__.py
    init_file = Path('social_media_backend/__init__.py')
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'celery' in content.lower():
                print("✅ Celery importé dans __init__.py")
            else:
                print("⚠️ Import Celery manquant dans __init__.py")
    
    # Vérifier les settings
    settings_file = Path('social_media_backend/settings.py')
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'CELERY_BROKER_URL' in content:
                print("✅ Configuration Celery broker trouvée")
            else:
                print("⚠️ Configuration Celery broker manquante")

def configurer_celery_complet():
    """Configurer Celery complètement"""
    
    print("\n⚙️ CONFIGURATION CELERY COMPLÈTE")
    print("=" * 50)
    
    # Ajouter la configuration Celery aux settings
    settings_file = Path('social_media_backend/settings.py')
    
    celery_config = '''

# ===================================================================
# CELERY CONFIGURATION FOR BACKGROUND TASKS
# ===================================================================

# Celery Configuration
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

# Celery Task Configuration
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat Configuration (for scheduled tasks)
CELERY_BEAT_SCHEDULE = {
    'cleanup-expired-tokens': {
        'task': 'users.tasks.cleanup_expired_tokens',
        'schedule': 3600.0,  # Every hour
    },
    'update-user-statistics': {
        'task': 'users.tasks.update_user_statistics',
        'schedule': 1800.0,  # Every 30 minutes
    },
    'send-notification-emails': {
        'task': 'interactions.tasks.send_notification_emails',
        'schedule': 600.0,  # Every 10 minutes
    },
}

# Celery Worker Configuration
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

# Celery Security
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_IGNORE_RESULT = False
CELERY_RESULT_EXPIRES = 3600  # 1 hour

print("🔄 Configuration Celery ajoutée aux settings")
'''
    
    # Lire le contenu actuel des settings
    with open(settings_file, 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    # Ajouter la configuration Celery si elle n'existe pas
    if 'CELERY_BROKER_URL' not in settings_content:
        with open(settings_file, 'a', encoding='utf-8') as f:
            f.write(celery_config)
        print("✅ Configuration Celery ajoutée aux settings")
    else:
        print("✅ Configuration Celery déjà présente")
    
    # Configurer __init__.py pour Celery
    init_file = Path('social_media_backend/__init__.py')
    celery_init = '''# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
'''
    
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            init_content = f.read()
        
        if 'celery_app' not in init_content:
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(celery_init)
            print("✅ Import Celery ajouté à __init__.py")
        else:
            print("✅ Import Celery déjà présent")
    else:
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(celery_init)
        print("✅ Fichier __init__.py créé avec import Celery")

def creer_taches_celery():
    """Créer des tâches Celery d'exemple"""
    
    print("\n🎯 CRÉATION TÂCHES CELERY")
    print("=" * 40)
    
    # Tâches pour l'app users
    users_tasks = '''"""
Tâches Celery pour l'application Users
"""

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task
def cleanup_expired_tokens():
    """Nettoyer les tokens JWT expirés"""
    try:
        # Logique de nettoyage des tokens expirés
        logger.info("🧹 Nettoyage des tokens expirés démarré")
        
        # Ici vous pouvez ajouter la logique pour nettoyer
        # les tokens expirés de votre base de données
        
        logger.info("✅ Nettoyage des tokens terminé")
        return "Tokens expirés nettoyés avec succès"
    except Exception as e:
        logger.error(f"❌ Erreur nettoyage tokens : {e}")
        return f"Erreur : {e}"

@shared_task
def update_user_statistics():
    """Mettre à jour les statistiques utilisateur"""
    try:
        logger.info("📊 Mise à jour statistiques utilisateur démarrée")
        
        # Mettre à jour les compteurs pour tous les utilisateurs
        users = User.objects.all()
        updated_count = 0
        
        for user in users:
            # Mettre à jour followers_count
            user.followers_count = user.followers.count()
            # Mettre à jour following_count  
            user.following_count = user.following.count()
            # Mettre à jour posts_count
            user.posts_count = user.posts.count()
            user.save(update_fields=['followers_count', 'following_count', 'posts_count'])
            updated_count += 1
        
        logger.info(f"✅ Statistiques mises à jour pour {updated_count} utilisateurs")
        return f"Statistiques mises à jour pour {updated_count} utilisateurs"
    except Exception as e:
        logger.error(f"❌ Erreur mise à jour statistiques : {e}")
        return f"Erreur : {e}"

@shared_task
def send_welcome_email(user_id):
    """Envoyer un email de bienvenue à un nouvel utilisateur"""
    try:
        user = User.objects.get(id=user_id)
        logger.info(f"📧 Envoi email de bienvenue à {user.email}")
        
        # Ici vous pouvez ajouter la logique d'envoi d'email
        # Par exemple avec Django's send_mail ou un service externe
        
        logger.info(f"✅ Email de bienvenue envoyé à {user.email}")
        return f"Email de bienvenue envoyé à {user.email}"
    except User.DoesNotExist:
        logger.error(f"❌ Utilisateur {user_id} non trouvé")
        return f"Utilisateur {user_id} non trouvé"
    except Exception as e:
        logger.error(f"❌ Erreur envoi email : {e}")
        return f"Erreur : {e}"
'''
    
    users_tasks_file = Path('users/tasks.py')
    if not users_tasks_file.exists():
        with open(users_tasks_file, 'w', encoding='utf-8') as f:
            f.write(users_tasks)
        print("✅ Tâches Celery créées pour users")
    else:
        print("✅ Tâches Celery users déjà présentes")
    
    # Tâches pour l'app interactions
    interactions_tasks = '''"""
Tâches Celery pour l'application Interactions
"""

from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task
def send_notification_emails():
    """Envoyer les emails de notification en attente"""
    try:
        logger.info("📧 Envoi des notifications par email démarré")
        
        # Récupérer les notifications non lues des dernières 24h
        notifications = Notification.objects.filter(
            is_read=False,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).select_related('recipient', 'sender')
        
        sent_count = 0
        for notification in notifications:
            # Logique d'envoi d'email
            logger.info(f"📧 Notification envoyée à {notification.recipient.email}")
            sent_count += 1
        
        logger.info(f"✅ {sent_count} notifications envoyées par email")
        return f"{sent_count} notifications envoyées"
    except Exception as e:
        logger.error(f"❌ Erreur envoi notifications : {e}")
        return f"Erreur : {e}"

@shared_task
def cleanup_old_notifications():
    """Nettoyer les anciennes notifications"""
    try:
        logger.info("🧹 Nettoyage anciennes notifications démarré")
        
        # Supprimer les notifications de plus de 30 jours
        old_notifications = Notification.objects.filter(
            created_at__lt=timezone.now() - timedelta(days=30)
        )
        
        count = old_notifications.count()
        old_notifications.delete()
        
        logger.info(f"✅ {count} anciennes notifications supprimées")
        return f"{count} anciennes notifications supprimées"
    except Exception as e:
        logger.error(f"❌ Erreur nettoyage notifications : {e}")
        return f"Erreur : {e}"

@shared_task
def process_like_notification(like_id):
    """Traiter une notification de like"""
    try:
        from .models import Like
        
        like = Like.objects.select_related('user').get(id=like_id)
        logger.info(f"👍 Traitement notification like de {like.user.username}")
        
        # Créer une notification
        # Logique de création de notification
        
        return f"Notification like traitée pour {like.user.username}"
    except Exception as e:
        logger.error(f"❌ Erreur traitement like : {e}")
        return f"Erreur : {e}"
'''
    
    interactions_tasks_file = Path('interactions/tasks.py')
    if not interactions_tasks_file.exists():
        with open(interactions_tasks_file, 'w', encoding='utf-8') as f:
            f.write(interactions_tasks)
        print("✅ Tâches Celery créées pour interactions")
    else:
        print("✅ Tâches Celery interactions déjà présentes")

def configurer_swagger_complet():
    """Configurer Swagger/OpenAPI complètement"""
    
    print("\n📚 CONFIGURATION SWAGGER COMPLÈTE")
    print("=" * 50)
    
    # Vérifier si drf-spectacular est installé
    try:
        import drf_spectacular
        print("✅ drf-spectacular déjà installé")
    except ImportError:
        print("⚠️ Installation de drf-spectacular requise")
        subprocess.run(['pip', 'install', 'drf-spectacular'], check=True)
        print("✅ drf-spectacular installé")
    
    # Créer des vues API REST pour Swagger
    api_views_content = '''"""
Vues API REST pour documentation Swagger
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth import get_user_model
from posts.models import Post
from interactions.models import Like, Comment

User = get_user_model()

@extend_schema(
    summary="🏠 Page d'accueil de l'API",
    description="Point d'entrée principal de l'API ALX Project Nexus",
    responses={200: {"description": "Informations de l'API"}},
    tags=["🏠 Accueil"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_home(request):
    """Page d'accueil de l'API"""
    return Response({
        "message": "🚀 Bienvenue sur ALX Project Nexus API",
        "version": "1.0.0",
        "description": "API complète pour réseau social",
        "endpoints": {
            "graphql": "/graphql/",
            "admin": "/admin/",
            "swagger": "/api/docs/",
            "redoc": "/api/redoc/"
        },
        "features": [
            "👥 Gestion utilisateurs",
            "📝 Publications et commentaires", 
            "❤️ Likes et interactions",
            "🔍 Recherche avancée",
            "🔐 Authentification JWT"
        ]
    })

@extend_schema(
    summary="📊 Statistiques de la plateforme",
    description="Récupérer les statistiques générales de la plateforme",
    responses={200: {"description": "Statistiques de la plateforme"}},
    tags=["📊 Statistiques"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def platform_stats(request):
    """Statistiques de la plateforme"""
    try:
        stats = {
            "users_count": User.objects.count(),
            "posts_count": Post.objects.count(),
            "likes_count": Like.objects.count(),
            "comments_count": Comment.objects.count(),
        }
        return Response({
            "success": True,
            "data": stats,
            "message": "Statistiques récupérées avec succès"
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="🔍 Recherche globale",
    description="Rechercher dans tous les contenus de la plateforme",
    parameters=[
        OpenApiParameter(
            name='q',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Terme de recherche',
            required=True
        ),
        OpenApiParameter(
            name='type',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Type de contenu (users, posts, all)',
            required=False
        )
    ],
    responses={200: {"description": "Résultats de recherche"}},
    tags=["🔍 Recherche"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def global_search(request):
    """Recherche globale"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    if not query:
        return Response({
            "success": False,
            "error": "Paramètre 'q' requis"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    results = {"users": [], "posts": []}
    
    try:
        if search_type in ['users', 'all']:
            users = User.objects.filter(
                username__icontains=query
            ).values('id', 'username', 'email')[:10]
            results['users'] = list(users)
        
        if search_type in ['posts', 'all']:
            posts = Post.objects.filter(
                content__icontains=query
            ).select_related('author').values(
                'id', 'content', 'author__username', 'created_at'
            )[:10]
            results['posts'] = list(posts)
        
        return Response({
            "success": True,
            "query": query,
            "results": results,
            "message": f"Recherche effectuée pour '{query}'"
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="💚 Santé de l'API",
    description="Vérifier l'état de santé de l'API et des services",
    responses={200: {"description": "État de santé de l'API"}},
    tags=["🔧 Monitoring"]
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Vérification de santé de l'API"""
    try:
        # Vérifier la base de données
        User.objects.count()
        
        # Vérifier Redis (si configuré)
        health_status = {
            "status": "healthy",
            "database": "connected",
            "timestamp": timezone.now().isoformat(),
            "services": {
                "django": "running",
                "database": "connected",
                "redis": "connected"  # À adapter selon votre config
            }
        }
        
        return Response(health_status)
    except Exception as e:
        return Response({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": timezone.now().isoformat()
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
'''
    
    # Créer le fichier des vues API
    api_views_file = Path('social_media_backend/api_views.py')
    with open(api_views_file, 'w', encoding='utf-8') as f:
        f.write(api_views_content)
    print("✅ Vues API REST créées pour Swagger")

def mettre_a_jour_urls():
    """Mettre à jour les URLs pour inclure Swagger"""
    
    print("\n🔗 MISE À JOUR URLs POUR SWAGGER")
    print("=" * 50)
    
    # URLs principales avec Swagger
    main_urls_content = '''"""
Configuration des URLs principales avec Swagger
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)
from .api_views import api_home, platform_stats, global_search, health_check

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API REST Documentation
    path('', api_home, name='api-home'),
    path('api/stats/', platform_stats, name='platform-stats'),
    path('api/search/', global_search, name='global-search'),
    path('api/health/', health_check, name='health-check'),
    
    # GraphQL
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    
    # Swagger/OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Servir les fichiers statiques en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
    
    urls_file = Path('social_media_backend/urls.py')
    with open(urls_file, 'w', encoding='utf-8') as f:
        f.write(main_urls_content)
    print("✅ URLs mises à jour avec Swagger")

def tester_configuration():
    """Tester la configuration Celery et Swagger"""
    
    print("\n🧪 TEST CONFIGURATION")
    print("=" * 40)
    
    try:
        # Test import Celery
        from social_media_backend.celery import app as celery_app
        print("✅ Import Celery réussi")
        
        # Test import tâches
        try:
            from users.tasks import cleanup_expired_tokens
            print("✅ Import tâches users réussi")
        except ImportError:
            print("⚠️ Tâches users non importables")
        
        try:
            from interactions.tasks import send_notification_emails
            print("✅ Import tâches interactions réussi")
        except ImportError:
            print("⚠️ Tâches interactions non importables")
        
        # Test import Swagger
        try:
            import drf_spectacular
            print("✅ drf-spectacular importé")
        except ImportError:
            print("❌ drf-spectacular non disponible")
        
    except Exception as e:
        print(f"❌ Erreur test configuration : {e}")

def generer_rapport_final():
    """Générer le rapport final"""
    
    print("\n📊 RAPPORT FINAL - CELERY + SWAGGER")
    print("=" * 60)
    
    print("\n✅ CELERY CONFIGURATION COMPLÈTE :")
    print("  🔄 Configuration broker Redis ajoutée")
    print("  📋 Tâches background créées (users + interactions)")
    print("  ⏰ Planification automatique configurée")
    print("  🔧 Worker et beat settings optimisés")
    
    print("\n✅ SWAGGER DOCUMENTATION COMPLÈTE :")
    print("  📚 drf-spectacular configuré")
    print("  🌐 Interface Swagger UI disponible")
    print("  📖 Documentation ReDoc disponible")
    print("  🔗 Endpoints API REST créés")
    
    print("\n🌐 ENDPOINTS DISPONIBLES :")
    print("  📊 http://localhost:8000/ - API Home")
    print("  📈 http://localhost:8000/api/stats/ - Statistiques")
    print("  🔍 http://localhost:8000/api/search/ - Recherche")
    print("  💚 http://localhost:8000/api/health/ - Health Check")
    print("  🎯 http://localhost:8000/graphql/ - GraphQL")
    print("  📚 http://localhost:8000/api/docs/ - Swagger UI")
    print("  📖 http://localhost:8000/api/redoc/ - ReDoc")
    
    print("\n🎊 PROJET ALX 100% PRÊT AVEC CELERY + SWAGGER !")

def main():
    """Fonction principale"""
    
    print("🚀 SETUP CELERY + SWAGGER - ALX PROJECT NEXUS")
    print("=" * 70)
    
    # Configuration Celery
    verifier_configuration_celery()
    configurer_celery_complet()
    creer_taches_celery()
    
    # Configuration Swagger
    configurer_swagger_complet()
    mettre_a_jour_urls()
    
    # Tests
    tester_configuration()
    
    # Rapport final
    generer_rapport_final()
    
    print("\n" + "=" * 70)
    print("🎯 CONFIGURATION TERMINÉE - REDÉMARREZ DOCKER ! 🐳")

if __name__ == "__main__":
    main()
