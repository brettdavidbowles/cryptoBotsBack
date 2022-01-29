import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum
from users.schema import UserType

from api.models import Bot

class BotType(DjangoObjectType):
	class Meta:
		model = Bot
		fields = "__all__"
	user = graphene.List(UserType)
	total_profit = graphene.Float()

	@graphene.resolve_only_args
	def resolve_user(self):
		return self.user.all()
	def resolve_total_profit(self, info, **kwargs):
		return list(Bot.objects.filter(name=self.name).aggregate(Sum('transaction__profit')).values())[0]

class Query(graphene.ObjectType):
	bots = graphene.List(BotType)
	
	def resolve_bots(self, info, **kwargs):
		return Bot.objects.all()