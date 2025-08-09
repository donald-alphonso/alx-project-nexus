"""
Middleware GraphQL robuste pour ALX Project Nexus
Gestion complète des erreurs, authentification et logging
"""

import logging
import traceback
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError, DatabaseError
from graphql import GraphQLError
from graphql.execution.middleware import MiddlewareManager
from graphene_django.utils import GraphQLError as DjangoGraphQLError
import json

# Configuration du logging
logger = logging.getLogger('graphql')

class ErrorHandlingMiddleware:
    """
    Middleware pour gestion centralisée des erreurs GraphQL
    """
    
    def __init__(self):
        self.error_count = 0
        self.start_time = timezone.now()
    
    def resolve(self, next, root, info, **args):
        """
        Résout les requêtes avec gestion d'erreurs complète
        """
        
        operation_name = getattr(info.operation, 'name', {})
        operation_name = operation_name.value if operation_name else 'Unknown'
        field_name = info.field_name
        
        try:
            # Log de la requête
            logger.info(f"GraphQL Request: {operation_name}.{field_name}")
            
            # Exécuter la résolution
            result = next(root, info, **args)
            
            # Log du succès
            logger.debug(f"GraphQL Success: {operation_name}.{field_name}")
            
            return result
            
        except ValidationError as e:
            self.error_count += 1
            error_msg = f"Validation error in {field_name}"
            logger.warning(f"GraphQL Validation Error: {error_msg} - {str(e)}")
            
            raise GraphQLError(
                message=error_msg,
                extensions={
                    'code': 'VALIDATION_ERROR',
                    'field': field_name,
                    'details': e.message_dict if hasattr(e, 'message_dict') else str(e),
                    'timestamp': timezone.now().isoformat()
                }
            )
        
        except PermissionDenied as e:
            self.error_count += 1
            error_msg = f"Permission denied for {field_name}"
            logger.warning(f"GraphQL Permission Error: {error_msg}")
            
            raise GraphQLError(
                message=error_msg,
                extensions={
                    'code': 'PERMISSION_DENIED',
                    'field': field_name,
                    'authentication_required': True,
                    'timestamp': timezone.now().isoformat()
                }
            )
        
        except IntegrityError as e:
            self.error_count += 1
            error_msg = f"Data integrity error in {field_name}"
            logger.error(f"GraphQL Integrity Error: {error_msg} - {str(e)}")
            
            raise GraphQLError(
                message="Data integrity constraint violation",
                extensions={
                    'code': 'INTEGRITY_ERROR',
                    'field': field_name,
                    'timestamp': timezone.now().isoformat()
                }
            )
        
        except DatabaseError as e:
            self.error_count += 1
            error_msg = f"Database error in {field_name}"
            logger.error(f"GraphQL Database Error: {error_msg} - {str(e)}")
            
            raise GraphQLError(
                message="Database operation failed",
                extensions={
                    'code': 'DATABASE_ERROR',
                    'field': field_name,
                    'timestamp': timezone.now().isoformat()
                }
            )
        
        except Exception as e:
            self.error_count += 1
            error_msg = f"Unexpected error in {field_name}: {str(e)}"
            logger.error(f"GraphQL Unexpected Error: {error_msg}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            raise GraphQLError(
                message="An unexpected error occurred",
                extensions={
                    'code': 'INTERNAL_ERROR',
                    'field': field_name,
                    'timestamp': timezone.now().isoformat()
                }
            )

class AuthenticationMiddleware:
    """
    Middleware pour gestion de l'authentification GraphQL
    """
    
    def resolve(self, next, root, info, **args):
        """
        Vérifie l'authentification pour les opérations protégées
        """
        
        # Opérations qui nécessitent une authentification
        protected_operations = {
            'createPost', 'updatePost', 'deletePost',
            'likePost', 'unlikePost', 'createComment',
            'followUser', 'unfollowUser', 'updateProfile',
            'me', 'myPosts', 'myNotifications'
        }
        
        field_name = info.field_name
        
        if field_name in protected_operations:
            user = getattr(info.context, 'user', None)
            
            if not user or not user.is_authenticated:
                logger.warning(f"Unauthenticated access attempt to {field_name}")
                
                raise GraphQLError(
                    message=f"Authentication required for operation '{field_name}'. Please provide a valid JWT token.",
                    extensions={
                        'code': 'AUTHENTICATION_REQUIRED',
                        'field': field_name,
                        'login_required': True,
                        'help': 'Include Authorization header with Bearer token',
                        'timestamp': timezone.now().isoformat()
                    }
                )
        
        return next(root, info, **args)

class LoggingMiddleware:
    """
    Middleware pour logging détaillé des opérations GraphQL
    """
    
    def resolve(self, next, root, info, **args):
        """
        Log toutes les opérations GraphQL
        """
        
        start_time = timezone.now()
        field_name = info.field_name
        user = getattr(info.context, 'user', None)
        user_id = user.id if user and user.is_authenticated else 'anonymous'
        
        try:
            result = next(root, info, **args)
            
            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"GraphQL Operation: {field_name} | User: {user_id} | Duration: {duration:.3f}s")
            
            return result
            
        except Exception as e:
            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.error(f"GraphQL Error: {field_name} | User: {user_id} | Duration: {duration:.3f}s | Error: {str(e)}")
            raise

class RateLimitingMiddleware:
    """
    Middleware pour limitation du taux de requêtes
    """
    
    def __init__(self):
        self.request_counts = {}
        self.window_start = timezone.now()
        self.window_duration = 60  # 1 minute
        self.max_requests = 100    # 100 requêtes par minute
    
    def resolve(self, next, root, info, **args):
        """
        Limite le taux de requêtes par utilisateur
        """
        
        current_time = timezone.now()
        user = getattr(info.context, 'user', None)
        user_key = user.id if user and user.is_authenticated else info.context.META.get('REMOTE_ADDR', 'unknown')
        
        # Reset du compteur si la fenêtre est expirée
        if (current_time - self.window_start).total_seconds() > self.window_duration:
            self.request_counts = {}
            self.window_start = current_time
        
        # Vérification du taux
        current_count = self.request_counts.get(user_key, 0)
        
        if current_count >= self.max_requests:
            logger.warning(f"Rate limit exceeded for user: {user_key}")
            
            raise GraphQLError(
                message="Rate limit exceeded",
                extensions={
                    'code': 'RATE_LIMIT_EXCEEDED',
                    'max_requests': self.max_requests,
                    'window_duration': self.window_duration,
                    'retry_after': self.window_duration,
                    'timestamp': timezone.now().isoformat()
                }
            )
        
        # Incrémenter le compteur
        self.request_counts[user_key] = current_count + 1
        
        return next(root, info, **args)

class ValidationMiddleware:
    """
    Middleware pour validation des entrées
    """
    
    def resolve(self, next, root, info, **args):
        """
        Valide les arguments d'entrée
        """
        
        field_name = info.field_name
        
        # Validation spécifique par champ
        if field_name == 'createUser':
            self._validate_user_creation(args)
        elif field_name == 'createPost':
            self._validate_post_creation(args)
        elif field_name in ['likePost', 'unlikePost', 'deletePost']:
            self._validate_post_id(args)
        
        return next(root, info, **args)
    
    def _validate_user_creation(self, args):
        """Valide la création d'utilisateur"""
        
        email = args.get('email', '')
        username = args.get('username', '')
        password = args.get('password', '')
        
        errors = []
        
        if not email or '@' not in email:
            errors.append("Valid email is required")
        
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters")
        
        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters")
        
        if errors:
            raise ValidationError(errors)
    
    def _validate_post_creation(self, args):
        """Valide la création de post"""
        
        content = args.get('content', '')
        
        if not content or len(content.strip()) == 0:
            raise ValidationError("Post content cannot be empty")
        
        if len(content) > 2000:
            raise ValidationError("Post content cannot exceed 2000 characters")
    
    def _validate_post_id(self, args):
        """Valide l'ID de post"""
        
        post_id = args.get('postId') or args.get('post_id')
        
        if not post_id:
            raise ValidationError("Post ID is required")
        
        try:
            int(post_id)
        except (ValueError, TypeError):
            raise ValidationError("Post ID must be a valid integer")

# Combinaison de tous les middlewares
class GraphQLMiddlewareStack:
    """
    Stack de middlewares GraphQL
    """
    
    def __init__(self):
        self.error_handler = ErrorHandlingMiddleware()
        self.auth_handler = AuthenticationMiddleware()
        self.logger = LoggingMiddleware()
        self.rate_limiter = RateLimitingMiddleware()
        self.validator = ValidationMiddleware()
    
    def get_middleware(self):
        """
        Retourne la liste des middlewares dans l'ordre d'exécution
        """
        return [
            self.logger,
            self.rate_limiter,
            self.validator,
            self.auth_handler,
            self.error_handler
        ]

# Instance globale du middleware stack
middleware_stack = GraphQLMiddlewareStack()

def get_graphql_middleware():
    """
    Fonction pour obtenir les middlewares GraphQL
    """
    return middleware_stack.get_middleware()

# Fonction utilitaire pour formater les erreurs
def format_graphql_error(error):
    """
    Formate les erreurs GraphQL de manière cohérente
    """
    
    formatted_error = {
        'message': str(error),
        'locations': getattr(error, 'locations', None),
        'path': getattr(error, 'path', None)
    }
    
    # Ajouter les extensions si disponibles
    if hasattr(error, 'extensions') and error.extensions:
        formatted_error['extensions'] = error.extensions
    
    return formatted_error
