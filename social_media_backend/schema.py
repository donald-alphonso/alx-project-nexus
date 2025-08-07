"""
Main GraphQL Schema for Social Media Backend
"""

import graphene
import graphql_jwt


class Query(graphene.ObjectType):
    """
    Root Query
    """
    # Health check query
    health = graphene.String()
    
    def resolve_health(self, info):
        return "GraphQL API is running!"


class Mutation(graphene.ObjectType):
    """
    Root Mutation
    """
    # JWT Authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
