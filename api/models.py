from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.conf import settings

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

class Transaction(models.Model):
	bot = models.ForeignKey(Bot, on_delete=models.SET_NULL, null=True)
	coin = models.ForeignKey(Coin, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
	quantity = models.DecimalField(max_digits=16, decimal_places=5)
	bought_price = models.DecimalField(max_digits=16, decimal_places=5, default=0)
	sell_price = models.DecimalField(max_digits=16, decimal_places=5, default=0)
	date_time = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=200, default='default')

	def __str__(self):
		return self.name

	@property
	def change_in_total(self):
		return self.coin_quantity * self.transaction_price