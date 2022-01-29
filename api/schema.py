# import graphlib
import graphene
import graphql_jwt
# from graphene_django import DjangoObjectType
from django.db.models import Sum

from api.models import Transaction, Bot, Coin
import users.schema
import bots.schema
import coins.schema
import transactions.schema

from graphene_django.debug import DjangoDebug

class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")

    
class Mutation(users.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(users.schema.Query, bots.schema.Query, coins.schema.Query, transactions.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)