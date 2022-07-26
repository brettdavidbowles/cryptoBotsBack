import graphene
from graphene_django import DjangoObjectType
from api.models import TransactionCalculations, Transaction
from transactions.schema import TransactionInputById

class TransactionCalculationsType(DjangoObjectType):
  class Meta:
    model = TransactionCalculations
    fields = "__all__"

class TransactionCalculationsInput(graphene.InputObjectType):
  transaction = graphene.Field(TransactionInputById)
  transaction_revenue = graphene.Float()
  cumulative_revenue = graphene.Float()
  transaction_profit = graphene.Float()
  cumulative_profit = graphene.Float()
  transaction_expense = graphene.Float()
  cumulative_expense = graphene.Float()
  transaction_profit_margin = graphene.Float()
  cumulative_profit_margin = graphene.Float()
  market_profit_margin = graphene.Float()

class TransactionProfitInput(graphene.InputObjectType):
  transaction = graphene.Field(TransactionInputById)
  transaction_profit = graphene.Float()

class CreateTransactionCalculations(graphene.Mutation):
  transactionCalculations = graphene.Field(TransactionCalculationsType)
  class Arguments:
    input_data = TransactionCalculationsInput(required=True)

  @staticmethod
  def mutate(root, info, input_data):
    transaction = Transaction.objects.get(id=input_data.transaction.id)
    transactionCalculations = TransactionCalculations.objects.create(
      transaction=transaction,
      transaction_revenue = input_data.transaction_revenue,
      cumulative_revenue = input_data.cumulative_revenue,
      transaction_profit = input_data.transaction_profit,
      cumulative_profit = input_data.cumulative_profit,
      transaction_expense = input_data.transaction_expense,
      cumulative_expense = input_data.cumulative_expense,
      transaction_profit_margin = input_data.transaction_profit_margin,
      cumulative_profit_margin = input_data.cumulative_profit_margin,
      market_profit_margin = input_data.market_profit_margin,      
    )
    return CreateTransactionCalculations(transactionCalculations=transactionCalculations)

# class CreateTransactionProfit(graphene.Mutation):
#   TransactionCalculations = graphene.Field(TransactionCalculationsType)
#   class Arguments:
#     input_data = TransactionProfitInput
#   @staticmethod
#   def mutate(root, info, input_data):
#     transaction = Transaction.objects.get(id=input_data.transaction.id)
#     transactionCalculations = TransactionCalculations.objects.create(
#       transaction=transaction
#       transaction_profit = input_data.transaction_profit
#     )

class Mutation(graphene.ObjectType):
  create_transaction_calculations = CreateTransactionCalculations.Field()

class Query(graphene.ObjectType):
  bar_chart_data = graphene.List(TransactionCalculationsType, bot_name=graphene.String(), username=graphene.String())
  def resolve_bar_chart_data(self, info, bot_name=None, username=None,):
    if bot_name and username:
      FilteredQuerySet = Transaction.objects.select_related().filter(
        bot__name=bot_name
      ).filter(
        user__username=username
      )
      coins = list(Coin.objects.select_related().filter(
        bot__name=bot_name
      ))
      FilteredQueryList = list(FilteredQuerySet)
      for i in coins:

      print(coins)
      return FilteredQuerySet