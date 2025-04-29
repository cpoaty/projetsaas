from django.contrib import admin
from ..models.account import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('get_full_number', 'name', 'account_type', 'is_active')
    list_filter = ('account_type', 'is_active', 'account_group__account_class')
    search_fields = ('name', 'number')