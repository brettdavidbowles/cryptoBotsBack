from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings
from decimal import *
from django.db.models import Sum

# Create your models here.

class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	api_key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	# name = models.CharField(max_length=200)
	def __str__(self):
		return self.username

class Bot(models.Model):
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=50)
	url=models.CharField(max_length=50)
	user = models.ManyToManyField(settings.AUTH_USER_MODEL)

	def __str__(self):
		return self.name

class Coin(models.Model):
	name = models.CharField(max_length=200)
	abbrev = models.CharField(max_length=200)
	user = models.ManyToManyField(settings.AUTH_USER_MODEL)
	bot = models.ManyToManyField(Bot)
	def __str__(self):
		return self.name

class DeprecatedTransaction2(models.Model):
	bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	is_sale = models.BooleanField(default=False)
	coin_quantity = models.DecimalField(max_digits=16, decimal_places=5)
	quantity = models.DecimalField(max_digits=16, decimal_places=5)
	bought_price = models.DecimalField(max_digits=16, decimal_places=5)
	sell_price = models.DecimalField(max_digits=16, decimal_places=5)
	transaction_price = models.DecimalField(max_digits=16, decimal_places=2)
	contemporary_coin_price = models.DecimalField(max_digits=16, decimal_places=2)
	change_in_total = models.DecimalField(max_digits=16, decimal_places=5)
	transaction_date_time = models.DateTimeField(auto_now_add=True)
	profit = models.DecimalField(max_digits=16, decimal_places=5)
	name = models.CharField(max_length=200, default='default')

	def __str__(self):
		return self.name

	@property
	def change_in_total(self):
		return self.coin_quantity * self.transaction_price

class ProfitPerDay(models.Model):
	date = models.DateField(auto_now_add=True)
	bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	profit = models.DecimalField(max_digits=16, decimal_places=5)
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


# def getFilteredTransactionList(self):
# 	return list(Transaction.objects.filter(
# 		bot=self.bot
# 			).filter(
# 				coin=self.coin
# 			).filter(
# 				user=self.user
# 			).order_by(
# 				'date_time'
# 			)
# 			)

class TransactionQuerySet(models.QuerySet):
	def transactions(self):
		return self.select_related().filter(
			bot=self.bot
			).filter(
				coin=self.coin
			).filter(
				user=self.user
			).order_by('date_time')

class TransactionManager(models.Manager):
	def get_queryset(self):
		return TransactionQuerySet(self)
		# bot=self.bot
		# 	).filter(
		# 		coin=self.coin
		# 	).filter(
		# 		user=self.user
		# 	).order_by('date_time')
			# )
		# return super().get_queryset().select_related(
		# 	'bot', 'coin', 'user'	
				# ).order_by(
				# 	'date_time'
				# )
				


class Transaction(models.Model):
	bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	quantity = models.FloatField()
	bought_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	sell_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	current_price = models.DecimalField(max_digits=16, decimal_places=2)
	date_time = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200, default='default')
	objects = models.Manager()
	managed_objects = TransactionManager()

	def __str__(self):
		return self.name

	# @property
	# def bought_date_time(self):
	# 	if self.quantity:
	# 		return self.date_time
	# 	else:
	# 		boughtdate = "undefined"
	# 		queryset = Transaction.objects.select_related('bot', 'coin', 'user').filter(
	# 													bot_id=self.bot_id,
	# 												).filter(
	# 													coin_id=self.coin_id
	# 												).filter(
	# 													user_id=self.user_id
	# 												).order_by('date_time')
	# 		transactionList = list(queryset)
	# 		index = transactionList.index(self)
	# 		while boughtdate == "undefined":
	# 			if index > 0 and transactionList[index - 1].sell_price > 0:
	# 				index = index - 1
	# 				print('ok')
	# 			else:
	# 				boughtdate = transactionList[index -1].date_time
	# 				print(boughtdate)
	# 		return boughtdate


	# @property
	# def sell_date_time(self):
	# 	queryset = Transaction.objects.select_related('bot', 'coin', 'user').filter(
	# 													bot_id=self.bot_id,
	# 												).filter(
	# 													coin_id=self.coin_id
	# 												).filter(
	# 													user_id=self.user_id
	# 												).order_by('date_time')
	# 	transactionList = list(queryset)
	# 	transactionIndex = transactionList.index(self)
	# 	transactionListFromCurrentTransaction = transactionList[transactionIndex:]
	# 	index = 1
	# 	while index < (len(transactionListFromCurrentTransaction) - 1):
	# 		if(transactionListFromCurrentTransaction[index].sell_price > 0 and transactionListFromCurrentTransaction[index + 1].sell_price > 0):
	# 			transactionListFromCurrentTransaction.pop(index)
	# 		else:
	# 			index = index + 1
	# 	if self.quantity:
	# 		return transactionListFromCurrentTransaction[1].date_time
	# 	else:
	# 		return self.date_time

	@property
	def transaction_profit(self):
		queryset = Transaction.objects.select_related('bot', 'coin', 'user').filter(
														bot_id=self.bot_id,
													).filter(
														coin_id=self.coin_id
													).filter(
														user_id=self.user_id
													).order_by('date_time')
		transactionList = list(queryset)
		transactionIndex = transactionList.index(self)
		def findLastValidTransactionIndex(startingindex):
			if not transactionList[transactionIndex - startingindex].quantity:
				return findLastValidTransactionIndex(startingindex + 1)
			else:
				return startingindex


		# # return transactionIndex
		if self.quantity and transactionIndex < (len(transactionList) - 1) and transactionList[transactionIndex+1].quantity:
			return 0
		if self.quantity:
			return (self.current_price - self.bought_price) * Decimal(str(self.quantity))


			# skip this one?
		# if self.sell_price and transactionIndex > transactionList.len - 1 and transactionList[transactionIndex+1].sell_price != "0.00":
		# 	return 9


		if self.sell_price and transactionIndex < (len(transactionList) - 1) and transactionList[transactionIndex+1].sell_price:
			return 0
		if self.sell_price:
			return (self.sell_price - transactionList[transactionIndex-findLastValidTransactionIndex(1)].bought_price) * Decimal(str(transactionList[transactionIndex-findLastValidTransactionIndex(1)].quantity))

	
	@property
	def market_cumulative_profit(self):
		queryset = Transaction.objects.select_related().filter(
														bot_id=self.bot_id,
													).filter(
														coin_id=self.coin_id
													).filter(
														user_id=self.user_id
													).order_by('date_time')
		transactionList = list(queryset)
		return self.current_price - transactionList[0].current_price
		

	@property
	def market_percent_profit(self):

		queryset = Transaction.objects.select_related().filter(
														bot_id=self.bot_id,
													).filter(
														coin_id=self.coin_id
													).filter(
														user_id=self.user_id
													).order_by('date_time')
		transactionList = list(queryset)
		return (self.current_price - transactionList[0].current_price)/transactionList[0].current_price

	# @property
	# def table_row(self):
	# 	transactionList = Transaction.objects.filter(
	# 			bot=self.bot
	# 		).filter(
	# 			coin=self.coin
	# 		).filter(
	# 			user=self.user
	# 		).order_by(
	# 			'date_time'
	# 		)
	# 	transactionIndex = transactionList.index(self)
	# 	nextTransactionIndex = transactionList.index(self) + 1
	# 	transactionListSansFailedTransactions = transactionList.exclude(
	# 		transactionList[transactionIndex].quantity == 0 and transactionList[nextTransactionIndex] ==0
	# 	)
	# 	transactionObject = transactionList[transactionIndex]
		# get_next_by_publish_date(publish_date__isnull=False)
		# nextEntry = transactionList[transactionIndex].get_next_by_date_time().id
		# transactionListWithoutFailedRows = transactionList.exclude(
		# 	self.quantity == 0 and nextEntry.quantity == 0
		# )
		# transactionList = list(Transaction.objects.filter(
		# 		bot=self.bot,
		# 	).filter(
		# 		coin=self.coin
		# 	).filter(
		# 		user=self.user
		# 	).order_by(
		# 		'date_time'
		# 	).exclude(
		# 	self.quantity == 0 and nextEntry.quantity == 0
		# ))
		# return transactionList[transactionIndex].get_next_by_date_time()

	# @property
	# def cumulative_coin_profit(self):
	# 	transactionIndex = list(Transaction.objects.filter(
	# 			coin=self.coin
	# 		).filter(
	# 			bot=self.bot
	# 		).filter(
	# 			user=self.user)).index(self)
	# 	if self.sell_price:
	# 		return sum([transaction.transaction_profit for transaction in list(Transaction.objects.filter(
	# 			coin=self.coin).filter(
	# 			bot=self.bot
	# 		).filter(
	# 			user=self.user).exclude(
	# 				sell_price=0
	# 			))[0:transactionIndex]])
	# 		return Transaction.objects.filter(
	# 			coin=self.coin).filter(
	# 			bot=self.bot
	# 		).filter(
	# 			user=self.user).exclude(
	# 				sell_price=0
	# 			)[0:transactionIndex].aggregate(Sum("transaction__transaction_profit"))
	# 	if self.quantity:
	# 		return sum([transaction.transaction_profit for transaction in list(Transaction.objects.filter(
	# 			coin=self.coin).filter(
	# 			bot=self.bot
	# 		).filter(
	# 			user=self.user).exclude(
	# 				sell_price=0
	# 			))[0:transactionIndex]]) + self.transaction_profit
	# 		return Transaction.objects.filter(
	# 			coin=self.coin).filter(
	# 			bot=self.bot
	# 		).filter(
	# 			user=self.user).exclude(
	# 				sell_price=0
	# 			)[0:transactionIndex].aggregate(Sum("transaction_profit")) + self.transaction_profit

class TransactionCalculations(models.Model):
	transaction = models.OneToOneField(
			Transaction,
			on_delete=models.RESTRICT,
			primary_key=True,
	)
	transaction_revenue = models.FloatField(null=True)
	cumulative_revenue = models.FloatField(null=True)
	transaction_profit = models.FloatField(null=True)
	cumulative_profit = models.FloatField(null=True)
	transaction_expense = models.FloatField(null=True)
	cumulative_expense = models.FloatField(null=True)
	transaction_profit_margin = models.FloatField(null=True)
	cumulative_profit_margin = models.FloatField(null=True)
	market_profit_margin = models.FloatField(null=True)
