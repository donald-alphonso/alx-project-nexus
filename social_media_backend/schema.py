"""
Main GraphQL Schema for Social Media Backend
"""

import graphene
import graphql_jwt

# Import all app schemas
from users.schema import UserQuery, UserMutation
from posts.schema import PostQuery, PostMutation
from interactions.schema import InteractionQuery, InteractionMutation


class Query(
    UserQuery,
    PostQuery, 
    InteractionQuery,
    graphene.ObjectType
):
    """
    Root Query combining all app queries
    """
    # Health check query
    health = graphene.String()
    
    def resolve_health(self, info):
        return "GraphQL API is running!"


class Mutation(
    UserMutation,
    PostMutation,
    InteractionMutation,
    graphene.ObjectType
):
    """
    Root Mutation combining all app mutations
    """
    # JWT Authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
