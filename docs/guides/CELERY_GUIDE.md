# 🔧 Celery Background Tasks Guide

## Overview

Celery is integrated into ALX Project Nexus to handle background tasks, scheduled operations, and asynchronous processing. This guide covers all Celery functionality and management.

## 📋 Available Tasks

### 👥 User Management Tasks

#### `cleanup_expired_tokens`
- **Purpose:** Clean up expired JWT tokens and inactive sessions
- **Schedule:** Daily at 2:00 AM
- **Queue:** maintenance
- **Description:** Identifies users inactive for 30+ days and cleans up associated tokens

#### `update_user_statistics`
- **Purpose:** Update user statistics and counters
- **Schedule:** Daily at 3:00 AM  
- **Queue:** analytics
- **Description:** Updates followers_count, following_count, and posts_count for all users

#### `send_welcome_email`
- **Purpose:** Send welcome email to new users
- **Trigger:** Manual (called after user registration)
- **Queue:** emails
- **Description:** Sends personalized welcome email to newly registered users

### 📝 Content Management Tasks

#### `process_media_upload`
- **Purpose:** Process uploaded media files
- **Trigger:** Manual (called after media upload)
- **Queue:** media (high priority)
- **Description:** Processes images and videos (resize, thumbnails, compression)

#### `update_trending_hashtags`
- **Purpose:** Update trending hashtags based on recent activity
- **Schedule:** Every hour
- **Queue:** analytics
- **Description:** Analyzes hashtag usage in the last 7 days and updates trending status

#### `cleanup_old_posts`
- **Purpose:** Clean up old posts with no engagement
- **Schedule:** Weekly on Sunday at 1:00 AM
- **Queue:** maintenance
- **Description:** Reviews posts older than 1 year with minimal engagement

#### `generate_content_analytics`
- **Purpose:** Generate daily content analytics and insights
- **Schedule:** Daily at 4:00 AM
- **Queue:** analytics
- **Description:** Calculates daily statistics for posts, comments, and user activity

#### `update_post_engagement_scores`
- **Purpose:** Update engagement scores for posts
- **Schedule:** Daily at 5:00 AM
- **Queue:** analytics
- **Description:** Calculates engagement scores for better feed ranking

#### `send_content_digest_email`
- **Purpose:** Send weekly content digest to active users
- **Schedule:** Weekly on Monday at 9:00 AM
- **Queue:** emails
- **Description:** Sends personalized content digest with top posts

## 🚀 Getting Started

### Prerequisites

1. **Redis Server** - Required for Celery broker
2. **Django Application** - Must be running
3. **Database Access** - For task data storage

### Starting Celery Services

#### Method 1: Using Docker (Recommended)
```bash
# Start all services including Celery
docker-compose up -d

# Check Celery worker logs
docker-compose logs celery_worker

# Check Celery beat logs  
docker-compose logs celery_beat
```

#### Method 2: Manual Start
```bash
# Start Celery worker
celery -A social_media_backend worker --loglevel=info

# Start Celery beat scheduler (in separate terminal)
celery -A social_media_backend beat --loglevel=info
```

#### Method 3: Using Management Script
```bash
# Check system status
python scripts/utils/CELERY_MANAGER.py status

# Start worker
python scripts/utils/CELERY_MANAGER.py worker

# Start beat scheduler
python scripts/utils/CELERY_MANAGER.py beat

# Test tasks
python scripts/utils/CELERY_MANAGER.py test
```

## 📊 Monitoring and Management

### Checking Task Status

#### Using Django Admin
1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Navigate to "Periodic Tasks" section
4. View scheduled tasks and their status

#### Using Celery Commands
```bash
# Check active tasks
celery -A social_media_backend inspect active

# Check scheduled tasks
celery -A social_media_backend inspect scheduled

# Check worker stats
celery -A social_media_backend inspect stats

# Monitor in real-time
celery -A social_media_backend events
```

#### Using Management Script
```bash
# Monitor workers and tasks
python scripts/utils/CELERY_MANAGER.py monitor
```

### Task Queues

The system uses multiple queues for task prioritization:

- **media** (Priority 9) - Media processing tasks
- **emails** (Priority 8) - Email sending tasks  
- **users** (Priority 7) - User management tasks
- **analytics** (Priority 5) - Analytics and statistics
- **maintenance** (Priority 3) - Cleanup and maintenance
- **default** - General tasks

## 🧪 Testing Tasks

### Manual Task Execution

#### From Django Shell
```python
# Open Django shell
python manage.py shell

# Import and execute tasks
from users.tasks import update_user_statistics
from posts.tasks import update_trending_hashtags

# Execute immediately
result = update_user_statistics.delay()
print(f"Task ID: {result.id}")

# Check result
if result.ready():
    print(f"Result: {result.result}")
```

#### Using Management Script
```bash
# Test all tasks
python scripts/utils/CELERY_MANAGER.py test
```

### Automated Testing

The system includes automated task testing in the validation scripts:

```bash
# Run comprehensive validation including Celery
python scripts/tests/VALIDATION_AMELIOREE.py
```

## ⚙️ Configuration

### Task Schedules

Task schedules are defined in `social_media_backend/celery_schedule.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'cleanup-expired-tokens': {
        'task': 'users.tasks.cleanup_expired_tokens',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2:00 AM
        'options': {'queue': 'maintenance'}
    },
    # ... other tasks
}
```

### Environment Variables

Configure Celery using environment variables:

```bash
# Redis broker URL
CELERY_BROKER_URL=redis://localhost:6379/1

# Result backend URL  
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Worker concurrency
CELERY_WORKER_CONCURRENCY=4
```

### Development vs Production

#### Development Settings
- Tasks execute synchronously (`task_always_eager=True`)
- Reduced task frequency
- Enhanced logging

#### Production Settings
- Asynchronous task execution
- Full task scheduling
- Optimized performance

## 🔧 Troubleshooting

### Common Issues

#### Redis Connection Error
```
Error: Redis connection failed
```
**Solution:**
1. Check if Redis is running: `redis-cli ping`
2. Verify Redis URL in settings
3. Check firewall/network connectivity

#### Worker Not Starting
```
Error: Failed to start Celery worker
```
**Solution:**
1. Check Django settings are correct
2. Verify database connectivity
3. Check for port conflicts
4. Review worker logs for specific errors

#### Tasks Not Executing
```
Tasks submitted but not executing
```
**Solution:**
1. Verify worker is running: `celery -A social_media_backend inspect active`
2. Check task routing and queues
3. Verify Redis connectivity
4. Check worker logs for errors

#### Beat Scheduler Issues
```
Scheduled tasks not running
```
**Solution:**
1. Verify beat scheduler is running
2. Check database permissions for beat schedule
3. Verify timezone settings
4. Check beat logs for errors

### Debugging Commands

```bash
# Check worker status
celery -A social_media_backend inspect ping

# Purge all tasks
celery -A social_media_backend purge

# Restart workers
celery -A social_media_backend control shutdown
# Then restart workers

# Check configuration
celery -A social_media_backend inspect conf
```

## 📈 Performance Optimization

### Worker Configuration

```bash
# Optimize worker for high load
celery -A social_media_backend worker \
    --concurrency=8 \
    --prefetch-multiplier=1 \
    --max-tasks-per-child=1000
```

### Queue Management

```bash
# Start workers for specific queues
celery -A social_media_backend worker -Q media,emails
celery -A social_media_backend worker -Q analytics,maintenance
```

### Monitoring

```bash
# Real-time monitoring
celery -A social_media_backend events

# Flower web monitoring (if installed)
celery -A social_media_backend flower
```

## 🔒 Security Considerations

1. **Redis Security:** Secure Redis with authentication and network restrictions
2. **Task Validation:** Validate all task inputs and parameters
3. **Error Handling:** Implement proper error handling and logging
4. **Resource Limits:** Set appropriate memory and CPU limits
5. **Queue Isolation:** Use separate queues for different task types

## 📚 Additional Resources

- **Celery Documentation:** https://docs.celeryproject.org/
- **Django-Celery-Beat:** https://django-celery-beat.readthedocs.io/
- **Redis Documentation:** https://redis.io/documentation
- **Task Monitoring:** Use Flower or Django Admin for monitoring

## 🎯 Best Practices

1. **Task Design:** Keep tasks small and focused
2. **Error Handling:** Implement retry logic for transient failures
3. **Monitoring:** Monitor task execution and performance
4. **Testing:** Test tasks in development before production
5. **Documentation:** Document task purpose and dependencies
6. **Logging:** Use structured logging for debugging
7. **Resource Management:** Monitor memory and CPU usage
8. **Queue Management:** Use appropriate queues for task priority

---

*This guide covers all aspects of Celery integration in ALX Project Nexus. For specific implementation details, refer to the task files in `users/tasks.py` and `posts/tasks.py`.*
