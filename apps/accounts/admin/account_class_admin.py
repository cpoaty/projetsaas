from django.contrib import admin
from ..models.account_class import AccountClass

@admin.register(AccountClass)
class AccountClassAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'description')
    search_fields = ('name', 'number')
