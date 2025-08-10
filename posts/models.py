"""
Post models for the social media backend.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    """
    Model representing a social media post.
    """
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('followers', 'Followers Only'),
        ('private', 'Private'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=2200)
    image = models.ImageField(
        upload_to='posts/images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    video = models.FileField(
        upload_to='posts/videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv'])]
    )
    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='public'
    )
    is_pinned = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['visibility', '-created_at']),
        ]

    def __str__(self):
        return f"Post by @{self.author.username} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def has_media(self):
        """Check if post has any media attachments."""
        return bool(self.image or self.video)

    def get_media_url(self):
        """Return the media URL if available."""
        if self.image:
            return self.image.url
        elif self.video:
            return self.video.url
        return None


class Comment(models.Model):
    """
    Model representing comments on posts.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies'
    )
    content = models.TextField(max_length=1000)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return f"Comment by @{self.author.username} on {self.post}"

    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment."""
        return self.parent is not None


class Hashtag(models.Model):
    """
    Model representing hashtags used in posts.
    """
    name = models.CharField(max_length=100, unique=True)
    posts_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hashtags'
        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'
        ordering = ['-posts_count', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-posts_count']),
        ]

    def __str__(self):
        return f"#{self.name}"


class PostHashtag(models.Model):
    """
    Model representing the many-to-many relationship between posts and hashtags.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_hashtags'
        unique_together = ('post', 'hashtag')
        verbose_name = 'Post Hashtag'
        verbose_name_plural = 'Post Hashtags'

    def __str__(self):
        return f"{self.post} - {self.hashtag}"
