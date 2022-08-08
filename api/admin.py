from django.contrib import admin
from .models import User, Bot, Coin, Transaction, TransactionCalculations

# Register your models here.

admin.site.register(Bot)
admin.site.register(Coin)
admin.site.register(TransactionCalculations)

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key',)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time', 'id', 'transaction_profit', 'market_cumulative_profit', 'market_percent_profit',)
    list_filter = ('bot__name',)


admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)