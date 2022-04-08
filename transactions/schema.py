# from platform import java_ver
# from numpy import require
import graphene
from graphene_django import DjangoObjectType

import datetime

from api.models import Transaction, Bot, Coin, User, ProfitPerDay
from bots.schema import BotInput
from coins.schema import CoinInput
from users.schema import UserInput

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

class TransactionInput(graphene.InputObjectType):
	bot = graphene.Field(BotInput)
	coin = graphene.Field(CoinInput)
	user = graphene.Field(UserInput)
	is_sale = graphene.Boolean(required=True)
	coin_quantity = graphene.Decimal(required=True)
	transaction_price = graphene.Decimal(required=True)
	contemporary_coin_price = graphene.Decimal(required=True)
	profit = graphene.Decimal(required=True)
	name = graphene.String(required=True)


class CreateTransaction(graphene.Mutation):
	transaction = graphene.Field(TransactionType)
	class Arguments:
		input_data = TransactionInput(required=True)

	@staticmethod
	def mutate(root, info, input_data):
		bot = Bot.objects.get(name=input_data.bot.name)
		coin = Coin.objects.get(abbrev=input_data.coin.abbrev)
		user = User.objects.get(username=input_data.user.username, api_key=input_data.user.api_key)
		transaction = Transaction.objects.create(
			bot=bot,
			coin=coin,
			user=user,
			is_sale=input_data.is_sale,
			coin_quantity=input_data.coin_quantity,
			transaction_price=input_data.transaction_price,
			contemporary_coin_price=input_data.contemporary_coin_price,
			profit=input_data.profit,
			name=input_data.name
		)
		ProfitObject = ProfitPerDay.objects.filter(
										bot=bot
									).filter(
										coin=coin
									).filter(
										user=user
									).filter(
										date=datetime.date.today()
									)
		if ProfitObject:
			ProfitObject[0].profit += input_data.profit
			ProfitObject[0].save()
		else:
			NewProfitObject = ProfitPerDay(
				bot=bot,
				coin=coin,
				user=user,
				profit=input_data.profit,
				name=user.username + '_' + bot.name + '_' + coin.abbrev + '_' + str(datetime.date.today())
			)
			NewProfitObject.save()
			print(user.username + '_' + bot.name + '_' + coin.abbrev + '_' + str(datetime.date.today()))
		return CreateTransaction(transaction=transaction)

class Mutation(graphene.ObjectType):
    create_transaction = CreateTransaction.Field()
