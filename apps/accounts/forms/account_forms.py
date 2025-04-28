from django import forms
from ..models.account import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_group', 'number', 'name', 'description', 'account_type', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'account_group': forms.Select(attrs={'class': 'form-select'}),
            'account_type': forms.Select(attrs={'class': 'form-select'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        account_group = cleaned_data.get('account_group')
        number = cleaned_data.get('number')
        
        if account_group and number:
            # Vérification que le numéro complet ne dépasse pas 8 chiffres
            full_number = f"{account_group.get_full_number()}{number}"
            if len(full_number) > 8:
                raise forms.ValidationError(
                    "Le numéro de compte complet ne peut pas dépasser 8 chiffres."
                )
        
        return cleaned_data
