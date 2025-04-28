from django.contrib import admin
from ..models.account_type import AccountType

@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')