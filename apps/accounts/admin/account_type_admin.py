from django.contrib import admin
from ..models.account_type import AccountType

@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_description')
    list_filter = ('code',)
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('name', 'description')  # Les deux champs sont générés automatiquement

    # Définir tous les champs à afficher dans le formulaire
    fields = ('code', 'name', 'description')

    def get_description(self, obj):
        """Retourne une description du type de compte"""
        return obj.description or obj.DESCRIPTIONS.get(obj.code, "")
    get_description.short_description = "Description"

    # Changer les labels des champs
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'name':
            field.label = "Nom"
        return field
    
    def has_delete_permission(self, request, obj=None):
    # Empêcher la suppression des types de base
        if obj and obj.code in [AccountType.AC, AccountType.PA, AccountType.CH, AccountType.PR, AccountType.CP]:
            return False
        return super().has_delete_permission(request, obj)
    
    class Media:
        js = ('accounts/js/account_type_admin.js',)