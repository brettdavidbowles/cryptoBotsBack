from django.contrib import admin
from .models import User, Bot, Coin, DeprecatedTransaction2, ProfitPerDay, Transaction

# Register your models here.

admin.site.register(Bot)
admin.site.register(Coin)

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key',)
class DeprecatedTransaction2Admin(admin.ModelAdmin):
    readonly_fields = ('transaction_date_time', 'change_in_total',)
class ProfitPerDayAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time', 'id')

admin.site.register(User, UserAdmin)
admin.site.register(DeprecatedTransaction2, DeprecatedTransaction2Admin)
admin.site.register(ProfitPerDay, ProfitPerDayAdmin)
admin.site.register(Transaction, TransactionAdmin)