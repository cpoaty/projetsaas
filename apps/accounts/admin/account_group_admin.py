from django.contrib import admin
from django import forms
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html
from ..models.account_group import AccountGroup
from ..models.account_class import AccountClass

class AccountGroupForm(forms.ModelForm):
    # Ne pas définir le champ number ici du tout
    
    class Meta:
        model = AccountGroup
        fields = ['account_class', 'number', 'actif']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Limiter les choix aux classes existantes
        self.fields['account_class'].queryset = AccountClass.objects.filter(actif=True)
        
        # Définir le champ number directement ici
        self.fields['number'] = forms.ChoiceField(
            choices=[('', '---------')],
            label="Numéro",
            help_text="Entrez un numéro de groupe selon le plan comptable OHADA (ex: 10, 11, etc.)",
            required=True,
            widget=forms.Select(attrs={'class': 'select-number'})
        )
        
        # Déterminer la classe sélectionnée
        selected_class = None
        
        # Cas POST : filtrer selon classe soumise
        if 'account_class' in self.data:
            try:
                class_id = int(self.data.get('account_class'))
                selected_class = AccountClass.objects.get(pk=class_id)
            except (ValueError, TypeError, AccountClass.DoesNotExist):
                pass
        
        # Cas édition (instance)
        elif self.instance.pk and self.instance.account_class:
            selected_class = self.instance.account_class
        
        # Si nous avons une classe, limiter les options du numéro
        if selected_class:
            class_number = selected_class.number
            choices = [('', '---------')]
            
            # Générer uniquement les options pour cette classe
            for i in range(0, 10):
                number = class_number * 10 + i
                if number in AccountGroup.NOMS_GROUPES:
                    choices.append((str(number), f"{number} - {AccountGroup.NOMS_GROUPES[number]}"))
            
            # Mettre à jour les choix du champ numéro
            self.fields['number'].choices = choices
    
    def clean(self):
        cleaned_data = super().clean()
        account_class = cleaned_data.get('account_class')
        number = cleaned_data.get('number')
        
        if account_class and number:
            # Convertir en entier
            try:
                number = int(number)
                cleaned_data['number'] = number
            except (ValueError, TypeError):
                self.add_error('number', "Le numéro doit être un entier valide.")
                return cleaned_data
            
            # Vérifier que le numéro est cohérent avec la classe
            if number // 10 != account_class.number:
                self.add_error('number', f"Le numéro de groupe doit commencer par {account_class.number} pour la classe sélectionnée.")
        
        return cleaned_data

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    form = AccountGroupForm
    
    list_display = ('number', 'get_original_name', 'get_class_name', 'actif', 'date_creation')
    list_filter = ('account_class', 'actif')
    search_fields = ('name', 'number')
    readonly_fields = ('name', 'description', 'date_creation')
    
    # Méthode pour afficher le nom original du dictionnaire NOMS_GROUPES
    def get_original_name(self, obj):
        return AccountGroup.NOMS_GROUPES.get(obj.number, "")
    get_original_name.short_description = "Nom"
    
    # Méthode pour afficher le nom de la classe de compte
    def get_class_name(self, obj):
        return obj.account_class.name
    get_class_name.short_description = "Classe de compte"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_group_info/<int:number>/', self.admin_site.admin_view(self.get_group_info), name='get_group_info'),
            path('get_group_options/<int:class_id>/', self.admin_site.admin_view(self.get_group_options), name='get_group_options'),
        ]
        return custom_urls + urls

    def get_group_options(self, request, class_id):
        """Renvoie les options de groupe disponibles pour une classe donnée"""
        try:
            account_class = AccountClass.objects.get(pk=class_id)
            class_number = account_class.number
            
            options = []
            for i in range(0, 10):
                number = class_number * 10 + i
                if number in AccountGroup.NOMS_GROUPES:
                    options.append({
                        'value': str(number),
                        'label': f"{number} - {AccountGroup.NOMS_GROUPES[number]}"
                    })
            
            return JsonResponse({'options': options})
        except (ValueError, TypeError, AccountClass.DoesNotExist):
            return JsonResponse({'error': 'Classe invalide'}, status=400)
    
    def get_group_info(self, request, number):
        """Renvoie les informations d'un groupe de comptes basé sur son numéro"""
        try:
            number = int(number)
            if 10 <= number <= 89:
                return JsonResponse({
                    'name': AccountGroup.NOMS_GROUPES.get(number, ""),
                    'description': AccountGroup.DESCRIPTIONS_GROUPES.get(number, "")
                })
        except (ValueError, TypeError):
            pass
            
        return JsonResponse({'error': 'Numéro de groupe invalide'}, status=400)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': ('account_class', 'number'),
                'description': 'Sélectionnez une classe de compte et un numéro de groupe. Les autres informations seront générées automatiquement.',
            }),
            ('Paramètres', {
                'fields': ('actif',),
            }),
        ]
        
        # Si on est en mode édition, ajouter les champs en lecture seule
        if obj:
            fieldsets.extend([
                ('Informations générées automatiquement', {
                    'fields': ('name', 'description'),
                    'description': 'Ces informations ont été générées automatiquement à partir du numéro de groupe.',
                }),
                ('Métadonnées', {
                    'fields': ('date_creation',),
                    'classes': ('collapse',),
                }),
            ])
        
        return fieldsets
    
    
    
    