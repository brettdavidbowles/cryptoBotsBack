from django.contrib.auth import get_user_model
from numpy import require
import graphene
from graphene_django import DjangoObjectType

class TransactionType(DjangoObjectType):
	class Meta:
		model = get_user_model()

# class createTransaction(graphene.Mutation):
# 	class Arguments:
# 		username = graphene.String(required=True)
# 		coin_abbrev = graphene.String(required=True)
# 		bot_name = graphene.String(required=True)
# 		is_sale = graphene.Boolean(required=True)
# 		coin_quantity = 
# 		contemporary_coin_price = 
# 		change_in_total = 
# 		transaction_date_time = 
# 		profit = 
# 		name = 

	# transaction = graphene.Field(TransactionType)
