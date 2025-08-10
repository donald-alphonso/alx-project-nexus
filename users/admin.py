"""
Admin configuration for Users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Follow


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin
    """
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'is_verified', 'followers_count', 'following_count', 
        'posts_count', 'created_at'
    )
    list_filter = (
        'is_verified', 'is_staff', 'is_superuser', 
        'is_active', 'created_at'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = (
        'followers_count', 'following_count', 'posts_count', 
        'created_at', 'updated_at'
    )
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'avatar', 'birth_date', 'location', 'website')
        }),
        ('Social Stats', {
            'fields': ('is_verified', 'followers_count', 'following_count', 'posts_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Follow relationship admin
    """
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('follower', 'following')
