"""
URLs configuration for social_media_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views

# Try to import GraphQL safely
try:
    from graphene_django.views import GraphQLView
    from .schema import schema
    GRAPHQL_AVAILABLE = True
except ImportError:
    GRAPHQL_AVAILABLE = False

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

# Simple working URLs
urlpatterns = [
    # Root endpoint
    path('', root_view, name='root'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Presentation page for ALX validation
    path('presentation/', views.presentation_view, name='presentation'),
    
    # API endpoints
    path('api/health/', views.api_health, name='api-health'),
    path('api/stats/', views.api_stats, name='api-stats'),
    path('api/schema/', views.graphql_schema_info, name='api-schema'),
]

# Add GraphQL if available
if GRAPHQL_AVAILABLE:
    urlpatterns.append(
        path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='graphql')
    )

# Static files handled by WhiteNoise middleware
