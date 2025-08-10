# 🔧 Admin Dashboard Guide - ALX Project Nexus

## 🎯 Overview

The Django Admin Dashboard provides comprehensive management capabilities for the ALX Project Nexus social media platform. This guide covers all administrative features and functionalities.

---

## 🔑 Admin Access

### Login Information
- **URL:** http://localhost:8000/admin/
- **Email:** `admin@example.com` ⚠️ **Use EMAIL for login**
- **Password:** `admin123`

### Important Note
The system uses email-based authentication (`USERNAME_FIELD = 'email'`), so you must login with the email address, not the username.

---

## 👥 User Management

### User Administration Features

#### View All Users
- **Location:** Admin Dashboard → Users → Users
- **Features:**
  - List all registered users (currently 27 users)
  - Filter by status, verification, staff permissions
  - Search by username, email, or name
  - Bulk actions for multiple users

#### User Details Available
- **Personal Info:** Username, email, first name, last name
- **Profile Data:** Bio, avatar, birth date, location, website
- **Status Flags:** Active, staff, superuser, verified
- **Statistics:** Followers count, following count, posts count
- **Timestamps:** Date joined, last login, last updated

#### User Management Actions
```python
# Promote user to admin
user.is_staff = True
user.is_superuser = True
user.save()

# Verify user account
user.is_verified = True
user.save()

# Deactivate user
user.is_active = False
user.save()
```

### User Permissions
- **Superuser:** Full admin access
- **Staff:** Admin panel access
- **Active:** Can login and use platform
- **Verified:** Verified account badge

---

## 📝 Content Management

### Post Administration

#### Post Overview
- **Location:** Admin Dashboard → Posts → Posts
- **Features:**
  - View all posts across the platform
  - Filter by author, visibility, date
  - Search post content
  - Moderate content

#### Post Details
- **Content:** Text content (up to 2200 characters)
- **Media:** Image and video support
  - **Images:** JPG, JPEG, PNG, GIF
  - **Videos:** MP4, AVI, MOV, WMV
- **Visibility:** Public, followers-only, private
- **Engagement:** Likes, comments, shares, views counts
- **Status:** Pinned posts, creation/update timestamps

#### Content Moderation
- **Review flagged content**
- **Delete inappropriate posts**
- **Pin important announcements**
- **Monitor engagement metrics**

### Comment Management
- **Location:** Admin Dashboard → Posts → Comments
- **Features:**
  - View all comments
  - Moderate comment threads
  - Handle nested replies
  - Remove inappropriate content

---

## ❤️ Social Interactions Management

### Likes System
- **Location:** Admin Dashboard → Interactions → Likes
- **Features:**
  - View all like activities
  - Monitor popular content
  - Analyze engagement patterns

### Follow Relationships
- **Location:** Admin Dashboard → Users → Follows
- **Features:**
  - View follower/following relationships
  - Monitor user connections
  - Identify influential users

### Notifications
- **Location:** Admin Dashboard → Interactions → Notifications
- **Features:**
  - View all system notifications
  - Monitor notification delivery
  - Manage notification types

---

## 🏷️ Content Organization

### Hashtag Management
- **Location:** Admin Dashboard → Posts → Hashtags
- **Features:**
  - View all hashtags
  - Monitor hashtag popularity
  - Manage trending topics
  - Link hashtags to posts

### Post-Hashtag Relationships
- **Location:** Admin Dashboard → Posts → Post hashtags
- **Features:**
  - Manage hashtag associations
  - Bulk hashtag operations
  - Content categorization

---

## 📊 Analytics & Monitoring

### User Analytics
- **Total Users:** 27 registered users
- **User Types:**
  - Regular users: 26
  - Admin users: 1
  - Verified users: Variable
  - Active users: Monitor login activity

### Content Analytics
- **Post Statistics:**
  - Total posts created
  - Posts by visibility type
  - Media vs text posts
  - Engagement metrics

### Engagement Metrics
- **Likes:** Total likes across platform
- **Comments:** Comment activity
- **Follows:** User relationship growth
- **Hashtags:** Trending topics

---

## 🛡️ Security & Moderation

### Security Features
- **User Authentication:** Email-based login
- **Permission System:** Staff/superuser roles
- **Content Validation:** File type restrictions
- **Rate Limiting:** API abuse prevention

### Moderation Tools
- **Content Review:** Manual post/comment review
- **User Management:** Account activation/deactivation
- **Bulk Actions:** Mass content operations
- **Reporting System:** Handle user reports

### Security Best Practices
- **Regular Password Updates:** Change admin passwords
- **Permission Audits:** Review user permissions
- **Content Monitoring:** Regular content review
- **Activity Logs:** Monitor admin actions

---

## 🔧 System Administration

### Database Management
- **Migrations:** Apply database changes
- **Backups:** Regular data backups
- **Cleanup:** Remove orphaned data
- **Optimization:** Database performance tuning

### Media Management
- **File Storage:** Monitor uploaded files
- **Storage Cleanup:** Remove unused media
- **File Validation:** Ensure proper formats
- **Size Monitoring:** Track storage usage

### System Health
- **Health Check:** http://localhost:8000/api/health/
- **Service Status:** Monitor all services
- **Error Logs:** Review system errors
- **Performance:** Monitor response times

---

## 📈 Advanced Features

### Bulk Operations
```python
# Bulk user verification
User.objects.filter(email__endswith='@company.com').update(is_verified=True)

# Bulk post visibility change
Post.objects.filter(author__username='spammer').update(visibility='private')

# Bulk notification cleanup
Notification.objects.filter(created_at__lt=thirty_days_ago).delete()
```

### Custom Admin Actions
- **Verify Users:** Bulk user verification
- **Content Moderation:** Mass content actions
- **Notification Management:** Bulk notification operations
- **Data Export:** Export user/content data

### Reporting Features
- **User Reports:** Generate user activity reports
- **Content Reports:** Analyze content performance
- **Engagement Reports:** Social interaction analytics
- **System Reports:** Technical performance metrics

---

## 🚨 Emergency Procedures

### Content Crisis Management
1. **Inappropriate Content:**
   - Immediately set post visibility to 'private'
   - Review and delete if necessary
   - Notify content author if appropriate

2. **Spam Attack:**
   - Identify spam patterns
   - Bulk delete spam content
   - Temporarily restrict user accounts

3. **Security Breach:**
   - Change admin passwords immediately
   - Review user permissions
   - Check system logs for suspicious activity

### User Management Crisis
1. **Account Compromise:**
   - Deactivate affected accounts
   - Reset passwords
   - Review account activity

2. **Mass User Issues:**
   - Use bulk operations for efficiency
   - Communicate with affected users
   - Document actions taken

---

## 🔍 Troubleshooting

### Common Admin Issues

#### Login Problems
- **Issue:** Cannot access admin panel
- **Solution:** Verify email/password, check staff status
- **Command:** 
  ```bash
  docker-compose exec web python manage.py shell -c "
  from users.models import User
  admin = User.objects.get(username='admin')
  admin.is_staff = True
  admin.save()
  "
  ```

#### Permission Errors
- **Issue:** Insufficient permissions for admin actions
- **Solution:** Verify superuser status
- **Command:**
  ```bash
  docker-compose exec web python manage.py shell -c "
  from users.models import User
  admin = User.objects.get(username='admin')
  admin.is_superuser = True
  admin.save()
  "
  ```

#### Database Issues
- **Issue:** Database connection errors
- **Solution:** Check PostgreSQL container status
- **Command:** `docker-compose ps`

---

## 📚 Quick Reference

### Essential Admin URLs
- **Main Dashboard:** `/admin/`
- **Users:** `/admin/users/user/`
- **Posts:** `/admin/posts/post/`
- **Comments:** `/admin/posts/comment/`
- **Interactions:** `/admin/interactions/`

### Key Admin Commands
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Change user password
docker-compose exec web python manage.py changepassword username

# Collect static files
docker-compose exec web python manage.py collectstatic

# Database migrations
docker-compose exec web python manage.py migrate
```

### Useful Queries
```python
# Most active users
User.objects.order_by('-posts_count')[:10]

# Recent posts
Post.objects.order_by('-created_at')[:20]

# Popular hashtags
Hashtag.objects.order_by('-posts_count')[:10]

# Unread notifications
Notification.objects.filter(is_read=False)
```

---

## 🎯 Best Practices

### Daily Admin Tasks
1. **Content Review:** Check recent posts/comments
2. **User Activity:** Monitor new registrations
3. **System Health:** Check health endpoint
4. **Security Review:** Review admin logs

### Weekly Admin Tasks
1. **Analytics Review:** Analyze platform growth
2. **Content Cleanup:** Remove inappropriate content
3. **User Management:** Review user permissions
4. **System Maintenance:** Database optimization

### Monthly Admin Tasks
1. **Security Audit:** Comprehensive security review
2. **Performance Analysis:** System performance review
3. **Data Backup:** Ensure data backup integrity
4. **Feature Planning:** Plan new features/improvements

---

## 🆘 Support & Resources

### Getting Help
1. **Health Check:** Monitor system status
2. **Error Logs:** Review Django logs
3. **Documentation:** Consult API docs
4. **Community:** Django admin documentation

## 🔧 Celery Task Management

### Accessing Celery Admin

#### Django Celery Beat Section
1. Navigate to **Django Celery Beat** in the admin sidebar
2. Available sections:
   - **Periodic Tasks** - Manage scheduled tasks
   - **Crontab Schedules** - Define cron-style schedules
   - **Interval Schedules** - Define interval-based schedules
   - **Solar Schedules** - Sun-based scheduling
   - **Clocked Schedules** - One-time scheduled tasks

### Managing Periodic Tasks

#### Viewing Tasks
- **List View:** Shows all periodic tasks with status
- **Filters:** Filter by enabled/disabled, schedule type
- **Search:** Search by task name or description
- **Actions:** Enable/disable, edit, delete tasks

#### Task Information
- **Name:** Human-readable task identifier
- **Task:** Python path to the task function
- **Enabled:** Whether the task is active
- **Schedule:** When the task runs (crontab, interval, etc.)
- **Last Run:** When the task last executed
- **Total Runs:** Number of times the task has run

#### Creating New Tasks
1. Click **Add Periodic Task**
2. Fill in task details:
   - **Name:** Descriptive name
   - **Task:** Select from available tasks
   - **Enabled:** Check to activate
3. Configure schedule:
   - **Crontab:** For cron-style scheduling
   - **Interval:** For regular intervals
   - **One-off:** For single execution
4. Set optional parameters:
   - **Arguments:** JSON array of positional args
   - **Keyword Arguments:** JSON object of named args
   - **Queue:** Specific queue for the task
   - **Priority:** Task priority (0-9)

#### Available Tasks

**User Management Tasks:**
- `users.tasks.cleanup_expired_tokens`
- `users.tasks.update_user_statistics`
- `users.tasks.send_welcome_email`

**Content Management Tasks:**
- `posts.tasks.process_media_upload`
- `posts.tasks.update_trending_hashtags`
- `posts.tasks.cleanup_old_posts`
- `posts.tasks.generate_content_analytics`
- `posts.tasks.update_post_engagement_scores`
- `posts.tasks.send_content_digest_email`

### Schedule Management

#### Crontab Schedules
- **Minute:** 0-59 or * for any
- **Hour:** 0-23 or * for any
- **Day of Week:** 0-6 (Sunday=0) or * for any
- **Day of Month:** 1-31 or * for any
- **Month of Year:** 1-12 or * for any

**Common Examples:**
- Daily at 2 AM: `0 2 * * *`
- Every hour: `0 * * * *`
- Weekly on Monday: `0 9 * * 1`
- Monthly on 1st: `0 0 1 * *`

#### Interval Schedules
- **Every:** Number of periods
- **Period:** seconds, minutes, hours, days

**Examples:**
- Every 30 minutes: `30 minutes`
- Every 2 hours: `2 hours`
- Every day: `1 days`

### Task Monitoring

#### Task Status
- **Green dot:** Task is enabled and running
- **Red dot:** Task is disabled
- **Last Run:** Shows when task last executed
- **Total Runs:** Shows execution count

#### Troubleshooting Tasks
1. **Task not running:**
   - Check if task is enabled
   - Verify Celery worker is running
   - Check task schedule is correct
   - Review Celery logs

2. **Task failing:**
   - Check task arguments are correct
   - Verify task function exists
   - Review error logs in Celery worker
   - Test task manually in Django shell

3. **Schedule issues:**
   - Verify crontab syntax
   - Check timezone settings
   - Ensure schedule is in the future

### Best Practices

#### Task Management
1. **Naming:** Use descriptive task names
2. **Documentation:** Add descriptions to tasks
3. **Testing:** Test tasks before enabling
4. **Monitoring:** Regularly check task execution
5. **Cleanup:** Remove unused tasks

#### Security
1. **Access Control:** Limit admin access
2. **Task Validation:** Validate task arguments
3. **Resource Limits:** Set appropriate timeouts
4. **Logging:** Monitor task execution

### Setup Instructions

If Celery admin is not visible:

1. **Install django-celery-beat:**
   ```bash
   python scripts/utils/SETUP_CELERY_ADMIN.py
   ```

2. **Manual setup:**
   ```bash
   poetry install  # Installs django-celery-beat
   python manage.py migrate django_celery_beat
   ```

3. **Restart Django:**
   ```bash
   docker-compose restart web
   ```

### External Resources
- **Django Admin Documentation:** https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
- **Django Celery Beat:** https://django-celery-beat.readthedocs.io/
- **Celery Documentation:** https://docs.celeryproject.org/
- **GraphQL Documentation:** https://graphql.org/learn/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

*Last updated: January 10, 2025*  
*Admin Guide Version: 1.0.0*
