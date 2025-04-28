from django.contrib import admin
from ..models.account_group import AccountGroup

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('get_full_number', 'name', 'description')
    list_filter = ('account_class',)
    search_fields = ('name', 'number')