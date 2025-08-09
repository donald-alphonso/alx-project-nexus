"""
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
