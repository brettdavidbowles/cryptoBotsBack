import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum

from api.models import Coin

class CoinType(DjangoObjectType):
	class Meta:
		model = Coin
		fields = "__all__"
	total_profit = graphene.Float()
	
	def resolve_total_profit(self, info, **kwargs):
		return list(Coin.objects.filter(name=self.name).aggregate(Sum('transaction__profit')).values())[0]

class Query(graphene.ObjectType):
	coins = graphene.List(CoinType)
	coins_by_bot = graphene.List(CoinType, bot_name=graphene.String())
	
	def resolve_coins(self, info, **kwargs):
		return Coin.objects.all()
    
	def resolve_coins_by_bot(self, info, bot_name = None):
		if bot_name:
			return Coin.objects.filter(bot__name=bot_name)

class CoinInput(graphene.InputObjectType):
	abbrev = graphene.String(required=True)
