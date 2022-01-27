import graphlib
import graphene
from graphene_django import DjangoObjectType
from django.db.models import Sum

from api.models import Transaction, Bot, Coin, User

from graphene_django.debug import DjangoDebug

class Query(graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("name", "api_key")

class BotType(DjangoObjectType):
    class Meta:
        model = Bot
        fields = ("id", "name")
    user = graphene.List(UserType)
    total_profit = graphene.Float()

    @graphene.resolve_only_args
    def resolve_user(self):
        return self.user.all()
    def resolve_total_profit(self, info, **kwargs):
        return list(Bot.objects.filter(name=self.name).aggregate(Sum('transaction__profit')).values())[0]

class CoinType(DjangoObjectType):
    class Meta:
        model = Coin
        fields = ("id", "name", "abbrev")
    total_profit = graphene.Float()

    def resolve_total_profit(self, info, **kwargs):
        return list(Coin.objects.filter(name=self.name).aggregate(Sum('transaction__profit')).values())[0]

class TransactionType(DjangoObjectType):
    change_in_total = graphene.Float(source="change_in_total")

    class Meta:
        model = Transaction
        fields = ("id", "bot", "coin", "coin_quantity", "contemporary_coin_price", "transaction_date_time", "profit", "name")



class Query(graphene.ObjectType):
    all_transactions = graphene.List(TransactionType)
    all_bots = graphene.List(BotType)
    all_coins = graphene.List(CoinType)
    transactions_by_bot = graphene.List(TransactionType, bot_name=graphene.String())
    transactions_by_coin = graphene.List(TransactionType, coin_abbrev=graphene.String())
    transactions_by_bot_and_coin = graphene.List(TransactionType, bot_name=graphene.String(), coin_abbrev=graphene.String())

    def resolve_all_transactions(self, info, **kwargs):
        return Transaction.objects.all()
    
    def resolve_all_bots(self, info, **kwargs):
        return Bot.objects.all()

    def resolve_all_coins(self, info, **kwargs):
        return Coin.objects.all()

    def resolve_transactions_by_bot(self, info, bot_name = None, **kwargs):
        if bot_name:
            return Transaction.objects.filter(bot__name=bot_name)

    def resolve_transactions_by_coin(self, info, coin_abbrev = None, **kwargs):
        if coin_abbrev:
            return Transaction.objects.filter(coin__abbrev=coin_abbrev)
    
    def resolve_transactions_by_bot_and_coin(self, info, bot_name = None, coin_abbrev = None, **kwargs):
        if bot_name and coin_abbrev:
            return Transaction.objects.filter(bot__name=bot_name, coin__abbrev=coin_abbrev)

# class TransactionInput(graphene.InputObjectType):
#     title = graphene.String()
    

schema = graphene.Schema(query=Query)