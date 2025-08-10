"""
URLs configuration for social_media_backend project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# Import GraphQL schema
try:
    from .schema import schema
except ImportError:
    schema = None

# Try to import optional views with fallbacks
try:
    from . import api_views
except ImportError:
    api_views = None

try:
    from .simple_swagger import simple_swagger_docs
except ImportError:
    simple_swagger_docs = None

try:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView
    )
except ImportError:
    SpectacularAPIView = None
    SpectacularSwaggerView = None
    SpectacularRedocView = None

try:
    from . import swagger_views
except ImportError:
    swagger_views = None

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

# Basic URL patterns that should always work
urlpatterns = [
    # Root endpoint
    path('', root_view, name='root'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # GraphQL endpoint (main API)
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='graphql'),
]

# Add optional API documentation endpoints if modules are available
if api_views:
    urlpatterns.extend([
        path('api/graphql-docs/', api_views.graphql_endpoint_docs, name='graphql-docs'),
        path('api/auth/', api_views.auth_info, name='auth-info'),
        path('api/stats/', api_views.platform_stats, name='platform-stats'),
        path('api/health/', api_views.health_check, name='health-check'),
        path('api/schema-info/', api_views.api_schema, name='api-schema'),
        path('api/errors/', api_views.error_handling_guide, name='error-guide'),
    ])

if swagger_views:
    urlpatterns.append(
        path('api/error-handling/', swagger_views.error_handling_documentation, name='error-handling-docs')
    )

if simple_swagger_docs:
    urlpatterns.append(
        path('api/docs/', simple_swagger_docs, name='api-docs')
    )

# Add Spectacular views if available
if SpectacularAPIView and SpectacularSwaggerView and SpectacularRedocView:
    urlpatterns.extend([
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ])

# Serve static and media files (WhiteNoise handles static files in production)
# Always serve media files for user uploads
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static files are handled by WhiteNoise middleware in production
# But we add this for development compatibility
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
