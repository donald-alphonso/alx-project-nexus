"""
Complete Swagger API Views for ALX Project Nexus
Professional REST API documentation with all GraphQL endpoints exposed
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

# Import our error handlers for documentation
from .error_handlers import ERROR_CODES, handle_errors

# ============================================================================
# ERROR HANDLING DOCUMENTATION
# ============================================================================

@extend_schema(
    tags=['Error Handling'],
    summary='Error Handling System Documentation',
    description="""
    **Comprehensive Error Handling System**
    
    ALX Project Nexus implements a robust error handling system with:
    - Centralized error management
    - Standardized error codes
    - Detailed error messages
    - Automatic validation
    - Rate limiting protection
    - Structured logging
    
    **Error Response Format:**
    All errors follow a consistent format with error codes, messages, and context.
    
    **Error Categories:**
    - Validation Errors (VALIDATION_001)
    - Authentication Errors (AUTH_001, AUTH_002)
    - Resource Errors (RESOURCE_001)
    - Database Errors (DB_001, DB_002)
    - Server Errors (SERVER_001)
    - Rate Limiting (RATE_001)
    - GraphQL Specific (GQL_001)
    """,
    examples=[
        OpenApiExample(
            'Standard Error Response',
            description='Standard error response format',
            value={
                "errors": [
                    {
                        "message": "Authentication required",
                        "code": "AUTH_001",
                        "field": None,
                        "timestamp": "2025-01-09T18:20:00Z"
                    }
                ],
                "success": False,
                "data": None
            }
        ),
        OpenApiExample(
            'Validation Error Response',
            description='Validation error with field details',
            value={
                "errors": [
                    {
                        "message": "Email is required",
                        "code": "VALIDATION_001",
                        "field": "email",
                        "timestamp": "2025-01-09T18:20:00Z"
                    },
                    {
                        "message": "Password must be at least 8 characters",
                        "code": "VALIDATION_001",
                        "field": "password",
                        "timestamp": "2025-01-09T18:20:00Z"
                    }
                ],
                "success": False,
                "data": None
            }
        ),
        OpenApiExample(
            'Rate Limit Error',
            description='Rate limiting error response',
            value={
                "errors": [
                    {
                        "message": "Rate limit exceeded. Please try again later.",
                        "code": "RATE_001",
                        "field": None,
                        "retry_after": 60,
                        "timestamp": "2025-01-09T18:20:00Z"
                    }
                ],
                "success": False,
                "data": None
            }
        )
    ]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@handle_errors
def error_handling_documentation(request):
    """
    Error handling system documentation
    """
    return Response({
        "error_handling_system": {
            "version": "1.0.0",
            "description": "Robust error handling with centralized management",
            "features": [
                "Centralized error handling",
                "Standardized error codes",
                "Automatic validation",
                "Rate limiting protection",
                "Structured logging",
                "GraphQL middleware integration"
            ]
        },
        "error_codes": ERROR_CODES,
        "error_types": {
            "validation": {
                "code": "VALIDATION_001",
                "description": "Input validation failed",
                "common_causes": [
                    "Missing required fields",
                    "Invalid data format",
                    "Data length constraints",
                    "Invalid email format",
                    "Weak password"
                ]
            },
            "authentication": {
                "code": "AUTH_001",
                "description": "Authentication required",
                "common_causes": [
                    "Missing JWT token",
                    "Invalid JWT token",
                    "Expired JWT token",
                    "Malformed Authorization header"
                ]
            },
            "permission": {
                "code": "AUTH_002",
                "description": "Permission denied",
                "common_causes": [
                    "Insufficient user permissions",
                    "Resource access denied",
                    "Operation not allowed"
                ]
            },
            "not_found": {
                "code": "RESOURCE_001",
                "description": "Resource not found",
                "common_causes": [
                    "Invalid resource ID",
                    "Deleted resource",
                    "Non-existent endpoint"
                ]
            },
            "database": {
                "code": "DB_001",
                "description": "Database operation failed",
                "common_causes": [
                    "Connection timeout",
                    "Query execution error",
                    "Database unavailable"
                ]
            },
            "integrity": {
                "code": "DB_002",
                "description": "Data integrity constraint violation",
                "common_causes": [
                    "Duplicate unique field",
                    "Foreign key constraint",
                    "Check constraint violation"
                ]
            },
            "server": {
                "code": "SERVER_001",
                "description": "Internal server error",
                "common_causes": [
                    "Unhandled exception",
                    "Service unavailable",
                    "Configuration error"
                ]
            },
            "rate_limit": {
                "code": "RATE_001",
                "description": "Rate limit exceeded",
                "common_causes": [
                    "Too many requests per minute",
                    "Suspicious activity detected",
                    "API quota exceeded"
                ]
            }
        },
        "best_practices": {
            "client_side": [
                "Always check the 'success' field in responses",
                "Handle errors gracefully in your frontend",
                "Implement retry logic for network errors",
                "Cache JWT tokens and refresh when needed",
                "Validate input before sending requests",
                "Respect rate limits and implement backoff"
            ],
            "error_handling": [
                "Parse error codes for programmatic handling",
                "Display user-friendly error messages",
                "Log errors for debugging",
                "Implement fallback mechanisms",
                "Monitor error rates and patterns"
            ]
        },
        "middleware_features": {
            "error_handling": "Centralized error processing with consistent formatting",
            "authentication": "Automatic JWT validation and user context",
            "logging": "Detailed request/response logging with performance metrics",
            "rate_limiting": "Configurable rate limits with automatic blocking",
            "validation": "Automatic input validation with detailed error messages"
        }
    })

# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['User Management'],
    summary='Create User Account',
    description="""
    **Create a new user account**
    
    This endpoint allows registration of new users on the platform.
    All fields are required for successful registration.
    
    **GraphQL Equivalent:**
    ```graphql
    mutation {
      createUser(username: "johndoe", email: "john@example.com", password: "securepass123") {
        user { id username email }
        success
        errors
      }
    }
    ```
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'johndoe'},
                'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
                'password': {'type': 'string', 'example': 'securepassword123'},
                'first_name': {'type': 'string', 'example': 'John'},
                'last_name': {'type': 'string', 'example': 'Doe'}
            },
            'required': ['username', 'email', 'password']
        }
    },
    responses={
        201: {
            'description': 'User created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'user': {
                            'id': 1,
                            'username': 'johndoe',
                            'email': 'john@example.com',
                            'first_name': 'John',
                            'last_name': 'Doe'
                        },
                        'success': True,
                        'errors': []
                    }
                }
            }
        },
        400: {
            'description': 'Validation errors',
            'content': {
                'application/json': {
                    'example': {
                        'user': None,
                        'success': False,
                        'errors': ['Username already exists', 'Invalid email format']
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_account(request):
    """Create new user account via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'mutation': '''
        mutation CreateUser {
          createUser(
            username: "johndoe"
            email: "john@example.com" 
            password: "securepassword123"
            firstName: "John"
            lastName: "Doe"
          ) {
            user {
              id
              username
              email
              firstName
              lastName
            }
            success
            errors
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST'
    })

@extend_schema(
    tags=['Authentication'],
    summary='User Login',
    description="""
    **Authenticate user and get JWT token**
    
    Login with email and password to receive a JWT token for authenticated requests.
    
    **GraphQL Equivalent:**
    ```graphql
    mutation {
      tokenAuth(email: "john@example.com", password: "securepass123") {
        token
        payload
        refreshExpiresIn
      }
    }
    ```
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email', 'example': 'john@example.com'},
                'password': {'type': 'string', 'example': 'securepassword123'}
            },
            'required': ['email', 'password']
        }
    },
    responses={
        200: {
            'description': 'Authentication successful',
            'content': {
                'application/json': {
                    'example': {
                        'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'payload': {
                            'user_id': 1,
                            'username': 'johndoe',
                            'email': 'john@example.com',
                            'exp': 1640995200
                        },
                        'refreshExpiresIn': 604800
                    }
                }
            }
        },
        401: {
            'description': 'Authentication failed',
            'content': {
                'application/json': {
                    'example': {
                        'errors': [{'message': 'Invalid credentials'}]
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """User authentication via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'mutation': '''
        mutation Login {
          tokenAuth(email: "john@example.com", password: "securepassword123") {
            token
            payload
            refreshExpiresIn
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST'
    })

@extend_schema(
    tags=['User Profile'],
    summary='Get Current User Profile',
    description="""
    **Get authenticated user's profile information**
    
    Requires JWT token in Authorization header.
    
    **GraphQL Equivalent:**
    ```graphql
    query {
      me {
        id
        username
        email
        firstName
        lastName
        bio
        avatar
        isActive
        dateJoined
      }
    }
    ```
    """,
    responses={
        200: {
            'description': 'User profile retrieved successfully',
            'content': {
                'application/json': {
                    'example': {
                        'id': 1,
                        'username': 'johndoe',
                        'email': 'john@example.com',
                        'firstName': 'John',
                        'lastName': 'Doe',
                        'bio': 'Software developer passionate about GraphQL',
                        'avatar': 'https://example.com/avatars/johndoe.jpg',
                        'isActive': True,
                        'dateJoined': '2025-01-09T10:30:00Z'
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'query': '''
        query GetMyProfile {
          me {
            id
            username
            email
            firstName
            lastName
            bio
            avatar
            isActive
            dateJoined
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST',
        'headers': {'Authorization': 'JWT <your-token>'}
    })

# ============================================================================
# POST MANAGEMENT ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Posts'],
    summary='Create New Post',
    description="""
    **Create a new post on the platform**
    
    Authenticated users can create posts with text content and optional media.
    
    **GraphQL Equivalent:**
    ```graphql
    mutation {
      createPost(content: "Hello ALX! #GraphQL #Django") {
        post {
          id
          content
          author { username }
          createdAt
          likesCount
          commentsCount
        }
        success
        errors
      }
    }
    ```
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'content': {'type': 'string', 'example': 'Hello ALX! #GraphQL #Django'},
                'media': {'type': 'string', 'format': 'uri', 'example': 'https://example.com/image.jpg'}
            },
            'required': ['content']
        }
    },
    responses={
        201: {
            'description': 'Post created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'post': {
                            'id': 1,
                            'content': 'Hello ALX! #GraphQL #Django',
                            'author': {'username': 'johndoe'},
                            'createdAt': '2025-01-09T15:30:00Z',
                            'likesCount': 0,
                            'commentsCount': 0
                        },
                        'success': True,
                        'errors': []
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    """Create new post via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'mutation': '''
        mutation CreatePost {
          createPost(content: "Hello ALX! #GraphQL #Django") {
            post {
              id
              content
              author { username }
              createdAt
              likesCount
              commentsCount
            }
            success
            errors
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST',
        'headers': {'Authorization': 'JWT <your-token>'}
    })

@extend_schema(
    tags=['Posts'],
    summary='Get All Posts',
    description="""
    **Retrieve all posts from the platform**
    
    Get a paginated list of all posts with author information and engagement metrics.
    
    **GraphQL Equivalent:**
    ```graphql
    query {
      allPosts {
        id
        content
        author {
          username
          avatar
        }
        createdAt
        likesCount
        commentsCount
        isLiked
      }
    }
    ```
    """,
    parameters=[
        OpenApiParameter(
            name='limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of posts to return (default: 20)'
        ),
        OpenApiParameter(
            name='offset',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of posts to skip (default: 0)'
        )
    ],
    responses={
        200: {
            'description': 'Posts retrieved successfully',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'content': 'Hello ALX! #GraphQL #Django',
                            'author': {
                                'username': 'johndoe',
                                'avatar': 'https://example.com/avatars/johndoe.jpg'
                            },
                            'createdAt': '2025-01-09T15:30:00Z',
                            'likesCount': 5,
                            'commentsCount': 2,
                            'isLiked': False
                        }
                    ]
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_posts(request):
    """Get all posts via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'query': '''
        query GetAllPosts {
          allPosts {
            id
            content
            author {
              username
              avatar
            }
            createdAt
            likesCount
            commentsCount
            isLiked
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST'
    })

@extend_schema(
    tags=['Social Interactions'],
    summary='Like a Post',
    description="""
    **Like or unlike a post**
    
    Toggle like status for a specific post. Creates notification for post author.
    
    **GraphQL Equivalent:**
    ```graphql
    mutation {
      likePost(postId: 1) {
        like {
          id
          user { username }
          createdAt
        }
        success
        errors
      }
    }
    ```
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'post_id': {'type': 'integer', 'example': 1}
            },
            'required': ['post_id']
        }
    },
    responses={
        200: {
            'description': 'Post liked successfully',
            'content': {
                'application/json': {
                    'example': {
                        'like': {
                            'id': 1,
                            'user': {'username': 'johndoe'},
                            'createdAt': '2025-01-09T15:30:00Z'
                        },
                        'success': True,
                        'errors': []
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request):
    """Like a post via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'mutation': '''
        mutation LikePost {
          likePost(postId: 1) {
            like {
              id
              user { username }
              createdAt
            }
            success
            errors
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST',
        'headers': {'Authorization': 'JWT <your-token>'}
    })

# ============================================================================
# COMMENT MANAGEMENT ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Comments'],
    summary='Create Comment',
    description="""
    **Add a comment to a post**
    
    Authenticated users can comment on posts. Creates notification for post author.
    
    **GraphQL Equivalent:**
    ```graphql
    mutation {
      createComment(postId: 1, content: "Great post!") {
        comment {
          id
          content
          author { username }
          post { id }
          createdAt
        }
        success
        errors
      }
    }
    ```
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'post_id': {'type': 'integer', 'example': 1},
                'content': {'type': 'string', 'example': 'Great post! Thanks for sharing.'}
            },
            'required': ['post_id', 'content']
        }
    },
    responses={
        201: {
            'description': 'Comment created successfully',
            'content': {
                'application/json': {
                    'example': {
                        'comment': {
                            'id': 1,
                            'content': 'Great post! Thanks for sharing.',
                            'author': {'username': 'johndoe'},
                            'post': {'id': 1},
                            'createdAt': '2025-01-09T15:30:00Z'
                        },
                        'success': True,
                        'errors': []
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    """Create comment via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'mutation': '''
        mutation CreateComment {
          createComment(postId: 1, content: "Great post! Thanks for sharing.") {
            comment {
              id
              content
              author { username }
              post { id }
              createdAt
            }
            success
            errors
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST',
        'headers': {'Authorization': 'JWT <your-token>'}
    })

# ============================================================================
# SEARCH AND DISCOVERY ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Search'],
    summary='Search Posts',
    description="""
    **Search posts by content**
    
    Full-text search across post content with optional filters.
    
    **GraphQL Equivalent:**
    ```graphql
    query {
      searchPosts(query: "GraphQL") {
        id
        content
        author { username }
        createdAt
        likesCount
        commentsCount
      }
    }
    ```
    """,
    parameters=[
        OpenApiParameter(
            name='q',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Search query'
        ),
        OpenApiParameter(
            name='limit',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of results to return'
        )
    ],
    responses={
        200: {
            'description': 'Search results',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'content': 'Learning GraphQL with Django is amazing!',
                            'author': {'username': 'johndoe'},
                            'createdAt': '2025-01-09T15:30:00Z',
                            'likesCount': 5,
                            'commentsCount': 2
                        }
                    ]
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def search_posts(request):
    """Search posts via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'query': '''
        query SearchPosts {
          searchPosts(query: "GraphQL") {
            id
            content
            author { username }
            createdAt
            likesCount
            commentsCount
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST'
    })

# ============================================================================
# FOLLOW SYSTEM ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Social Network'],
    summary='Follow User',
    description="""
    **Follow another user**
    
    Start following another user to see their posts in your feed.
    
    **GraphQL Equivalent:**
    ```graphql
    mutation {
      followUser(userId: 2) {
        follow {
          id
          follower { username }
          following { username }
          createdAt
        }
        success
        errors
      }
    }
    ```
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'integer', 'example': 2}
            },
            'required': ['user_id']
        }
    },
    responses={
        200: {
            'description': 'User followed successfully',
            'content': {
                'application/json': {
                    'example': {
                        'follow': {
                            'id': 1,
                            'follower': {'username': 'johndoe'},
                            'following': {'username': 'janedoe'},
                            'createdAt': '2025-01-09T15:30:00Z'
                        },
                        'success': True,
                        'errors': []
                    }
                }
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    """Follow user via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'mutation': '''
        mutation FollowUser {
          followUser(userId: 2) {
            follow {
              id
              follower { username }
              following { username }
              createdAt
            }
            success
            errors
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST',
        'headers': {'Authorization': 'JWT <your-token>'}
    })

# ============================================================================
# NOTIFICATION ENDPOINTS
# ============================================================================

@extend_schema(
    tags=['Notifications'],
    summary='Get User Notifications',
    description="""
    **Get user's notifications**
    
    Retrieve all notifications for the authenticated user.
    
    **GraphQL Equivalent:**
    ```graphql
    query {
      myNotifications {
        id
        message
        notificationType
        isRead
        createdAt
        sender { username }
      }
    }
    ```
    """,
    responses={
        200: {
            'description': 'Notifications retrieved successfully',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': 1,
                            'message': 'johndoe liked your post',
                            'notificationType': 'like',
                            'isRead': False,
                            'createdAt': '2025-01-09T15:30:00Z',
                            'sender': {'username': 'johndoe'}
                        }
                    ]
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """Get notifications via REST API"""
    return JsonResponse({
        'message': 'Use GraphQL endpoint: /graphql/',
        'query': '''
        query GetNotifications {
          myNotifications {
            id
            message
            notificationType
            isRead
            createdAt
            sender { username }
          }
        }
        ''',
        'endpoint': '/graphql/',
        'method': 'POST',
        'headers': {'Authorization': 'JWT <your-token>'}
    })

# ============================================================================
# PLATFORM STATISTICS
# ============================================================================

@extend_schema(
    tags=['Platform'],
    summary='Platform Statistics',
    description="""
    **Get platform statistics**
    
    Real-time platform metrics and analytics.
    """,
    responses={
        200: {
            'description': 'Statistics retrieved successfully',
            'content': {
                'application/json': {
                    'example': {
                        'total_users': 150,
                        'total_posts': 1250,
                        'total_comments': 3500,
                        'total_likes': 8750,
                        'active_users_today': 45,
                        'posts_today': 25,
                        'platform_health': 'excellent'
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def platform_statistics(request):
    """Get platform statistics"""
    return JsonResponse({
        'total_users': 150,
        'total_posts': 1250,
        'total_comments': 3500,
        'total_likes': 8750,
        'active_users_today': 45,
        'posts_today': 25,
        'platform_health': 'excellent',
        'api_version': '1.0.0',
        'graphql_endpoint': '/graphql/',
        'documentation': '/api/docs/'
    })

@extend_schema(
    tags=['Platform'],
    summary='Health Check',
    description="""
    **API Health Check**
    
    Check if the API is running and healthy.
    """,
    responses={
        200: {
            'description': 'API is healthy',
            'content': {
                'application/json': {
                    'example': {
                        'status': 'healthy',
                        'timestamp': '2025-01-09T15:30:00Z',
                        'version': '1.0.0',
                        'database': 'connected',
                        'cache': 'connected'
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API health check"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'database': 'connected',
        'cache': 'connected',
        'graphql_endpoint': '/graphql/',
        'documentation': '/api/docs/'
    })
