"""
GraphQL Schema for Interactions App
"""

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from .models import Like, Share, Bookmark, Notification, Report
from posts.models import Post, Comment


class LikeType(DjangoObjectType):
    """
    GraphQL Type for Like model
    """
    class Meta:
        model = Like
        fields = '__all__'


class ShareType(DjangoObjectType):
    """
    GraphQL Type for Share model
    """
    class Meta:
        model = Share
        fields = '__all__'


class BookmarkType(DjangoObjectType):
    """
    GraphQL Type for Bookmark model
    """
    class Meta:
        model = Bookmark
        fields = '__all__'


class NotificationType(DjangoObjectType):
    """
    GraphQL Type for Notification model
    """
    class Meta:
        model = Notification
        fields = '__all__'


class ReportType(DjangoObjectType):
    """
    GraphQL Type for Report model
    """
    class Meta:
        model = Report
        fields = '__all__'


class InteractionQuery(graphene.ObjectType):
    """
    GraphQL Queries for Interactions
    """
    # Likes
    post_likes = graphene.List(LikeType, post_id=graphene.ID(required=True))
    comment_likes = graphene.List(LikeType, comment_id=graphene.ID(required=True))
    user_likes = graphene.List(LikeType, user_id=graphene.ID(required=True))
    
    # Shares
    post_shares = graphene.List(ShareType, post_id=graphene.ID(required=True))
    user_shares = graphene.List(ShareType, user_id=graphene.ID(required=True))
    
    # Bookmarks
    user_bookmarks = graphene.List(BookmarkType)
    
    # Notifications
    my_notifications = graphene.List(NotificationType, unread_only=graphene.Boolean())
    unread_count = graphene.Int()
    
    def resolve_post_likes(self, info, post_id):
        post_content_type = ContentType.objects.get_for_model(Post)
        return Like.objects.filter(
            content_type=post_content_type,
            object_id=post_id
        )
    
    def resolve_comment_likes(self, info, comment_id):
        comment_content_type = ContentType.objects.get_for_model(Comment)
        return Like.objects.filter(
            content_type=comment_content_type,
            object_id=comment_id
        )
    
    def resolve_user_likes(self, info, user_id):
        return Like.objects.filter(user_id=user_id)
    
    def resolve_post_shares(self, info, post_id):
        return Share.objects.filter(post_id=post_id)
    
    def resolve_user_shares(self, info, user_id):
        return Share.objects.filter(user_id=user_id)
    
    @login_required
    def resolve_user_bookmarks(self, info):
        return Bookmark.objects.filter(user=info.context.user)
    
    @login_required
    def resolve_my_notifications(self, info, unread_only=False):
        notifications = Notification.objects.filter(recipient=info.context.user)
        if unread_only:
            notifications = notifications.filter(is_read=False)
        return notifications
    
    @login_required
    def resolve_unread_count(self, info):
        return Notification.objects.filter(
            recipient=info.context.user,
            is_read=False
        ).count()


class LikePost(graphene.Mutation):
    """
    Mutation to like a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
    
    like = graphene.Field(LikeType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id):
        try:
            with transaction.atomic():
                user = info.context.user
                post = Post.objects.get(pk=post_id)
                post_content_type = ContentType.objects.get_for_model(Post)
                
                like, created = Like.objects.get_or_create(
                    user=user,
                    content_type=post_content_type,
                    object_id=post_id
                )
                
                if created:
                    # Update post likes count
                    post.likes_count += 1
                    post.save(update_fields=['likes_count'])
                    
                    # Create notification for post author
                    if post.author != user:
                        Notification.objects.create(
                            recipient=post.author,
                            sender=user,
                            notification_type='like',
                            message=f"{user.username} liked your post",
                            content_type=post_content_type,
                            object_id=post_id
                        )
                
                return LikePost(like=like, success=True, errors=[])
        except Post.DoesNotExist:
            return LikePost(like=None, success=False, errors=["Post not found"])
        except Exception as e:
            return LikePost(like=None, success=False, errors=[str(e)])


class UnlikePost(graphene.Mutation):
    """
    Mutation to unlike a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id):
        try:
            with transaction.atomic():
                user = info.context.user
                post = Post.objects.get(pk=post_id)
                post_content_type = ContentType.objects.get_for_model(Post)
                
                like = Like.objects.get(
                    user=user,
                    content_type=post_content_type,
                    object_id=post_id
                )
                like.delete()
                
                # Update post likes count
                post.likes_count -= 1
                post.save(update_fields=['likes_count'])
                
                return UnlikePost(success=True, errors=[])
        except Like.DoesNotExist:
            return UnlikePost(success=False, errors=["Like not found"])
        except Post.DoesNotExist:
            return UnlikePost(success=False, errors=["Post not found"])
        except Exception as e:
            return UnlikePost(success=False, errors=[str(e)])


class SharePost(graphene.Mutation):
    """
    Mutation to share a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
        share_type = graphene.String()
        comment = graphene.String()
    
    share = graphene.Field(ShareType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id, share_type='repost', comment=''):
        try:
            with transaction.atomic():
                user = info.context.user
                post = Post.objects.get(pk=post_id)
                
                share, created = Share.objects.get_or_create(
                    user=user,
                    post=post,
                    defaults={
                        'share_type': share_type,
                        'comment': comment
                    }
                )
                
                if created:
                    # Update post shares count
                    post.shares_count += 1
                    post.save(update_fields=['shares_count'])
                    
                    # Create notification for post author
                    if post.author != user:
                        post_content_type = ContentType.objects.get_for_model(Post)
                        Notification.objects.create(
                            recipient=post.author,
                            sender=user,
                            notification_type='share',
                            message=f"{user.username} shared your post",
                            content_type=post_content_type,
                            object_id=post_id
                        )
                
                return SharePost(share=share, success=True, errors=[])
        except Post.DoesNotExist:
            return SharePost(share=None, success=False, errors=["Post not found"])
        except Exception as e:
            return SharePost(share=None, success=False, errors=[str(e)])


class BookmarkPost(graphene.Mutation):
    """
    Mutation to bookmark a post
    """
    class Arguments:
        post_id = graphene.ID(required=True)
    
    bookmark = graphene.Field(BookmarkType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id):
        try:
            user = info.context.user
            post = Post.objects.get(pk=post_id)
            
            bookmark, created = Bookmark.objects.get_or_create(
                user=user,
                post=post
            )
            
            return BookmarkPost(bookmark=bookmark, success=True, errors=[])
        except Post.DoesNotExist:
            return BookmarkPost(bookmark=None, success=False, errors=["Post not found"])
        except Exception as e:
            return BookmarkPost(bookmark=None, success=False, errors=[str(e)])


class RemoveBookmark(graphene.Mutation):
    """
    Mutation to remove a bookmark
    """
    class Arguments:
        post_id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, post_id):
        try:
            user = info.context.user
            bookmark = Bookmark.objects.get(user=user, post_id=post_id)
            bookmark.delete()
            return RemoveBookmark(success=True, errors=[])
        except Bookmark.DoesNotExist:
            return RemoveBookmark(success=False, errors=["Bookmark not found"])
        except Exception as e:
            return RemoveBookmark(success=False, errors=[str(e)])


class MarkNotificationRead(graphene.Mutation):
    """
    Mutation to mark a notification as read
    """
    class Arguments:
        notification_id = graphene.ID(required=True)
    
    notification = graphene.Field(NotificationType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, notification_id):
        try:
            user = info.context.user
            notification = Notification.objects.get(
                pk=notification_id,
                recipient=user
            )
            notification.mark_as_read()
            return MarkNotificationRead(notification=notification, success=True, errors=[])
        except Notification.DoesNotExist:
            return MarkNotificationRead(notification=None, success=False, errors=["Notification not found"])
        except Exception as e:
            return MarkNotificationRead(notification=None, success=False, errors=[str(e)])


class InteractionMutation(graphene.ObjectType):
    """
    GraphQL Mutations for Interactions
    """
    like_post = LikePost.Field()
    unlike_post = UnlikePost.Field()
    share_post = SharePost.Field()
    bookmark_post = BookmarkPost.Field()
    remove_bookmark = RemoveBookmark.Field()
    mark_notification_read = MarkNotificationRead.Field()
