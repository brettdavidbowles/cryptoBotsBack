from django.contrib import admin
from .models import User, Bot, Coin, Transaction

# Register your models here.

admin.site.register(Bot)
admin.site.register(Coin)

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key',)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('transaction_date_time',)

admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)