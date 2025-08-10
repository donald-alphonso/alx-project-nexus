"""
Custom Celery Admin Configuration
Enhanced admin interface for Celery task management
"""

from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask, CrontabSchedule, IntervalSchedule, 
    SolarSchedule, ClockedSchedule
)
from django_celery_beat.admin import (
    PeriodicTaskAdmin as BasePeriodicTaskAdmin,
    TaskSelectWidget
)
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe


class CustomPeriodicTaskAdmin(BasePeriodicTaskAdmin):
    """
    Enhanced Periodic Task Admin with better interface
    """
    list_display = (
        'name', 'task_name', 'enabled', 'schedule_type', 
        'last_run_at', 'total_run_count', 'task_actions'
    )
    list_filter = ('enabled', 'one_off', 'last_run_at')
    search_fields = ('name', 'task')
    ordering = ('-last_run_at',)
    
    fieldsets = (
        ('Task Information', {
            'fields': ('name', 'task', 'enabled', 'description')
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab', 'solar', 'clocked', 'one_off')
        }),
        ('Arguments', {
            'fields': ('args', 'kwargs'),
            'classes': ('collapse',)
        }),
        ('Execution Options', {
            'fields': ('queue', 'exchange', 'routing_key', 'priority', 'expires'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('last_run_at', 'total_run_count', 'date_changed'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_run_at', 'total_run_count', 'date_changed')
    
    def schedule_type(self, obj):
        """Display the type of schedule"""
        if obj.interval:
            return format_html('<span style="color: green;">Interval</span>')
        elif obj.crontab:
            return format_html('<span style="color: blue;">Crontab</span>')
        elif obj.solar:
            return format_html('<span style="color: orange;">Solar</span>')
        elif obj.clocked:
            return format_html('<span style="color: red;">Clocked</span>')
        else:
            return format_html('<span style="color: gray;">None</span>')
    schedule_type.short_description = 'Schedule Type'
    
    def task_actions(self, obj):
        """Add action buttons for tasks"""
        if obj.enabled:
            disable_url = reverse('admin:django_celery_beat_periodictask_change', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}">Edit</a> '
                '<span style="color: green;">●</span> Active',
                disable_url
            )
        else:
            enable_url = reverse('admin:django_celery_beat_periodictask_change', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}">Edit</a> '
                '<span style="color: red;">●</span> Inactive',
                enable_url
            )
    task_actions.short_description = 'Actions'
    task_actions.allow_tags = True


class CustomCrontabScheduleAdmin(admin.ModelAdmin):
    """
    Enhanced Crontab Schedule Admin
    """
    list_display = ('__str__', 'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')
    list_filter = ('hour', 'day_of_week')
    search_fields = ('minute', 'hour')
    
    fieldsets = (
        ('Schedule Definition', {
            'fields': ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year'),
            'description': 'Define when the task should run using cron syntax'
        }),
        ('Timezone', {
            'fields': ('timezone',),
            'classes': ('collapse',)
        }),
    )


class CustomIntervalScheduleAdmin(admin.ModelAdmin):
    """
    Enhanced Interval Schedule Admin
    """
    list_display = ('__str__', 'every', 'period')
    list_filter = ('period',)
    search_fields = ('every',)
    
    fieldsets = (
        ('Interval Definition', {
            'fields': ('every', 'period'),
            'description': 'Define how often the task should run'
        }),
    )


# Unregister default admin classes
admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)

# Register custom admin classes
admin.site.register(PeriodicTask, CustomPeriodicTaskAdmin)
admin.site.register(CrontabSchedule, CustomCrontabScheduleAdmin)
admin.site.register(IntervalSchedule, CustomIntervalScheduleAdmin)

# Keep default registration for other models
# SolarSchedule and ClockedSchedule use default admin
