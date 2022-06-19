import graphene
from graphene_django import DjangoObjectType
import statistics
from graphql import GraphQLError

import datetime

from api.models import Transaction, Bot, Coin, User, ProfitPerDay, TransactionCalculations
from bots.schema import BotInput
from coins.schema import CoinInput
from users.schema import UserInput

class TransactionType(DjangoObjectType):
		transaction_profit = graphene.Float(source="transaction_profit")
		# cumulative_coin_profit = graphene.Float(source="cumulative_coin_profit")
		market_cumulative_profit = graphene.Float(source="market_cumulative_profit")
		market_percent_profit = graphene.Float(source="market_percent_profit")
		table_row = graphene.String(source="table_row")
		bought_date_time = graphene.String(source="bought_date_time")
		sell_date_time = graphene.String(source="sell_date_time")
		

		class Meta:
				model = Transaction
				fields = "__all__"

class Query(graphene.ObjectType):
	transactions = graphene.List(TransactionType)
	transactions_by_bot = graphene.List(TransactionType, bot_name=graphene.String())
	transactions_by_coin = graphene.List(TransactionType, coin_abbrev=graphene.String())
	transactions_by_bot_and_coin = graphene.List(TransactionType, bot_name=graphene.String(), coin_abbrev=graphene.String())
	table_data = graphene.List(TransactionType, bot_name=graphene.String(), coin_abbrev=graphene.String(), username=graphene.String())

	def resolve_table_data(self, info, bot_name=None, coin_abbrev=None, username=None, **kwargs):
		if bot_name and coin_abbrev and username:
			# return Transaction.objects.filter(
			# 	bot__name=bot_name
			# ).filter(
			# 	coin__abbrev=coin_abbrev
			# ).filter(
			# 	user__username=username
			# ).exclude(
			# 	self.quantity == 0 and 
			# )
		

			transactionList = list(Transaction.objects.filter(
				bot__name=bot_name
			).filter(
				coin__abbrev=coin_abbrev
			).filter(
				user__username=username
			).order_by(
				'date_time'
			))

			if not len(transactionList):
				print('ladskjflaksdj')
				raise GraphQLError('Table Data does not exist')

			# transactionIndex = transactionList.index(self)
			# nextTransactionIndex = transactionList.index(self) + 1
			# return transactionList.exclude(
			# 	transactionList[transactionIndex].quantity == 0 and transactionList[nextTransactionIndex] ==0
			# )
			# for idx, x in enumerate(transactionList):
			# 	if idx < (len(transactionList) -1):
			# 		if x.quantity == 0 and transactionList[idx + 1].quantity == 0:
			# 			transactionList.pop(idx)
			index = 0
			while index < (len(transactionList) -1):
				if (transactionList[index].quantity == 0 and transactionList[index + 1].quantity == 0) or (transactionList[index].sell_price == 0.00 and transactionList[index + 1].sell_price == 0):
						transactionList.pop(index)
				else:
					index = index + 1
			# index = 0
			# while index < (len(transactionList) -1):
			# 	if transactionList[index].quantity:
			# 		transactionList[index].sell_price = transactionList[index + 1].sell_price
			# 	index = index + 1

			return transactionList


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
			return Transaction.objects.filter(
				bot__name=bot_name, coin__abbrev=coin_abbrev
				).order_by(
					'date_time'
				)

class TransactionInput(graphene.InputObjectType):
	bot = graphene.Field(BotInput)
	coin = graphene.Field(CoinInput)
	user = graphene.Field(UserInput)
	quantity = graphene.Float(required=True)
	bought_price = graphene.Decimal(required=False, default_value="0")
	sell_price = graphene.Decimal(required=False, default_value="0")
	current_price = graphene.Decimal(required=True)
	name = graphene.String(required=True)

class TransactionInputById(graphene.InputObjectType):
	id = graphene.ID(required=True)


class CreateTransaction(graphene.Mutation):
	transaction = graphene.Field(TransactionType)
	class Arguments:
		input_data = TransactionInput(required=True)

	@staticmethod
	def mutate(root, info, input_data):
		bot = Bot.objects.get(name=input_data.bot.name)
		coin = Coin.objects.get(abbrev=input_data.coin.abbrev)
		user = User.objects.get(username=input_data.user.username, api_key=input_data.user.api_key)
		

		

		filteredTransactionQuerySet = Transaction.objects.select_related().filter(
				bot=bot
			).filter(
				coin=coin
			).filter(
				user=user
			).order_by(
				'date_time'
			)
		filteredTransactionList = list(filteredTransactionQuerySet)
		index = 0
		while index < (len(filteredTransactionList) -1):
			if (filteredTransactionList[index].quantity == 0 and filteredTransactionList[index + 1].quantity == 0) or (filteredTransactionList[index].sell_price == 0.00 and filteredTransactionList[index + 1].sell_price == 0):
					filteredTransactionList.pop(index)
			else:
				index = index + 1
		transaction = Transaction.objects.create(
					bot=bot,
					coin=coin,
					user=user,
					quantity = input_data.quantity,
					bought_price = input_data.bought_price,
					sell_price = input_data.sell_price,
					current_price = input_data.current_price,
					name=input_data.name
				)
				
		lastBoughtTransactionIndex = -1
		lastBoughtTransactionFound = False
		if input_data.sell_price:
			while not lastBoughtTransactionFound:
				if filteredTransactionList[lastBoughtTransactionIndex].quantity:
					
					transaction_revenue = float(input_data.sell_price) * filteredTransactionList[lastBoughtTransactionIndex].quantity

					if len(filteredTransactionList) == 2:
						cumulative_revenue = transaction_revenue
					else:
						cumulative_revenue = transaction_revenue + filteredTransactionList[lastBoughtTransactionIndex - 1].transactioncalculations.cumulative_revenue

					transaction_profit = (float(input_data.sell_price) - float(filteredTransactionList[lastBoughtTransactionIndex].bought_price)) * filteredTransactionList[lastBoughtTransactionIndex].quantity
					
					if len(filteredTransactionList) == 2:
						cumulative_profit = transaction_profit
					else:
						cumulative_profit = transaction_profit + filteredTransactionList[lastBoughtTransactionIndex - 1].transactioncalculations.cumulative_profit
					
					transaction_profit_margin = (float(input_data.sell_price) - float(filteredTransactionList[lastBoughtTransactionIndex].bought_price)) / float(filteredTransactionList[lastBoughtTransactionIndex].bought_price)

					transaction_expense = float(filteredTransactionList[lastBoughtTransactionIndex].bought_price) * filteredTransactionList[lastBoughtTransactionIndex].quantity
					
					if len(filteredTransactionList) == 2:
						cumulative_expense = transaction_expense
					else:
						cumulative_expense = transaction_expense + filteredTransactionList[lastBoughtTransactionIndex - 1].transactioncalculations.cumulative_expense

					highestValueSpent = 0
					for i in filteredTransactionList:
						if i.quantity * float(i.bought_price) > highestValueSpent:
							highestValueSpent = i.quantity * float(i.bought_price)


					cumulative_profit_margin = cumulative_profit / highestValueSpent

					market_profit_margin = (input_data.current_price - filteredTransactionList[0].current_price) / filteredTransactionList[0].current_price

					NewTransactionCalculation = TransactionCalculations(
						transaction=transaction,
						transaction_revenue=transaction_revenue,
						cumulative_revenue=cumulative_revenue,
						transaction_profit=transaction_profit,
						cumulative_profit=cumulative_profit,
						transaction_expense=transaction_expense,
						cumulative_expense=cumulative_expense,
						transaction_profit_margin=transaction_profit_margin,
						cumulative_profit_margin=cumulative_profit_margin,
						market_profit_margin=market_profit_margin
					)
					NewTransactionCalculation.save()
					lastBoughtTransactionFound = True
				else:
					invalidTransaction = Transaction.objects.get(id = filteredTransactionList[lastBoughtTransactionIndex].id)
					try:
						TransactionCalculations.objects.get(transaction=invalidTransaction).delete()
					except TransactionCalculations.DoesNotExist:
						print('transaction calcs DNE, something is wrong')
					lastBoughtTransactionIndex = lastBoughtTransactionIndex - 1
			
		return CreateTransaction(transaction=transaction)

class DeleteTransaction(graphene.Mutation):
	ok = graphene.Boolean()
	class Arguments:
		id = graphene.ID()

	@classmethod
	def mutate(cls, root, info, **kwargs):
		obj = Transaction.objects.get(pk=kwargs["id"])
		obj.delete()
		return cls(ok=True)

class Mutation(graphene.ObjectType):
	create_transaction = CreateTransaction.Field()
	delete_transaction = DeleteTransaction.Field()
