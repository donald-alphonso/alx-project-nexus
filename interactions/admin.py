"""
Admin configuration for Interactions app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Like, Share, Bookmark, Notification, Report


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Like Admin
    """
    list_display = ('user', 'content_type', 'object_id', 'content_object', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    """
    Share Admin
    """
    list_display = ('user', 'post', 'share_type', 'created_at')
    list_filter = ('share_type', 'created_at')
    search_fields = ('user__username', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Share Information', {
            'fields': ('user', 'post', 'share_type')
        }),
        ('Comment', {
            'fields': ('comment',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """
    Bookmark Admin
    """
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Notification Admin
    """
    list_display = (
        'recipient', 'sender', 'notification_type', 
        'message_preview', 'is_read', 'created_at'
    )
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'sender', 'notification_type', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Related Object', {
            'fields': ('content_type', 'object_id')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def message_preview(self, obj):
        """Show preview of notification message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'sender', 'content_type')
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = 'Mark selected notifications as unread'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Report Admin
    """
    list_display = (
        'reporter', 'reason', 'status', 'content_type', 
        'object_id', 'created_at'
    )
    list_filter = ('reason', 'status', 'content_type', 'created_at')
    search_fields = ('reporter__username', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('reporter', 'reason', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Reported Object', {
            'fields': ('content_type', 'object_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reporter', 'content_type')
    
    actions = ['mark_as_reviewed', 'mark_as_resolved', 'mark_as_dismissed']
    
    def mark_as_reviewed(self, request, queryset):
        """Mark selected reports as reviewed"""
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} reports marked as reviewed.')
    mark_as_reviewed.short_description = 'Mark selected reports as reviewed'
    
    def mark_as_resolved(self, request, queryset):
        """Mark selected reports as resolved"""
        updated = queryset.update(status='resolved')
        self.message_user(request, f'{updated} reports marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected reports as resolved'
    
    def mark_as_dismissed(self, request, queryset):
        """Mark selected reports as dismissed"""
        updated = queryset.update(status='dismissed')
        self.message_user(request, f'{updated} reports marked as dismissed.')
    mark_as_dismissed.short_description = 'Mark selected reports as dismissed'
