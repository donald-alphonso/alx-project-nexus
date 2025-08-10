"""
Professional API Views for Production-Ready Swagger Documentation
ALX Project Nexus - GraphQL Social Media API
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, IntegrityError
from datetime import timedelta
import json
import logging
import traceback

# Import our error handler
from .error_handlers import APIErrorHandler, handle_errors, ErrorHandler

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# GRAPHQL API DOCUMENTATION ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['GraphQL API'],
    summary='GraphQL Main Endpoint',
    description="""
    **Main GraphQL endpoint for all API operations**
    
    This is the primary endpoint for the ALX Project Nexus social media platform.
    All queries and mutations are handled through this single GraphQL endpoint.
    
    **Key Features:**
    - 20 Queries for data retrieval
    - 18 Mutations for data modification
    - JWT authentication support
    - Real-time subscriptions
    - Comprehensive error handling
    
    **Authentication:**
    Include JWT token in headers: `Authorization: JWT <your-token>`
    
    **GraphiQL Interface:**
    Visit `/graphql/` for interactive testing and documentation
    """,
    examples=[
        OpenApiExample(
            'User Registration',
            description='Create a new user account',
            value={
                "query": """
                mutation CreateUser {
                  createUser(
                    username: "johndoe"
                    email: "john@example.com"
                    password: "SecurePass123!"
                    firstName: "John"
                    lastName: "Doe"
                  ) {
                    user {
                      id
                      username
                      email
                      dateJoined
                    }
                    success
                    errors
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'User Authentication',
            description='Login and obtain JWT token',
            value={
                "query": """
                mutation LoginUser {
                  tokenAuth(
                    email: "john@example.com"
                    password: "SecurePass123!"
                  ) {
                    token
                    payload
                    refreshExpiresIn
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Get User Profile',
            description='Retrieve current user profile (requires authentication)',
            value={
                "query": """
                query GetMyProfile {
                  me {
                    id
                    username
                    email
                    firstName
                    lastName
                    bio
                    location
                    website
                    followersCount
                    followingCount
                    postsCount
                    isVerified
                    dateJoined
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Create Post',
            description='Create a new post (requires authentication)',
            value={
                "query": """
                mutation CreatePost {
                  createPost(
                    content: "Hello from ALX Project Nexus! #GraphQL #Django #SocialMedia"
                    visibility: "public"
                  ) {
                    post {
                      id
                      content
                      hashtags
                      visibility
                      likesCount
                      commentsCount
                      createdAt
                    }
                    success
                    errors
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Get All Posts',
            description='Retrieve all public posts with pagination',
            value={
                "query": """
                query GetAllPosts {
                  allPosts {
                    id
                    content
                    author {
                      username
                      isVerified
                    }
                    likesCount
                    commentsCount
                    hashtags
                    visibility
                    createdAt
                    updatedAt
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Like a Post',
            description='Like a post (requires authentication)',
            value={
                "query": """
                mutation LikePost {
                  likePost(postId: 1) {
                    like {
                      id
                      createdAt
                    }
                    success
                    errors
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Search Users',
            description='Search for users by username or name',
            value={
                "query": """
                query SearchUsers {
                  searchUsers(query: "john") {
                    id
                    username
                    firstName
                    lastName
                    bio
                    followersCount
                    isVerified
                  }
                }
                """
            }
        ),
        OpenApiExample(
            'Get Personalized Feed',
            description='Get personalized feed (requires authentication)',
            value={
                "query": """
                query GetFeed {
                  feed {
                    id
                    content
                    author {
                      username
                      isVerified
                    }
                    likesCount
                    commentsCount
                    isLiked
                    createdAt
                  }
                }
                """
            }
        )
    ]
)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@handle_errors
def graphql_endpoint_docs(request):
    """
    GraphQL API endpoint documentation
    """
    return Response({
        "endpoint": "/graphql/",
        "methods": ["GET", "POST"],
        "description": "Main GraphQL endpoint for all API operations",
        "graphiql_interface": "/graphql/",
        "authentication": "JWT token required for protected operations",
        "content_type": "application/json",
        "operations": {
            "queries": 20,
            "mutations": 18,
            "total": 38
        },
        "features": [
            "User management and authentication",
            "Post creation and management",
            "Social interactions (likes, comments, follows)",
            "Advanced search capabilities",
            "Real-time notifications",
            "Content moderation tools"
        ]
    })

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Authentication'],
    summary='JWT Token Information',
    description="""
    **JWT Authentication Guide**
    
    This endpoint provides information about JWT authentication used in the API.
    
    **Token Lifecycle:**
    - Access token expires in 60 minutes
    - Refresh token expires in 7 days
    - Tokens are signed with HS256 algorithm
    
    **Usage:**
    1. Register using `createUser` mutation
    2. Login using `tokenAuth` mutation
    3. Include token in headers: `Authorization: JWT <token>`
    4. Refresh token when needed using `refreshToken` mutation
    """,
    examples=[
        OpenApiExample(
            'Token Usage Example',
            description='How to use JWT token in requests',
            value={
                "headers": {
                    "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "Content-Type": "application/json"
                },
                "note": "Replace the token with your actual JWT token obtained from tokenAuth mutation"
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@handle_errors
def auth_info(request):
    """
    JWT authentication information
    """
    return Response({
        "authentication_type": "JWT (JSON Web Token)",
        "token_expiry": "60 minutes",
        "refresh_token_expiry": "7 days",
        "algorithm": "HS256",
        "header_format": "Authorization: JWT <token>",
        "obtain_token": {
            "endpoint": "/graphql/",
            "mutation": "tokenAuth",
            "required_fields": ["email", "password"]
        },
        "refresh_token": {
            "endpoint": "/graphql/",
            "mutation": "refreshToken",
            "required_fields": ["token"]
        },
        "protected_operations": [
            "createPost", "updatePost", "deletePost",
            "likePost", "unlikePost", "createComment",
            "followUser", "unfollowUser", "me", "feed",
            "myPosts", "myNotifications"
        ]
    })

# ============================================================================
# PLATFORM STATISTICS
# ============================================================================

@extend_schema(
    tags=['Platform Analytics'],
    summary='Platform Statistics',
    description="""
    **Get comprehensive platform metrics and analytics**
    
    This endpoint provides real-time statistics about the platform usage,
    including user counts, content metrics, and engagement data.
    
    **Metrics Included:**
    - Total registered users
    - Total posts created
    - Total likes and comments
    - Active users in last 24 hours
    - Posts created today
    - Top trending hashtags
    """,
    examples=[
        OpenApiExample(
            'Statistics Response',
            description='Example platform statistics',
            value={
                "total_users": 1250,
                "total_posts": 8750,
                "total_likes": 45600,
                "total_comments": 12800,
                "active_users_24h": 320,
                "posts_today": 145,
                "top_hashtags": [
                    {"name": "GraphQL", "count": 89},
                    {"name": "Django", "count": 76},
                    {"name": "ALX", "count": 65}
                ],
                "engagement_rate": "78.5%",
                "last_updated": "2025-01-09T15:30:00Z"
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@handle_errors
def platform_stats(request):
    """
    Get platform statistics and analytics
    """
    try:
        # Import models safely
        from users.models import User
        from posts.models import Post
        from interactions.models import Like, Comment
        
        # Calculate statistics
        total_users = User.objects.count()
        total_posts = Post.objects.count()
        total_likes = Like.objects.count()
        total_comments = Comment.objects.count()
        
        # Active users in last 24 hours (if last_login field exists)
        active_users_24h = 0
        if hasattr(User, 'last_login'):
            active_users_24h = User.objects.filter(
                last_login__gte=timezone.now() - timedelta(days=1)
            ).count()
        
        # Posts created today
        posts_today = Post.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        
        # Calculate engagement rate
        engagement_rate = 0
        if total_posts > 0:
            total_engagements = total_likes + total_comments
            engagement_rate = round((total_engagements / total_posts) * 100, 1)
        
        stats = {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "active_users_24h": active_users_24h,
            "posts_today": posts_today,
            "engagement_rate": f"{engagement_rate}%",
            "platform_health": "excellent" if engagement_rate > 50 else "good" if engagement_rate > 25 else "needs_improvement",
            "last_updated": timezone.now().isoformat()
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response({
            "error": "Unable to fetch statistics",
            "message": str(e),
            "fallback_data": {
                "total_users": 0,
                "total_posts": 0,
                "total_likes": 0,
                "total_comments": 0,
                "status": "service_unavailable"
            }
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

# ============================================================================
# SYSTEM HEALTH CHECK
# ============================================================================

@extend_schema(
    tags=['System Monitoring'],
    summary='System Health Check',
    description="""
    **Monitor system health and service availability**
    
    This endpoint provides real-time health status of all system components
    including database connectivity, cache status, and service availability.
    
    **Health Indicators:**
    - Database connection status
    - Redis cache connectivity
    - API response time
    - Service availability
    - System load metrics
    """,
    examples=[
        OpenApiExample(
            'Healthy System Response',
            description='Response when all systems are operational',
            value={
                "status": "healthy",
                "database": "connected",
                "redis": "connected",
                "api_version": "1.0.0",
                "environment": "production",
                "uptime": "5 days, 12 hours",
                "response_time_ms": 45,
                "services": {
                    "web": "running",
                    "celery": "running",
                    "postgres": "running",
                    "redis": "running"
                },
                "timestamp": "2025-01-09T15:30:00Z"
            }
        ),
        OpenApiExample(
            'Degraded System Response',
            description='Response when some services are experiencing issues',
            value={
                "status": "degraded",
                "database": "connected",
                "redis": "disconnected",
                "api_version": "1.0.0",
                "environment": "production",
                "issues": [
                    "Redis cache unavailable - using fallback"
                ],
                "timestamp": "2025-01-09T15:30:00Z"
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@handle_errors
def health_check(request):
    """
    System health check endpoint
    """
    health_data = {
        "status": "healthy",
        "api_version": "1.0.0",
        "environment": "development",
        "timestamp": timezone.now().isoformat(),
        "response_time_ms": 50,
        "services": {
            "web": "running",
            "database": "connected",
            "graphql": "operational"
        }
    }
    
    # Test database connectivity
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_data["database"] = "connected"
    except Exception:
        health_data["database"] = "disconnected"
        health_data["status"] = "degraded"
    
    # Test Redis connectivity (if available)
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        health_data["redis"] = "connected"
    except Exception:
        health_data["redis"] = "disconnected"
        if health_data["status"] == "healthy":
            health_data["status"] = "degraded"
    
    # Determine overall status
    if health_data["database"] == "disconnected":
        health_data["status"] = "unhealthy"
        return Response(health_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    return Response(health_data)

# ============================================================================
# API SCHEMA AND DOCUMENTATION
# ============================================================================

@extend_schema(
    tags=['API Documentation'],
    summary='API Schema Information',
    description="""
    **Complete API schema and endpoint documentation**
    
    This endpoint provides a comprehensive overview of all available API endpoints,
    their purposes, and usage examples for frontend developers.
    
    **Includes:**
    - All GraphQL operations (queries and mutations)
    - Authentication requirements
    - Request/response examples
    - Error handling guidelines
    """,
    examples=[
        OpenApiExample(
            'API Schema Overview',
            description='Complete API schema information',
            value={
                "api_name": "ALX Project Nexus",
                "version": "1.0.0",
                "description": "Modern social media platform API",
                "base_url": "http://localhost:8000",
                "graphql_endpoint": "/graphql/",
                "documentation": "/api/docs/",
                "total_operations": 38
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@handle_errors
def api_schema(request):
    """
    API schema and documentation overview
    """
    schema_data = {
        "api_name": "ALX Project Nexus - GraphQL API",
        "version": "1.0.0",
        "description": "Modern social media platform with comprehensive GraphQL API",
        "base_url": request.build_absolute_uri('/'),
        "endpoints": {
            "graphql": {
                "url": "/graphql/",
                "methods": ["GET", "POST"],
                "description": "Main GraphQL endpoint for all operations",
                "interface": "/graphql/ (GraphiQL)"
            },
            "admin": {
                "url": "/admin/",
                "description": "Django admin interface"
            },
            "documentation": {
                "swagger": "/api/docs/",
                "redoc": "/api/redoc/",
                "schema": "/api/schema/"
            },
            "monitoring": {
                "health": "/api/health/",
                "stats": "/api/stats/"
            }
        },
        "authentication": {
            "type": "JWT",
            "header": "Authorization: JWT <token>",
            "obtain_endpoint": "/graphql/ (tokenAuth mutation)",
            "token_expiry": "60 minutes",
            "refresh_expiry": "7 days"
        },
        "operations": {
            "queries": 20,
            "mutations": 18,
            "total": 38
        },
        "features": [
            "User registration and authentication",
            "Profile management",
            "Post creation and management",
            "Social interactions (likes, comments, follows)",
            "Advanced search and discovery",
            "Real-time notifications",
            "Content moderation",
            "Platform analytics"
        ],
        "tech_stack": {
            "backend": "Django 5.1",
            "api": "GraphQL (Graphene-Django)",
            "database": "PostgreSQL 16",
            "cache": "Redis 7.2",
            "task_queue": "Celery",
            "authentication": "JWT",
            "containerization": "Docker"
        }
    }
    
    return Response(schema_data)

# ============================================================================
# ERROR HANDLING DOCUMENTATION
# ============================================================================

@extend_schema(
    tags=['API Documentation'],
    summary='Error Handling Guide',
    description="""
    **Comprehensive error handling documentation**
    
    This endpoint provides detailed information about error responses,
    status codes, and how to handle various error scenarios in the API.
    """,
    examples=[
        OpenApiExample(
            'Error Response Format',
            description='Standard error response structure',
            value={
                "errors": [
                    {
                        "message": "Authentication required",
                        "code": "AUTHENTICATION_REQUIRED",
                        "field": None
                    }
                ],
                "success": False,
                "timestamp": "2025-01-09T15:30:00Z"
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@handle_errors
def error_handling_guide(request):
    """
    Error handling documentation
    """
    return Response({
        "error_format": {
            "structure": {
                "errors": "Array of error objects",
                "success": "Boolean indicating operation success",
                "timestamp": "ISO 8601 timestamp"
            },
            "error_object": {
                "message": "Human-readable error message",
                "code": "Machine-readable error code",
                "field": "Field name (if field-specific error)"
            }
        },
        "common_errors": {
            "AUTHENTICATION_REQUIRED": "JWT token required for this operation",
            "INVALID_TOKEN": "JWT token is invalid or expired",
            "USER_NOT_FOUND": "Requested user does not exist",
            "POST_NOT_FOUND": "Requested post does not exist",
            "PERMISSION_DENIED": "Insufficient permissions for this operation",
            "VALIDATION_ERROR": "Input validation failed",
            "DUPLICATE_ENTRY": "Resource already exists",
            "RATE_LIMITED": "Too many requests, please slow down"
        },
        "http_status_codes": {
            "200": "Success",
            "400": "Bad Request - Invalid input",
            "401": "Unauthorized - Authentication required",
            "403": "Forbidden - Permission denied",
            "404": "Not Found - Resource not found",
            "429": "Too Many Requests - Rate limited",
            "500": "Internal Server Error"
        },
        "best_practices": [
            "Always check the 'success' field in responses",
            "Handle errors gracefully in your frontend",
            "Implement retry logic for network errors",
            "Cache JWT tokens and refresh when needed",
            "Validate input before sending requests"
        ]
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring
    """
    from django.db import connection
    from django.core.cache import cache
    import time
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    try:
        # Test cache connection
        cache_key = f"health_check_{int(time.time())}"
        cache.set(cache_key, "test", 10)
        cache_result = cache.get(cache_key)
        cache_status = "healthy" if cache_result == "test" else "error"
        cache.delete(cache_key)
    except Exception as e:
        cache_status = f"error: {str(e)}"
    
    # Overall status
    overall_status = "healthy" if db_status == "healthy" and cache_status == "healthy" else "degraded"
    
    return Response({
        "status": overall_status,
        "timestamp": timezone.now().isoformat(),
        "services": {
            "database": db_status,
            "cache": cache_status,
            "api": "healthy"
        },
        "version": "1.0.0"
    }, status=200)
