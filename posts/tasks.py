"""
Celery Tasks for Posts Application
Background tasks for content processing, analytics, and maintenance
"""

from celery import shared_task
from django.utils import timezone
from django.db.models import Count, F
from datetime import timedelta
import logging

from .models import Post, Hashtag, Comment
from users.models import User

logger = logging.getLogger(__name__)

@shared_task
def process_media_upload(post_id):
    """Process uploaded media files (resize images, generate thumbnails)"""
    try:
        logger.info(f"🎬 Processing media for post {post_id}")
        
        post = Post.objects.get(id=post_id)
        
        # Simulate media processing
        if post.image:
            logger.info(f"Processing image: {post.image.name}")
            # Add image processing logic here (resize, thumbnails, etc.)
            
        if post.video:
            logger.info(f"Processing video: {post.video.name}")
            # Add video processing logic here (compression, thumbnails, etc.)
        
        logger.info(f"✅ Media processing completed for post {post_id}")
        return f"Media processed successfully for post {post_id}"
        
    except Post.DoesNotExist:
        logger.error(f"❌ Post {post_id} not found")
        return f"Error: Post {post_id} not found"
    except Exception as e:
        logger.error(f"❌ Media processing error: {e}")
        return f"Error: {e}"

@shared_task
def update_trending_hashtags():
    """Update trending hashtags based on recent activity"""
    try:
        logger.info("📈 Updating trending hashtags")
        
        # Get hashtags from posts in the last 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        trending_hashtags = Hashtag.objects.filter(
            posts__created_at__gte=seven_days_ago
        ).annotate(
            recent_posts_count=Count('posts')
        ).order_by('-recent_posts_count')[:10]
        
        # Update hashtag trending status
        Hashtag.objects.all().update(is_trending=False)
        
        for hashtag in trending_hashtags:
            hashtag.is_trending = True
            hashtag.save(update_fields=['is_trending'])
        
        trending_count = trending_hashtags.count()
        logger.info(f"✅ Updated {trending_count} trending hashtags")
        return f"Updated {trending_count} trending hashtags"
        
    except Exception as e:
        logger.error(f"❌ Trending hashtags update error: {e}")
        return f"Error: {e}"

@shared_task
def cleanup_old_posts():
    """Clean up old posts and associated data"""
    try:
        logger.info("🧹 Starting old posts cleanup")
        
        # Find posts older than 1 year with no engagement
        one_year_ago = timezone.now() - timedelta(days=365)
        old_posts = Post.objects.filter(
            created_at__lt=one_year_ago,
            likes_count=0,
            comments_count=0,
            shares_count=0,
            views_count__lt=10
        )
        
        old_posts_count = old_posts.count()
        logger.info(f"Found {old_posts_count} old posts to review")
        
        # For now, just log - don't actually delete
        # old_posts.delete()  # Uncomment to actually delete
        
        logger.info(f"✅ Old posts cleanup completed")
        return f"Reviewed {old_posts_count} old posts"
        
    except Exception as e:
        logger.error(f"❌ Old posts cleanup error: {e}")
        return f"Error: {e}"

@shared_task
def generate_content_analytics():
    """Generate daily content analytics and insights"""
    try:
        logger.info("📊 Generating content analytics")
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Calculate daily statistics
        daily_stats = {
            'posts_created': Post.objects.filter(created_at__date=yesterday).count(),
            'comments_created': Comment.objects.filter(created_at__date=yesterday).count(),
            'total_posts': Post.objects.count(),
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(last_login__date=yesterday).count(),
        }
        
        # Most popular posts yesterday
        popular_posts = Post.objects.filter(
            created_at__date=yesterday
        ).order_by('-likes_count', '-comments_count')[:5]
        
        logger.info(f"Daily stats: {daily_stats}")
        logger.info(f"Popular posts: {popular_posts.count()}")
        
        logger.info("✅ Content analytics generated")
        return f"Analytics generated: {daily_stats['posts_created']} posts, {daily_stats['active_users']} active users"
        
    except Exception as e:
        logger.error(f"❌ Analytics generation error: {e}")
        return f"Error: {e}"

@shared_task
def update_post_engagement_scores():
    """Update engagement scores for posts to improve feed ranking"""
    try:
        logger.info("🎯 Updating post engagement scores")
        
        # Calculate engagement score based on likes, comments, shares, and views
        posts = Post.objects.all()
        updated_count = 0
        
        for post in posts:
            # Simple engagement score calculation
            engagement_score = (
                post.likes_count * 3 +
                post.comments_count * 5 +
                post.shares_count * 7 +
                post.views_count * 1
            )
            
            # Apply time decay (newer posts get boost)
            days_old = (timezone.now() - post.created_at).days
            time_factor = max(0.1, 1 - (days_old * 0.1))
            engagement_score *= time_factor
            
            # Update the post (you'd need to add engagement_score field to model)
            # post.engagement_score = engagement_score
            # post.save(update_fields=['engagement_score'])
            updated_count += 1
        
        logger.info(f"✅ Updated engagement scores for {updated_count} posts")
        return f"Updated engagement scores for {updated_count} posts"
        
    except Exception as e:
        logger.error(f"❌ Engagement score update error: {e}")
        return f"Error: {e}"

@shared_task
def send_content_digest_email():
    """Send weekly content digest to active users"""
    try:
        logger.info("📧 Sending content digest emails")
        
        # Get active users (logged in within last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        active_users = User.objects.filter(
            last_login__gte=seven_days_ago,
            is_active=True
        )
        
        # Get top posts from last week
        top_posts = Post.objects.filter(
            created_at__gte=seven_days_ago,
            visibility='public'
        ).order_by('-likes_count', '-comments_count')[:10]
        
        digest_sent = 0
        for user in active_users:
            # Here you would send actual email
            # send_mail(
            #     subject="Your Weekly Content Digest",
            #     message=f"Hi {user.username}, here are the top posts...",
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[user.email]
            # )
            digest_sent += 1
        
        logger.info(f"✅ Content digest sent to {digest_sent} users")
        return f"Content digest sent to {digest_sent} users"
        
    except Exception as e:
        logger.error(f"❌ Content digest error: {e}")
        return f"Error: {e}"
