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
	bots_by_user = graphene.List(BotType, username=graphene.String())
	bot_by_name = graphene.Field(BotType, name=graphene.String())
	
	def resolve_bots(self, info, **kwargs):
		return Bot.objects.all()
	
	def resolve_bots_by_user(self, info, username = None):
		if username:
			return Bot.objects.filter(user__username=username)
	
	def resolve_bot_by_name(self, info, name = None):
		if name:
			return Bot.objects.get(name=name)

class BotInput(graphene.InputObjectType):
	name = graphene.String(required=True)