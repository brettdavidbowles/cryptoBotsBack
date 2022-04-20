from django.contrib import admin
from .models import User, Bot, Coin, DeprecatedTransaction2, ProfitPerDay

# Register your models here.

admin.site.register(Bot)
admin.site.register(Coin)

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('api_key',)
class DeprecatedTransaction2Admin(admin.ModelAdmin):
    readonly_fields = ('transaction_date_time',)
class ProfitPerDayAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(User, UserAdmin)
admin.site.register(DeprecatedTransaction2, DeprecatedTransaction2Admin)
admin.site.register(ProfitPerDay, ProfitPerDayAdmin)