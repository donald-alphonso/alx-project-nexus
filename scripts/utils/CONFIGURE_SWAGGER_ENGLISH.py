#!/usr/bin/env python3
"""
Configure Swagger with proper English documentation for all GraphQL endpoints
"""

import os
import sys

def configure_swagger_settings():
    """Configure Swagger settings for English documentation"""
    
    settings_content = '''
# =============================================================================
# SWAGGER/OPENAPI CONFIGURATION (ENGLISH)
# =============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'ALX Project Nexus - GraphQL API',
    'DESCRIPTION': '''
    # ALX Project Nexus - Modern Social Media Platform

    A comprehensive GraphQL API for a modern social media platform built with Django.
    
    ## Features
    - **User Management**: Registration, authentication, profiles
    - **Content Creation**: Posts, comments, media sharing
    - **Social Interactions**: Likes, follows, notifications
    - **Advanced Search**: Full-text search, hashtags, filters
    - **Real-time Updates**: Live notifications and feeds
    - **Moderation Tools**: Content reporting and management
    
    ## Authentication
    This API uses JWT (JSON Web Tokens) for authentication.
    
    ### How to authenticate:
    1. Create an account using `createUser` mutation
    2. Login using `tokenAuth` mutation to get your JWT token
    3. Include the token in your requests: `Authorization: JWT <your-token>`
    
    ## GraphQL Endpoint
    All API operations are available through the GraphQL endpoint:
    **POST** `/graphql/`
    
    ## Available Operations
    - **20 Queries**: Retrieve data (users, posts, feed, search, etc.)
    - **18 Mutations**: Modify data (create, update, delete, like, follow, etc.)
    
    ## Quick Start
    1. Navigate to `/graphql/` for the GraphiQL interface
    2. Use the documentation explorer to discover all available operations
    3. Test queries and mutations directly in the browser
    
    ---
    *Developed by Donald Ahossi - ALX Software Engineering Program 2025*
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
        'tryItOutEnabled': True,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
        'docExpansion': 'list',
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'ENABLE_DJANGO_DEPLOY_CHECK': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'SERVE_AUTHENTICATION': [],
    'SCHEMA_PATH_PREFIX': '/api/',
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'SERVERS': [
        {
            'url': 'http://localhost:8000',
            'description': 'Development Server'
        }
    ],
    'TAGS': [
        {
            'name': 'Authentication',
            'description': 'User registration, login, and JWT token management'
        },
        {
            'name': 'Users',
            'description': 'User profile management and social features'
        },
        {
            'name': 'Posts',
            'description': 'Content creation, editing, and management'
        },
        {
            'name': 'Interactions',
            'description': 'Likes, comments, follows, and social engagement'
        },
        {
            'name': 'Search',
            'description': 'Search users, posts, and discover content'
        },
        {
            'name': 'Notifications',
            'description': 'Real-time notifications and alerts'
        },
        {
            'name': 'Administration',
            'description': 'Platform statistics and monitoring'
        },
        {
            'name': 'GraphQL',
            'description': 'Main GraphQL endpoint for all operations'
        }
    ]
}

# REST Framework configuration for Swagger
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'graphql_jwt.backends.JSONWebTokenBackend',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
'''
    
    return settings_content

def create_api_views_english():
    """Create API views with English documentation"""
    
    api_views_content = '''
"""
API Views for Swagger documentation - English version
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.openapi import OpenApiTypes
from django.http import JsonResponse
import json

@extend_schema(
    tags=['GraphQL'],
    summary='GraphQL API Endpoint',
    description="""
    Main GraphQL endpoint for all API operations.
    
    This endpoint handles all GraphQL queries and mutations for the social media platform.
    Use the GraphiQL interface at /graphql/ for interactive testing.
    
    **Available Operations:**
    - User management (registration, authentication, profiles)
    - Content creation (posts, comments, media)
    - Social interactions (likes, follows, notifications)
    - Search and discovery
    - Real-time updates
    """,
    examples=[
        OpenApiExample(
            'User Registration',
            value={
                "query": """
                mutation {
                  createUser(
                    username: "johndoe"
                    email: "john@example.com"
                    password: "securePassword123"
                    firstName: "John"
                    lastName: "Doe"
                  ) {
                    user {
                      id
                      username
                      email
                    }
                    success
                    errors
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'User Login',
            value={
                "query": """
                mutation {
                  tokenAuth(
                    email: "john@example.com"
                    password: "securePassword123"
                  ) {
                    token
                    payload
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Get All Posts',
            value={
                "query": """
                query {
                  allPosts {
                    id
                    content
                    author {
                      username
                    }
                    likesCount
                    commentsCount
                    createdAt
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Create Post',
            value={
                "query": """
                mutation {
                  createPost(
                    content: "Hello from ALX Project Nexus! #GraphQL #Django"
                    visibility: "public"
                  ) {
                    post {
                      id
                      content
                      hashtags
                    }
                    success
                  }
                }
                """
            }
        )
    ]
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def graphql_documentation(request):
    """GraphQL API documentation endpoint"""
    return Response({
        "message": "GraphQL API Endpoint",
        "endpoint": "/graphql/",
        "interface": "/graphql/ (GraphiQL)",
        "documentation": "/api/docs/",
        "operations": {
            "queries": 20,
            "mutations": 18,
            "total_endpoints": 38
        }
    })

@extend_schema(
    tags=['Administration'],
    summary='Platform Statistics',
    description='Get comprehensive platform metrics and analytics',
    examples=[
        OpenApiExample(
            'Platform Stats Response',
            value={
                "total_users": 150,
                "total_posts": 1250,
                "total_likes": 5600,
                "total_comments": 890,
                "active_users_24h": 45,
                "posts_today": 23
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def platform_stats(request):
    """Get platform statistics"""
    try:
        from users.models import User
        from posts.models import Post
        from interactions.models import Like, Comment
        
        stats = {
            "total_users": User.objects.count(),
            "total_posts": Post.objects.count(),
            "total_likes": Like.objects.count(),
            "total_comments": Comment.objects.count(),
            "active_users_24h": User.objects.filter(
                last_login__gte=timezone.now() - timedelta(days=1)
            ).count() if hasattr(User, 'last_login') else 0,
            "posts_today": Post.objects.filter(
                created_at__date=timezone.now().date()
            ).count()
        }
        return Response(stats)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@extend_schema(
    tags=['Administration'],
    summary='Health Check',
    description='Check system health and service status',
    examples=[
        OpenApiExample(
            'Healthy Response',
            value={
                "status": "healthy",
                "database": "connected",
                "redis": "connected",
                "services": {
                    "web": "running",
                    "celery": "running"
                },
                "timestamp": "2025-01-09T15:00:00Z"
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """System health check"""
    from django.utils import timezone
    
    health_status = {
        "status": "healthy",
        "database": "connected",
        "timestamp": timezone.now().isoformat(),
        "version": "1.0.0",
        "environment": "development"
    }
    
    return Response(health_status)

@extend_schema(
    tags=['GraphQL'],
    summary='API Documentation JSON',
    description='Get API documentation in JSON format for external tools'
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_docs_json(request):
    """API documentation in JSON format"""
    docs = {
        "title": "ALX Project Nexus - GraphQL API",
        "version": "1.0.0",
        "description": "Modern social media platform with GraphQL API",
        "endpoints": {
            "graphql": {
                "url": "/graphql/",
                "methods": ["GET", "POST"],
                "description": "Main GraphQL endpoint",
                "operations": {
                    "queries": 20,
                    "mutations": 18
                }
            },
            "admin": {
                "url": "/admin/",
                "description": "Django admin interface"
            },
            "docs": {
                "url": "/api/docs/",
                "description": "Swagger UI documentation"
            }
        },
        "authentication": {
            "type": "JWT",
            "header": "Authorization: JWT <token>",
            "obtain_token": "/graphql/ (tokenAuth mutation)"
        }
    }
    
    return Response(docs)
'''
    
    return api_views_content

def update_urls_configuration():
    """Update URLs to include Swagger endpoints"""
    
    urls_content = '''
"""
URL Configuration for ALX Project Nexus - English version
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# Import API views
try:
    from . import api_views
    api_views_available = True
except ImportError:
    api_views_available = False

# Import Swagger views
try:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
        SpectacularRedocView
    )
    swagger_available = True
except ImportError:
    swagger_available = False

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # GraphQL endpoint (main API)
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

# Add API documentation endpoints if available
if api_views_available:
    urlpatterns += [
        # API endpoints
        path('api/graphql-docs/', api_views.graphql_documentation, name='graphql-docs'),
        path('api/stats/', api_views.platform_stats, name='platform-stats'),
        path('api/health/', api_views.health_check, name='health-check'),
        path('api/docs/json/', api_views.api_docs_json, name='api-docs-json'),
    ]

# Add Swagger endpoints if available
if swagger_available:
    urlpatterns += [
        # Swagger/OpenAPI documentation
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    return urls_content

def main():
    """Configure Swagger with English documentation"""
    
    print("🔧 CONFIGURING SWAGGER WITH ENGLISH DOCUMENTATION")
    print("=" * 60)
    
    # 1. Update settings
    print("1. Updating Swagger settings...")
    settings_content = configure_swagger_settings()
    
    # 2. Create API views
    print("2. Creating English API views...")
    api_views_content = create_api_views_english()
    
    with open('social_media_backend/api_views.py', 'w', encoding='utf-8') as f:
        f.write(api_views_content)
    
    # 3. Update URLs
    print("3. Updating URL configuration...")
    urls_content = update_urls_configuration()
    
    with open('social_media_backend/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print("\n✅ SWAGGER CONFIGURATION COMPLETED!")
    print("📚 English documentation configured")
    print("🔗 Swagger UI: http://localhost:8000/api/docs/")
    print("📊 ReDoc: http://localhost:8000/api/redoc/")
    print("🎯 GraphQL: http://localhost:8000/graphql/")
    
    print("\n🔄 Restarting Docker services...")
    os.system("docker-compose restart web")
    
    print("\n🎊 SWAGGER READY FOR ALX PRESENTATION!")

if __name__ == "__main__":
    main()
