"""
Gestionnaire d'erreurs complet pour ALX Project Nexus
Gestion robuste de tous les cas d'erreur possibles
"""

import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError, DatabaseError
from graphql import GraphQLError
from rest_framework import status
from rest_framework.response import Response
import json

# Configuration du logging
logger = logging.getLogger(__name__)

class ErrorHandler:
    """Gestionnaire centralisé d'erreurs"""
    
    @staticmethod
    def handle_graphql_error(error, context=None):
        """Gère les erreurs GraphQL avec contexte"""
        
        error_info = {
            'message': str(error),
            'type': type(error).__name__,
            'timestamp': None,
            'context': context or {},
            'code': 'GRAPHQL_ERROR'
        }
        
        # Erreurs spécifiques
        if isinstance(error, ValidationError):
            error_info.update({
                'code': 'VALIDATION_ERROR',
                'details': error.message_dict if hasattr(error, 'message_dict') else str(error)
            })
        
        elif isinstance(error, PermissionDenied):
            error_info.update({
                'code': 'PERMISSION_DENIED',
                'message': 'Access denied. Authentication required.'
            })
        
        elif isinstance(error, IntegrityError):
            error_info.update({
                'code': 'INTEGRITY_ERROR',
                'message': 'Data integrity constraint violation'
            })
        
        elif isinstance(error, DatabaseError):
            error_info.update({
                'code': 'DATABASE_ERROR',
                'message': 'Database operation failed'
            })
        
        # Log l'erreur
        logger.error(f"GraphQL Error: {error_info}")
        
        return GraphQLError(
            message=error_info['message'],
            extensions={
                'code': error_info['code'],
                'type': error_info['type'],
                'context': error_info['context']
            }
        )
    
    @staticmethod
    def handle_authentication_error():
        """Gère les erreurs d'authentification"""
        return {
            'success': False,
            'errors': ['Authentication required. Please provide a valid JWT token.'],
            'code': 'AUTHENTICATION_REQUIRED',
            'data': None
        }
    
    @staticmethod
    def handle_validation_error(errors):
        """Gère les erreurs de validation"""
        if isinstance(errors, dict):
            error_list = []
            for field, messages in errors.items():
                if isinstance(messages, list):
                    for message in messages:
                        error_list.append(f"{field}: {message}")
                else:
                    error_list.append(f"{field}: {messages}")
        else:
            error_list = [str(errors)]
        
        return {
            'success': False,
            'errors': error_list,
            'code': 'VALIDATION_ERROR',
            'data': None
        }
    
    @staticmethod
    def handle_not_found_error(resource_type="Resource"):
        """Gère les erreurs de ressource non trouvée"""
        return {
            'success': False,
            'errors': [f"{resource_type} not found."],
            'code': 'NOT_FOUND',
            'data': None
        }
    
    @staticmethod
    def handle_permission_error():
        """Gère les erreurs de permission"""
        return {
            'success': False,
            'errors': ['You do not have permission to perform this action.'],
            'code': 'PERMISSION_DENIED',
            'data': None
        }
    
    @staticmethod
    def handle_database_error():
        """Gère les erreurs de base de données"""
        return {
            'success': False,
            'errors': ['Database operation failed. Please try again.'],
            'code': 'DATABASE_ERROR',
            'data': None
        }
    
    @staticmethod
    def handle_server_error():
        """Gère les erreurs serveur internes"""
        return {
            'success': False,
            'errors': ['Internal server error. Please contact support.'],
            'code': 'INTERNAL_ERROR',
            'data': None
        }
    
    @staticmethod
    def handle_rate_limit_error():
        """Gère les erreurs de limite de taux"""
        return {
            'success': False,
            'errors': ['Rate limit exceeded. Please try again later.'],
            'code': 'RATE_LIMIT_EXCEEDED',
            'data': None
        }

class APIErrorHandler:
    """Gestionnaire d'erreurs pour les vues REST API"""
    
    @staticmethod
    def handle_api_error(error, request=None):
        """Gère les erreurs API REST avec réponse appropriée"""
        
        error_response = {
            'error': True,
            'message': 'An error occurred',
            'code': 'UNKNOWN_ERROR',
            'timestamp': None,
            'path': request.path if request else None,
            'method': request.method if request else None
        }
        
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        if isinstance(error, ValidationError):
            error_response.update({
                'message': 'Validation failed',
                'code': 'VALIDATION_ERROR',
                'details': error.message_dict if hasattr(error, 'message_dict') else str(error)
            })
            status_code = status.HTTP_400_BAD_REQUEST
        
        elif isinstance(error, PermissionDenied):
            error_response.update({
                'message': 'Access denied',
                'code': 'PERMISSION_DENIED'
            })
            status_code = status.HTTP_403_FORBIDDEN
        
        elif isinstance(error, IntegrityError):
            error_response.update({
                'message': 'Data integrity constraint violation',
                'code': 'INTEGRITY_ERROR'
            })
            status_code = status.HTTP_409_CONFLICT
        
        elif isinstance(error, DatabaseError):
            error_response.update({
                'message': 'Database operation failed',
                'code': 'DATABASE_ERROR'
            })
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        
        # Log l'erreur
        logger.error(f"API Error: {error_response}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return JsonResponse(error_response, status=status_code)

def handle_404(request, exception=None):
    """Gestionnaire personnalisé pour erreur 404"""
    return JsonResponse({
        'error': True,
        'message': 'Endpoint not found',
        'code': 'NOT_FOUND',
        'path': request.path,
        'available_endpoints': [
            '/graphql/',
            '/api/docs/',
            '/api/swagger/',
            '/api/health/',
            '/admin/'
        ]
    }, status=404)

def handle_500(request):
    """Gestionnaire personnalisé pour erreur 500"""
    return JsonResponse({
        'error': True,
        'message': 'Internal server error',
        'code': 'INTERNAL_ERROR',
        'contact': 'Please contact support if this persists'
    }, status=500)

def handle_403(request, exception=None):
    """Gestionnaire personnalisé pour erreur 403"""
    return JsonResponse({
        'error': True,
        'message': 'Access forbidden',
        'code': 'FORBIDDEN',
        'authentication_required': True,
        'login_url': '/admin/login/'
    }, status=403)

class GraphQLErrorMiddleware:
    """Middleware pour gérer les erreurs GraphQL"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            if '/graphql/' in request.path:
                logger.error(f"GraphQL Middleware Error: {e}")
                return JsonResponse({
                    'errors': [{
                        'message': 'GraphQL server error',
                        'extensions': {
                            'code': 'INTERNAL_ERROR',
                            'type': type(e).__name__
                        }
                    }]
                }, status=500)
            raise

# Décorateur pour gestion d'erreurs automatique
def handle_errors(func):
    """Décorateur pour gestion automatique d'erreurs"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e.message_dict if hasattr(e, 'message_dict') else str(e))
        except PermissionDenied:
            return ErrorHandler.handle_permission_error()
        except IntegrityError:
            return ErrorHandler.handle_database_error()
        except DatabaseError:
            return ErrorHandler.handle_database_error()
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return ErrorHandler.handle_server_error()
    
    return wrapper

# Utilitaires pour validation
class ValidationUtils:
    """Utilitaires de validation"""
    
    @staticmethod
    def validate_email(email):
        """Valide un email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Valide un mot de passe"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Za-z]', password):
            errors.append("Password must contain at least one letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        return errors
    
    @staticmethod
    def validate_username(username):
        """Valide un nom d'utilisateur"""
        errors = []
        
        if len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if len(username) > 30:
            errors.append("Username must be less than 30 characters")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append("Username can only contain letters, numbers, and underscores")
        
        return errors

# Configuration des codes d'erreur
ERROR_CODES = {
    'VALIDATION_ERROR': 'VALIDATION_001',
    'AUTHENTICATION_REQUIRED': 'AUTH_001',
    'PERMISSION_DENIED': 'AUTH_002',
    'NOT_FOUND': 'RESOURCE_001',
    'DATABASE_ERROR': 'DB_001',
    'INTEGRITY_ERROR': 'DB_002',
    'INTERNAL_ERROR': 'SERVER_001',
    'RATE_LIMIT_EXCEEDED': 'RATE_001',
    'GRAPHQL_ERROR': 'GQL_001'
}

def get_error_code(error_type):
    """Récupère le code d'erreur standardisé"""
    return ERROR_CODES.get(error_type, 'UNKNOWN_001')
