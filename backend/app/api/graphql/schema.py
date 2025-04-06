import strawberry
from strawberry.fastapi import GraphQLRouter

from app.api.graphql.resolvers.user import UserMutation, UserQuery


@strawberry.type
class Query(UserQuery):
    # You can add more query resolvers from other domains here
    pass


@strawberry.type
class Mutation(UserMutation):
    # You can add more mutation resolvers from other domains here
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema)