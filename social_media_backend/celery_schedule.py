"""
Celery Beat Schedule Configuration
Defines periodic tasks and their execution schedules
"""

from celery.schedules import crontab

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    # User Management Tasks
    'cleanup-expired-tokens': {
        'task': 'users.tasks.cleanup_expired_tokens',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2:00 AM
        'options': {'queue': 'maintenance'}
    },
    
    'update-user-statistics': {
        'task': 'users.tasks.update_user_statistics',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3:00 AM
        'options': {'queue': 'analytics'}
    },
    
    # Content Management Tasks
    'update-trending-hashtags': {
        'task': 'posts.tasks.update_trending_hashtags',
        'schedule': crontab(minute=0),  # Every hour
        'options': {'queue': 'analytics'}
    },
    
    'cleanup-old-posts': {
        'task': 'posts.tasks.cleanup_old_posts',
        'schedule': crontab(hour=1, minute=0, day_of_week=0),  # Weekly on Sunday at 1:00 AM
        'options': {'queue': 'maintenance'}
    },
    
    'generate-content-analytics': {
        'task': 'posts.tasks.generate_content_analytics',
        'schedule': crontab(hour=4, minute=0),  # Daily at 4:00 AM
        'options': {'queue': 'analytics'}
    },
    
    'update-post-engagement-scores': {
        'task': 'posts.tasks.update_post_engagement_scores',
        'schedule': crontab(hour=5, minute=0),  # Daily at 5:00 AM
        'options': {'queue': 'analytics'}
    },
    
    # Communication Tasks
    'send-content-digest-email': {
        'task': 'posts.tasks.send_content_digest_email',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # Weekly on Monday at 9:00 AM
        'options': {'queue': 'emails'}
    },
}

# Task Routes - Assign tasks to specific queues
CELERY_TASK_ROUTES = {
    # User tasks
    'users.tasks.*': {'queue': 'users'},
    
    # Post tasks
    'posts.tasks.process_media_upload': {'queue': 'media'},
    'posts.tasks.update_trending_hashtags': {'queue': 'analytics'},
    'posts.tasks.cleanup_old_posts': {'queue': 'maintenance'},
    'posts.tasks.generate_content_analytics': {'queue': 'analytics'},
    'posts.tasks.update_post_engagement_scores': {'queue': 'analytics'},
    'posts.tasks.send_content_digest_email': {'queue': 'emails'},
}

# Queue Priorities
CELERY_TASK_QUEUE_PRIORITIES = {
    'media': 9,      # High priority for media processing
    'emails': 8,     # High priority for emails
    'users': 7,      # Medium-high priority for user tasks
    'analytics': 5,  # Medium priority for analytics
    'maintenance': 3, # Low priority for maintenance tasks
}

# Task Configuration
CELERY_TASK_CONFIG = {
    # Default task settings
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
    
    # Task execution settings
    'task_always_eager': False,  # Set to True for testing
    'task_eager_propagates': True,
    'task_ignore_result': False,
    'task_store_eager_result': True,
    
    # Task retry settings
    'task_acks_late': True,
    'task_reject_on_worker_lost': True,
    'task_default_retry_delay': 60,  # 1 minute
    'task_max_retries': 3,
    
    # Worker settings
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 1000,
    'worker_disable_rate_limits': False,
    
    # Result backend settings
    'result_expires': 3600,  # 1 hour
    'result_persistent': True,
}

# Monitoring and Logging
CELERY_MONITORING = {
    'worker_send_task_events': True,
    'task_send_sent_event': True,
    'worker_hijack_root_logger': False,
    'worker_log_color': True,
}

# Development vs Production Settings
import os

if os.getenv('DJANGO_ENV') == 'development':
    # Development settings
    CELERY_TASK_CONFIG.update({
        'task_always_eager': True,  # Execute tasks synchronously in development
        'task_eager_propagates': True,
    })
    
    # Reduce frequency for development
    CELERY_BEAT_SCHEDULE.update({
        'update-trending-hashtags': {
            'task': 'posts.tasks.update_trending_hashtags',
            'schedule': crontab(minute='*/30'),  # Every 30 minutes in dev
            'options': {'queue': 'analytics'}
        },
    })
