"""
Django Apps Configuration for Social Media Backend
"""

from django.apps import AppConfig


class SocialMediaBackendConfig(AppConfig):
    """
    Main application configuration
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_media_backend'
    verbose_name = 'Social Media Backend'
    
    def ready(self):
        """
        Initialize application when Django starts
        """
        # Import Celery admin customizations
        # Temporarily disabled to fix startup issues
        pass
