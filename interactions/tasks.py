"""
Celery tasks for interactions app.
"""

from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from .models import Notification


@shared_task
def send_notification(recipient_id, sender_id, notification_type, message, content_type_id=None, object_id=None):
    """
    Send a notification to a user.
    """
    try:
        from users.models import User
        
        recipient = User.objects.get(id=recipient_id)
        sender = User.objects.get(id=sender_id) if sender_id else None
        
        content_type = None
        if content_type_id:
            content_type = ContentType.objects.get(id=content_type_id)
        
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            message=message,
            content_type=content_type,
            object_id=object_id
        )
        
        return f"Notification {notification.id} sent to {recipient.username}"
    except Exception as e:
        return f"Error sending notification: {str(e)}"


@shared_task
def cleanup_old_notifications():
    """
    Clean up old read notifications (older than 30 days).
    """
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_count = Notification.objects.filter(
            is_read=True,
            created_at__lt=cutoff_date
        ).delete()[0]
        
        return f"Cleaned up {deleted_count} old notifications"
    except Exception as e:
        return f"Error cleaning up notifications: {str(e)}"


@shared_task
def update_trending_hashtags():
    """
    Update trending hashtags based on recent activity.
    """
    try:
        from posts.models import Hashtag, PostHashtag
        from django.utils import timezone
        from datetime import timedelta
        from django.db import models
        
        # Get hashtags used in the last 7 days
        week_ago = timezone.now() - timedelta(days=7)
        recent_hashtags = PostHashtag.objects.filter(
            created_at__gte=week_ago
        ).values('hashtag').annotate(
            recent_count=models.Count('hashtag')
        )
        
        # Update trending scores (simplified algorithm)
        for item in recent_hashtags:
            hashtag = Hashtag.objects.get(id=item['hashtag'])
            # Simple trending score: recent posts * 2 + total posts
            hashtag.trending_score = item['recent_count'] * 2 + hashtag.posts_count
            hashtag.save(update_fields=['trending_score'])
        
        return f"Updated trending scores for {len(recent_hashtags)} hashtags"
    except Exception as e:
        return f"Error updating trending hashtags: {str(e)}"
