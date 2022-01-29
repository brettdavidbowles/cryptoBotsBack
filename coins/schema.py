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
	
	def resolve_coins(self, info, **kwargs):
		return Coin.objects.all()
