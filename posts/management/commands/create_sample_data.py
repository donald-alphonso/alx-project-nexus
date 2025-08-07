"""
Django management command to create sample data for testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from users.models import User, Follow
from posts.models import Post, Comment, Hashtag, PostHashtag
from interactions.models import Like, Share, Bookmark, Notification
import random


class Command(BaseCommand):
    help = 'Create sample data for testing the social media backend'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=50,
            help='Number of posts to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create users
        users_count = options['users']
        users = self.create_users(users_count)
        self.stdout.write(f'Created {len(users)} users')
        
        # Create follows
        follows = self.create_follows(users)
        self.stdout.write(f'Created {len(follows)} follow relationships')
        
        # Create hashtags
        hashtags = self.create_hashtags()
        self.stdout.write(f'Created {len(hashtags)} hashtags')
        
        # Create posts
        posts_count = options['posts']
        posts = self.create_posts(users, hashtags, posts_count)
        self.stdout.write(f'Created {len(posts)} posts')
        
        # Create comments
        comments = self.create_comments(users, posts)
        self.stdout.write(f'Created {len(comments)} comments')
        
        # Create interactions
        likes, shares, bookmarks = self.create_interactions(users, posts, comments)
        self.stdout.write(f'Created {len(likes)} likes, {len(shares)} shares, {len(bookmarks)} bookmarks')
        
        # Create notifications
        notifications = self.create_notifications(users, posts)
        self.stdout.write(f'Created {len(notifications)} notifications')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created all sample data!')
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        for i in range(count):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=f'User{i+1}',
                    last_name='Test',
                    bio=f'This is the bio for {username}. I love social media!',
                    location=random.choice(['New York', 'London', 'Paris', 'Tokyo', 'Sydney'])
                )
                users.append(user)
        return users

    def create_follows(self, users):
        """Create follow relationships"""
        follows = []
        for user in users:
            # Each user follows 2-5 random other users
            follow_count = random.randint(2, min(5, len(users) - 1))
            potential_follows = [u for u in users if u != user]
            to_follow = random.sample(potential_follows, follow_count)
            
            for target in to_follow:
                follow, created = Follow.objects.get_or_create(
                    follower=user,
                    following=target
                )
                if created:
                    follows.append(follow)
                    # Update counts
                    user.following_count += 1
                    target.followers_count += 1
            
            user.save(update_fields=['following_count'])
        
        # Update followers count for all users
        for user in users:
            user.save(update_fields=['followers_count'])
        
        return follows

    def create_hashtags(self):
        """Create sample hashtags"""
        hashtag_names = [
            'python', 'django', 'graphql', 'coding', 'programming',
            'webdev', 'backend', 'api', 'database', 'tech',
            'socialmedia', 'innovation', 'startup', 'ai', 'ml'
        ]
        
        hashtags = []
        for name in hashtag_names:
            hashtag, created = Hashtag.objects.get_or_create(name=name)
            if created:
                hashtags.append(hashtag)
        
        return hashtags

    def create_posts(self, users, hashtags, count):
        """Create sample posts"""
        post_contents = [
            "Just finished building an amazing GraphQL API! 🚀",
            "Django is such a powerful framework for backend development.",
            "Working on some exciting new features today!",
            "Love how clean and organized this codebase is turning out.",
            "GraphQL makes data fetching so much more efficient.",
            "Building scalable social media backends is challenging but fun!",
            "PostgreSQL + Django = Perfect combination 💪",
            "Celery tasks are running smoothly in the background.",
            "API optimization is an art form.",
            "Clean code is not written by following a set of rules.",
        ]
        
        posts = []
        for i in range(count):
            author = random.choice(users)
            content = random.choice(post_contents)
            visibility = random.choice(['public', 'public', 'public', 'followers'])  # Mostly public
            
            post = Post.objects.create(
                author=author,
                content=f"{content} #{i+1}",
                visibility=visibility
            )
            
            # Add random hashtags to posts
            post_hashtags = random.sample(hashtags, random.randint(1, 3))
            for hashtag in post_hashtags:
                PostHashtag.objects.create(post=post, hashtag=hashtag)
                hashtag.posts_count += 1
                hashtag.save(update_fields=['posts_count'])
            
            # Update author's post count
            author.posts_count += 1
            author.save(update_fields=['posts_count'])
            
            posts.append(post)
        
        return posts

    def create_comments(self, users, posts):
        """Create sample comments"""
        comment_contents = [
            "Great post!",
            "I totally agree with this.",
            "Thanks for sharing!",
            "This is really helpful.",
            "Interesting perspective.",
            "Love this approach!",
            "Well said!",
            "This made my day.",
            "Couldn't agree more.",
            "Awesome work!"
        ]
        
        comments = []
        for post in posts:
            # Each post gets 0-5 comments
            comment_count = random.randint(0, 5)
            for _ in range(comment_count):
                author = random.choice(users)
                content = random.choice(comment_contents)
                
                comment = Comment.objects.create(
                    post=post,
                    author=author,
                    content=content
                )
                
                # Update post comment count
                post.comments_count += 1
                
                comments.append(comment)
            
            post.save(update_fields=['comments_count'])
        
        return comments

    def create_interactions(self, users, posts, comments):
        """Create likes, shares, and bookmarks"""
        likes = []
        shares = []
        bookmarks = []
        
        post_content_type = ContentType.objects.get_for_model(Post)
        comment_content_type = ContentType.objects.get_for_model(Comment)
        
        # Create post likes
        for post in posts:
            # Each post gets 0-10 likes
            like_count = random.randint(0, 10)
            likers = random.sample(users, min(like_count, len(users)))
            
            for user in likers:
                like, created = Like.objects.get_or_create(
                    user=user,
                    content_type=post_content_type,
                    object_id=post.id
                )
                if created:
                    likes.append(like)
                    post.likes_count += 1
            
            post.save(update_fields=['likes_count'])
        
        # Create comment likes
        for comment in comments:
            # Each comment gets 0-3 likes
            like_count = random.randint(0, 3)
            likers = random.sample(users, min(like_count, len(users)))
            
            for user in likers:
                like, created = Like.objects.get_or_create(
                    user=user,
                    content_type=comment_content_type,
                    object_id=comment.id
                )
                if created:
                    likes.append(like)
                    comment.likes_count += 1
            
            comment.save(update_fields=['likes_count'])
        
        # Create shares
        for post in posts:
            # Each post gets 0-3 shares
            share_count = random.randint(0, 3)
            sharers = random.sample(users, min(share_count, len(users)))
            
            for user in sharers:
                share, created = Share.objects.get_or_create(
                    user=user,
                    post=post,
                    defaults={'share_type': 'repost'}
                )
                if created:
                    shares.append(share)
                    post.shares_count += 1
            
            post.save(update_fields=['shares_count'])
        
        # Create bookmarks
        for user in users:
            # Each user bookmarks 0-5 posts
            bookmark_count = random.randint(0, 5)
            posts_to_bookmark = random.sample(posts, min(bookmark_count, len(posts)))
            
            for post in posts_to_bookmark:
                bookmark, created = Bookmark.objects.get_or_create(
                    user=user,
                    post=post
                )
                if created:
                    bookmarks.append(bookmark)
        
        return likes, shares, bookmarks

    def create_notifications(self, users, posts):
        """Create sample notifications"""
        notifications = []
        post_content_type = ContentType.objects.get_for_model(Post)
        
        for user in users:
            # Each user gets 2-8 notifications
            notification_count = random.randint(2, 8)
            
            for _ in range(notification_count):
                sender = random.choice([u for u in users if u != user])
                post = random.choice(posts)
                notification_type = random.choice(['like', 'comment', 'share', 'follow'])
                
                messages = {
                    'like': f"{sender.username} liked your post",
                    'comment': f"{sender.username} commented on your post",
                    'share': f"{sender.username} shared your post",
                    'follow': f"{sender.username} started following you"
                }
                
                notification = Notification.objects.create(
                    recipient=user,
                    sender=sender,
                    notification_type=notification_type,
                    message=messages[notification_type],
                    content_type=post_content_type if notification_type != 'follow' else None,
                    object_id=post.id if notification_type != 'follow' else None,
                    is_read=random.choice([True, False])
                )
                notifications.append(notification)
        
        return notifications
