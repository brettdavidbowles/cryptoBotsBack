import graphene
from graphene_django import DjangoObjectType

from api.models import Transaction

class TransactionType(DjangoObjectType):
    change_in_total = graphene.Float(source="change_in_total")

    class Meta:
        model = Transaction
        fields = "__all__"

class Query(graphene.ObjectType):
	transactions = graphene.List(TransactionType)
	transactions_by_bot = graphene.List(TransactionType, bot_name=graphene.String())
	transactions_by_coin = graphene.List(TransactionType, coin_abbrev=graphene.String())
	transactions_by_bot_and_coin = graphene.List(TransactionType, bot_name=graphene.String(), coin_abbrev=graphene.String())

	def resolve_transactions(self, info, **kwargs):
		return Transaction.objects.all()

	def resolve_transactions_by_bot(self, info, bot_name = None, **kwargs):
		if bot_name:
			return Transaction.objects.filter(bot__name=bot_name)

	def resolve_transactions_by_coin(self, info, coin_abbrev = None, **kwargs):
		if coin_abbrev:
			return Transaction.objects.filter(coin__abbrev=coin_abbrev)
    
	def resolve_transactions_by_bot_and_coin(self, info, bot_name = None, coin_abbrev = None, **kwargs):
		if bot_name and coin_abbrev:
			return Transaction.objects.filter(bot__name=bot_name, coin__abbrev=coin_abbrev)
