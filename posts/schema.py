"""
GraphQL Schema for Posts App
"""

import graphene
from graphene_django import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator

from .models import Post, Comment, Hashtag, PostHashtag
from users.schema import UserType


class PostType(DjangoObjectType):
    """
    GraphQL Type for Post model
    """
    media_url = graphene.String()
    has_media = graphene.Boolean()
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def resolve_media_url(self, info):
        return self.get_media_url()
    
    def resolve_has_media(self, info):
        return self.has_media


class CommentType(DjangoObjectType):
    """
    GraphQL Type for Comment model
    """
    is_reply = graphene.Boolean()
    
    class Meta:
        model = Comment
        fields = '__all__'
    
    def resolve_is_reply(self, info):
        return self.is_reply


class HashtagType(DjangoObjectType):
    """
    GraphQL Type for Hashtag model
    """
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostHashtagType(DjangoObjectType):
    """
    GraphQL Type for PostHashtag model
    """
    class Meta:
        model = PostHashtag
        fields = '__all__'


class PostQuery(graphene.ObjectType):
    """
    GraphQL Queries for Posts
    """
    # Single post queries
    post = graphene.Field(PostType, id=graphene.ID())
    
    # List queries
    all_posts = graphene.List(
        PostType,
        first=graphene.Int(),
        skip=graphene.Int(),
        visibility=graphene.String()
    )
    user_posts = graphene.List(
        PostType,
        user_id=graphene.ID(required=True),
        first=graphene.Int(),
        skip=graphene.Int()
    )
    feed = graphene.List(
        PostType,
        first=graphene.Int(),
        skip=graphene.Int()
    )
    
    # Comments
    post_comments = graphene.List(
        CommentType,
        post_id=graphene.ID(required=True),
        first=graphene.Int(),
        skip=graphene.Int()
    )
    
    # Hashtags
    trending_hashtags = graphene.List(HashtagType, limit=graphene.Int())
    posts_by_hashtag = graphene.List(
        PostType,
        hashtag=graphene.String(required=True),
        first=graphene.Int(),
        skip=graphene.Int()
    )
    
    def resolve_post(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            # Increment view count
            post.views_count += 1
            post.save(update_fields=['views_count'])
            return post
        except Post.DoesNotExist:
            return None
    
    def resolve_all_posts(self, info, first=20, skip=0, visibility='public'):
        posts = Post.objects.filter(visibility=visibility).order_by('-created_at')
        return posts[skip:skip + first]
    
    def resolve_user_posts(self, info, user_id, first=20, skip=0):
        posts = Post.objects.filter(author_id=user_id).order_by('-created_at')
        return posts[skip:skip + first]
    
    @login_required
    def resolve_feed(self, info, first=20, skip=0):
        user = info.context.user
        # Get posts from followed users + own posts
        following_ids = user.following.values_list('following_id', flat=True)
        posts = Post.objects.filter(
            author_id__in=list(following_ids) + [user.id],
            visibility__in=['public', 'followers']
        ).order_by('-created_at')
        return posts[skip:skip + first]
    
    def resolve_post_comments(self, info, post_id, first=20, skip=0):
        comments = Comment.objects.filter(
            post_id=post_id,
            parent__isnull=True
        ).order_by('created_at')
        return comments[skip:skip + first]
    
    def resolve_trending_hashtags(self, info, limit=10):
        return Hashtag.objects.order_by('-posts_count')[:limit]
    
    def resolve_posts_by_hashtag(self, info, hashtag, first=20, skip=0):
        try:
            hashtag_obj = Hashtag.objects.get(name=hashtag)
            post_ids = PostHashtag.objects.filter(
                hashtag=hashtag_obj
            ).values_list('post_id', flat=True)
            posts = Post.objects.filter(
                id__in=post_ids,
                visibility='public'
            ).order_by('-created_at')
            return posts[skip:skip + first]
        except Hashtag.DoesNotExist:
            return []


class CreatePost(graphene.Mutation):
    """
    Mutation to create a new post
    """
    class Arguments:
        content = graphene.String(required=True)
        visibility = graphene.String()
        hashtags = graphene.List(graphene.String)
    
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, content, visibility='public', hashtags=None):
        try:
            with transaction.atomic():
                user = info.context.user
                post = Post.objects.create(
                    author=user,
                    content=content,
                    visibility=visibility
                )
                
                # Handle hashtags
                if hashtags:
                    for hashtag_name in hashtags:
                        hashtag_name = hashtag_name.strip().lower()
                        if hashtag_name:
                            hashtag, created = Hashtag.objects.get_or_create(
                                name=hashtag_name
                            )
                            PostHashtag.objects.create(
                                post=post,
                                hashtag=hashtag
                            )
                            hashtag.posts_count += 1
                            hashtag.save(update_fields=['posts_count'])
                
                # Update user posts count
                user.posts_count += 1
                user.save(update_fields=['posts_count'])
                
                return CreatePost(post=post, success=True, errors=[])
        except Exception as e:
            return CreatePost(post=None, success=False, errors=[str(e)])


class UpdatePost(graphene.Mutation):
    """
    Mutation to update a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String()
        visibility = graphene.String()
    
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id, **kwargs):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id, author=user)
            
            for field, value in kwargs.items():
                if value is not None:
                    setattr(post, field, value)
            
            post.save()
            return UpdatePost(post=post, success=True, errors=[])
        except Post.DoesNotExist:
            return UpdatePost(post=None, success=False, errors=["Post not found or not authorized"])
        except Exception as e:
            return UpdatePost(post=None, success=False, errors=[str(e)])


class DeletePost(graphene.Mutation):
    """
    Mutation to delete a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id, author=user)
            
            # Update user posts count
            user.posts_count -= 1
            user.save(update_fields=['posts_count'])
            
            post.delete()
            return DeletePost(success=True, errors=[])
        except Post.DoesNotExist:
            return DeletePost(success=False, errors=["Post not found or not authorized"])
        except Exception as e:
            return DeletePost(success=False, errors=[str(e)])


class CreateComment(graphene.Mutation):
    """
    Mutation to create a comment on a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String(required=True)
        parent_id = graphene.ID()
    
    comment = graphene.Field(CommentType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id, content, parent_id=None):
        try:
            with transaction.atomic():
                user = info.context.user
                post = Post.objects.get(pk=post_id)
                
                parent = None
                if parent_id:
                    parent = Comment.objects.get(pk=parent_id)
                
                comment = Comment.objects.create(
                    post=post,
                    author=user,
                    content=content,
                    parent=parent
                )
                
                # Update post comments count
                post.comments_count += 1
                post.save(update_fields=['comments_count'])
                
                return CreateComment(comment=comment, success=True, errors=[])
        except Post.DoesNotExist:
            return CreateComment(comment=None, success=False, errors=["Post not found"])
        except Comment.DoesNotExist:
            return CreateComment(comment=None, success=False, errors=["Parent comment not found"])
        except Exception as e:
            return CreateComment(comment=None, success=False, errors=[str(e)])


class PostMutation(graphene.ObjectType):
    """
    GraphQL Mutations for Posts
    """
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
