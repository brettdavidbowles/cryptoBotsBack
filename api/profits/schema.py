import graphene
from graphene_django import DjangoObjectType

from api.models import ProfitPerDay
from bots.schema import BotInput
from coins.schema import CoinInput
from users.schema import UserInput

class ProfitType(DjangoObjectType):
  class Meta:
    model = ProfitPerDay
    fields = "__all__"

class ProfitInput(graphene.InputObjectType):
  bot = graphene.Field(BotInput)
  coin = graphene.Field(CoinInput)
  user = graphene.Field(UserInput)

class CreateProfitEntry(graphene.Mutation):
  profit_entry = graphene.Field(ProfitType)
  class Arguments:
    profit_data = ProfitInput(required=True)
