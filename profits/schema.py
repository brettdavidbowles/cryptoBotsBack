import graphene
from graphene_django import DjangoObjectType

from api.models import ProfitPerDay

class ProfitType(DjangoObjectType):
  class Meta:
    model = ProfitPerDay
    fields = "__all__"

class Query(graphene.ObjectType):
  profits = graphene.List(ProfitType)
  profits_by_bot = graphene.List(ProfitType, bot_name=graphene.String())
  profits_by_user_and_bot = graphene.List(ProfitType, username=graphene.String(), botname=graphene.String())

  def resolve_profits(self, info):
    return ProfitPerDay.objects.all()

  def resolve_profits_by_bot(self, info, bot_name = None):
    if bot_name:
      return ProfitPerDay.objects.filter(bot__name=bot_name)
  
  
  def resolve_profits_by_user_and_bot(self, info, botname = None, username = None):
    if botname and username:
      return ProfitPerDay.objects.filter(bot__name=botname, user__username=username)