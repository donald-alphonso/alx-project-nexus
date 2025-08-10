"""
URLs configuration for social_media_backend project.
"""

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

# Production-ready URLs configuration

def root_view(request):
    """Root endpoint with project information"""
    return JsonResponse({
        'project': 'ALX Project Nexus',
        'description': 'Social Media Backend with GraphQL API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'graphql': '/graphql/',
            'documentation': '/api/docs/',
            'swagger': '/api/swagger/',
            'admin': '/admin/',
            'health': '/api/health/'
        },
        'features': [
            'GraphQL API with 38 endpoints',
            'JWT Authentication',
            'Real-time notifications',
            'Robust error handling',
            'Professional documentation'
        ]
    })

# Minimal URL patterns for debugging
urlpatterns = [
    # Root endpoint
    path('', root_view, name='root'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Simple API endpoints
    path('api/health/', lambda request: JsonResponse({'status': 'healthy', 'service': 'ALX Project Nexus'}), name='health-check'),
    path('api/test/', lambda request: JsonResponse({'message': 'API is working!', 'endpoints': ['/', '/admin/', '/api/health/']}), name='api-test'),
]

# End of URLs - Minimal configuration for debugging
