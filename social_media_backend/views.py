from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Count
import json

# Cache pour 5 minutes
@cache_page(60 * 5)
def presentation_view(request):
    """Page de présentation pour la validation ALX"""
    return render(request, 'presentation.html')

def api_health(request):
    """Endpoint de santé simple"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'ALX Project Nexus',
        'version': '1.0.0',
        'endpoints': {
            'graphql': '/graphql/',
            'admin': '/admin/',
            'presentation': '/presentation/',
            'health': '/api/health/'
        }
    })

def api_stats(request):
    """Statistiques du projet en cache"""
    stats = cache.get('project_stats')
    if not stats:
        try:
            # Importer les modèles de façon sécurisée
            from users.models import User
            from posts.models import Post
            from interactions.models import Comment, Like, Follow
            
            stats = {
                'users_count': User.objects.count(),
                'posts_count': Post.objects.count(),
                'comments_count': Comment.objects.count(),
                'likes_count': Like.objects.count(),
                'follows_count': Follow.objects.count(),
                'graphql_endpoints': 38,
                'django_models': 11,
                'queries': 20,
                'mutations': 18
            }
            # Cache pour 10 minutes
            cache.set('project_stats', stats, 60 * 10)
        except Exception as e:
            stats = {
                'error': 'Database not ready',
                'graphql_endpoints': 38,
                'django_models': 11,
                'queries': 20,
                'mutations': 18
            }
    
    return JsonResponse(stats)

def graphql_schema_info(request):
    """Information sur le schéma GraphQL"""
    schema_info = {
        'queries': [
            'allUsers', 'user', 'me', 'allPosts', 'post', 'myPosts', 'feed',
            'allComments', 'postComments', 'allLikes', 'postLikes', 'userLikes',
            'allFollows', 'userFollowers', 'userFollowing', 'allHashtags',
            'trendingHashtags', 'hashtagPosts', 'allNotifications', 'myNotifications',
            'allReports', 'myReports', 'contentReports'
        ],
        'mutations': [
            'createUser', 'updateUser', 'deleteUser', 'createPost', 'updatePost',
            'deletePost', 'createComment', 'updateComment', 'deleteComment',
            'createLike', 'deleteLike', 'createFollow', 'deleteFollow',
            'createHashtag', 'updateHashtag', 'deleteHashtag', 'createNotification',
            'markNotificationRead', 'createReport', 'updateReport'
        ],
        'types': [
            'UserType', 'PostType', 'CommentType', 'LikeType', 'FollowType',
            'HashtagType', 'NotificationType', 'ReportType'
        ]
    }
    return JsonResponse(schema_info)
