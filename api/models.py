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

	def __str__(self):
		return self.name


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

		if self.quantity and transactionIndex < (len(transactionList) - 1) and transactionList[transactionIndex+1].quantity:
			return 0
		if self.quantity:
			return (self.current_price - self.bought_price) * Decimal(str(self.quantity))

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
