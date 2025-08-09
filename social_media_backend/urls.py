"""
URLs configuration for social_media_backend project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# Import API views
from . import api_views
from .simple_swagger import simple_swagger_docs

# Import Swagger views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

# Import advanced Swagger views
from . import swagger_views

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

urlpatterns = [
    # Root endpoint
    path('', root_view, name='root'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # GraphQL endpoint (main API)
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphql'),
    
    # API Documentation endpoints
    path('api/graphql-docs/', api_views.graphql_endpoint_docs, name='graphql-docs'),
    path('api/auth/', api_views.auth_info, name='auth-info'),
    path('api/stats/', api_views.platform_stats, name='platform-stats'),
    path('api/health/', api_views.health_check, name='health-check'),
    path('api/schema-info/', api_views.api_schema, name='api-schema'),
    path('api/errors/', api_views.error_handling_guide, name='error-guide'),
    
    # Advanced Error Handling Documentation
    path('api/error-handling/', swagger_views.error_handling_documentation, name='error-handling-docs'),
    
    # API Documentation (Simple and reliable)
    path('api/docs/', simple_swagger_docs, name='api-docs'),
    
    # Swagger/OpenAPI documentation (Production-ready)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
