"""
GraphQL Schema for Users App
"""

import graphene
from graphene_django import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from django.contrib.auth import authenticate
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from .models import User, Follow


class UserType(DjangoObjectType):
    """
    GraphQL Type for User model
    """
    full_name = graphene.String()
    avatar_url = graphene.String()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'avatar', 'birth_date', 'location', 'website',
            'is_verified', 'followers_count', 'following_count',
            'posts_count', 'created_at', 'updated_at'
        )
    
    def resolve_full_name(self, info):
        return self.full_name
    
    def resolve_avatar_url(self, info):
        return self.get_avatar_url()


class FollowType(DjangoObjectType):
    """
    GraphQL Type for Follow model
    """
    class Meta:
        model = Follow
        fields = '__all__'


class UserQuery(graphene.ObjectType):
    """
    GraphQL Queries for Users
    """
    # Single user queries
    user = graphene.Field(UserType, id=graphene.ID())
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))
    me = graphene.Field(UserType)
    
    # List queries
    all_users = graphene.List(UserType)
    followers = graphene.List(UserType, user_id=graphene.ID(required=True))
    following = graphene.List(UserType, user_id=graphene.ID(required=True))
    
    # Search
    search_users = graphene.List(UserType, query=graphene.String(required=True))
    
    def resolve_user(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
    
    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
    
    @login_required
    def resolve_me(self, info):
        return info.context.user
    
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
    
    def resolve_followers(self, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return [follow.follower for follow in user.followers.all()]
        except User.DoesNotExist:
            return []
    
    def resolve_following(self, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return [follow.following for follow in user.following.all()]
        except User.DoesNotExist:
            return []
    
    def resolve_search_users(self, info, query):
        return User.objects.filter(
            username__icontains=query
        ) | User.objects.filter(
            first_name__icontains=query
        ) | User.objects.filter(
            last_name__icontains=query
        )


class CreateUser(graphene.Mutation):
    """
    Mutation to create a new user
    """
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, username, email, password, first_name=None, last_name=None):
        try:
            # Validation préalable
            if User.objects.filter(username=username).exists():
                return CreateUser(
                    user=None, 
                    success=False, 
                    errors=[f"Username '{username}' already exists"]
                )
            
            if User.objects.filter(email=email).exists():
                return CreateUser(
                    user=None, 
                    success=False, 
                    errors=[f"Email '{email}' already exists"]
                )
            
            # Validation du mot de passe
            if len(password) < 8:
                return CreateUser(
                    user=None, 
                    success=False, 
                    errors=["Password must be at least 8 characters long"]
                )
            
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name or '',
                    last_name=last_name or ''
                )
                return CreateUser(user=user, success=True, errors=[])
                
        except IntegrityError as e:
            if 'username' in str(e).lower():
                return CreateUser(user=None, success=False, errors=["Username already exists"])
            elif 'email' in str(e).lower():
                return CreateUser(user=None, success=False, errors=["Email already exists"])
            else:
                return CreateUser(user=None, success=False, errors=["User creation failed: duplicate data"])
                
        except ValidationError as e:
            error_messages = []
            if hasattr(e, 'message_dict'):
                for field, messages in e.message_dict.items():
                    error_messages.extend([f"{field}: {msg}" for msg in messages])
            else:
                error_messages = [str(e)]
            return CreateUser(user=None, success=False, errors=error_messages)
            
        except Exception as e:
            return CreateUser(user=None, success=False, errors=[f"User creation failed: {str(e)}"])


class UpdateProfile(graphene.Mutation):
    """
    Mutation to update user profile
    """
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        bio = graphene.String()
        location = graphene.String()
        website = graphene.String()
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, **kwargs):
        try:
            user = info.context.user
            for field, value in kwargs.items():
                if value is not None:
                    setattr(user, field, value)
            user.save()
            return UpdateProfile(user=user, success=True, errors=[])
        except Exception as e:
            return UpdateProfile(user=None, success=False, errors=[str(e)])


class FollowUser(graphene.Mutation):
    """
    Mutation to follow a user
    """
    class Arguments:
        user_id = graphene.ID(required=True)
    
    follow = graphene.Field(FollowType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, user_id):
        try:
            follower = info.context.user
            following = User.objects.get(pk=user_id)
            
            if follower == following:
                return FollowUser(follow=None, success=False, errors=["Cannot follow yourself"])
            
            follow, created = Follow.objects.get_or_create(
                follower=follower,
                following=following
            )
            
            if created:
                # Update counts
                follower.following_count += 1
                following.followers_count += 1
                follower.save(update_fields=['following_count'])
                following.save(update_fields=['followers_count'])
            
            return FollowUser(follow=follow, success=True, errors=[])
        except User.DoesNotExist:
            return FollowUser(follow=None, success=False, errors=["User not found"])
        except Exception as e:
            return FollowUser(follow=None, success=False, errors=[str(e)])


class UnfollowUser(graphene.Mutation):
    """
    Mutation to unfollow a user
    """
    class Arguments:
        user_id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, user_id):
        try:
            follower = info.context.user
            following = User.objects.get(pk=user_id)
            
            follow = Follow.objects.get(
                follower=follower,
                following=following
            )
            follow.delete()
            
            # Update counts
            follower.following_count -= 1
            following.followers_count -= 1
            follower.save(update_fields=['following_count'])
            following.save(update_fields=['followers_count'])
            
            return UnfollowUser(success=True, errors=[])
        except Follow.DoesNotExist:
            return UnfollowUser(success=False, errors=["Not following this user"])
        except User.DoesNotExist:
            return UnfollowUser(success=False, errors=["User not found"])
        except Exception as e:
            return UnfollowUser(success=False, errors=[str(e)])


class UserMutation(graphene.ObjectType):
    """
    GraphQL Mutations for Users
    """
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()
    follow_user = FollowUser.Field()
    unfollow_user = UnfollowUser.Field()
