"""
Admin configuration for Posts app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, Hashtag, PostHashtag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post Admin
    """
    list_display = (
        'id', 'author', 'content_preview', 'visibility', 
        'likes_count', 'comments_count', 'shares_count', 
        'views_count', 'created_at'
    )
    list_filter = ('visibility', 'is_pinned', 'created_at')
    search_fields = ('content', 'author__username')
    ordering = ('-created_at',)
    readonly_fields = (
        'likes_count', 'comments_count', 'shares_count', 
        'views_count', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('Content', {
            'fields': ('author', 'content', 'image', 'video')
        }),
        ('Settings', {
            'fields': ('visibility', 'is_pinned')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'comments_count', 'shares_count', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def content_preview(self, obj):
        """Show preview of post content"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Comment Admin
    """
    list_display = (
        'id', 'author', 'post', 'content_preview', 
        'parent', 'likes_count', 'created_at'
    )
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('likes_count', 'created_at', 'updated_at')
    
    def content_preview(self, obj):
        """Show preview of comment content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'parent')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    """
    Hashtag Admin
    """
    list_display = ('name', 'posts_count', 'created_at')
    search_fields = ('name',)
    ordering = ('-posts_count', 'name')
    readonly_fields = ('posts_count', 'created_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(PostHashtag)
class PostHashtagAdmin(admin.ModelAdmin):
    """
    PostHashtag relationship admin
    """
    list_display = ('post', 'hashtag', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__content', 'hashtag__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'hashtag')
