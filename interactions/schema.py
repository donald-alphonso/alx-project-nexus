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
    
    # Reports
    all_reports = graphene.List(ReportType)  # Admin only
    my_reports = graphene.List(ReportType)  # User's own reports
    content_reports = graphene.List(ReportType, content_type=graphene.String(required=True), object_id=graphene.ID(required=True))
    
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
    
    @login_required
    def resolve_all_reports(self, info):
        user = info.context.user
        if not user.is_staff:
            return []
        return Report.objects.all().order_by('-created_at')
    
    @login_required
    def resolve_my_reports(self, info):
        return Report.objects.filter(reporter=info.context.user).order_by('-created_at')
    
    def resolve_content_reports(self, info, content_type, object_id):
        user = info.context.user
        if not user.is_staff:
            return []
        
        if content_type.lower() == 'post':
            content_type_obj = ContentType.objects.get_for_model(Post)
        elif content_type.lower() == 'comment':
            content_type_obj = ContentType.objects.get_for_model(Comment)
        else:
            return []
        
        return Report.objects.filter(
            content_type=content_type_obj,
            object_id=object_id
        ).order_by('-created_at')


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


class CreateReport(graphene.Mutation):
    """
    Mutation to create a report
    """
    class Arguments:
        content_type = graphene.String(required=True)  # 'post' or 'comment'
        object_id = graphene.ID(required=True)
        reason = graphene.String(required=True)
        description = graphene.String()
    
    report = graphene.Field(ReportType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, content_type, object_id, reason, description=''):
        try:
            user = info.context.user
            
            # Get content type
            if content_type.lower() == 'post':
                content_type_obj = ContentType.objects.get_for_model(Post)
                content_obj = Post.objects.get(pk=object_id)
            elif content_type.lower() == 'comment':
                content_type_obj = ContentType.objects.get_for_model(Comment)
                content_obj = Comment.objects.get(pk=object_id)
            else:
                return CreateReport(report=None, success=False, errors=["Invalid content type"])
            
            # Check if user already reported this content
            existing_report = Report.objects.filter(
                reporter=user,
                content_type=content_type_obj,
                object_id=object_id
            ).first()
            
            if existing_report:
                return CreateReport(report=None, success=False, errors=["You have already reported this content"])
            
            # Create report
            report = Report.objects.create(
                reporter=user,
                reason=reason,
                description=description,
                content_type=content_type_obj,
                object_id=object_id
            )
            
            return CreateReport(report=report, success=True, errors=[])
            
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return CreateReport(report=None, success=False, errors=["Content not found"])
        except Exception as e:
            return CreateReport(report=None, success=False, errors=[str(e)])


class UpdateReport(graphene.Mutation):
    """
    Mutation to update report status (admin only)
    """
    class Arguments:
        report_id = graphene.ID(required=True)
        status = graphene.String(required=True)
    
    report = graphene.Field(ReportType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, report_id, status):
        try:
            user = info.context.user
            
            # Check if user is admin/staff
            if not user.is_staff:
                return UpdateReport(report=None, success=False, errors=["Permission denied"])
            
            report = Report.objects.get(pk=report_id)
            
            # Validate status
            valid_statuses = ['pending', 'reviewed', 'resolved', 'dismissed']
            if status not in valid_statuses:
                return UpdateReport(report=None, success=False, errors=["Invalid status"])
            
            report.status = status
            report.save(update_fields=['status', 'updated_at'])
            
            return UpdateReport(report=report, success=True, errors=[])
            
        except Report.DoesNotExist:
            return UpdateReport(report=None, success=False, errors=["Report not found"])
        except Exception as e:
            return UpdateReport(report=None, success=False, errors=[str(e)])


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
    create_report = CreateReport.Field()
    update_report = UpdateReport.Field()
