from django.contrib import admin
from django import forms
from django.http import JsonResponse
from django.urls import path
from accounts.models.account_class import AccountClass

class AccountClassForm(forms.ModelForm):
    # Remplacer le champ number par un ChoiceField
    number = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 9)],  # Crée des choix de 1 à 8
        label="Numéro",
        help_text="Entrez un chiffre entre 1 et 8 conformément au plan comptable OHADA.",
    )
    # Ajout de champs de prévisualisation en lecture seule avec des widgets plus grands
    class Meta:
        model = AccountClass
        fields = ['number']  # Seulement le numéro est modifiable, tout le reste est automatique

    def clean_number(self):
        # Convertir la chaîne en entier
        number = int(self.cleaned_data.get('number', 0))
        if number < 1 or number > 8:
            raise forms.ValidationError("Le numéro de classe doit être compris entre 1 et 8.")
        return number
    
    def save(self, commit=True):
        # Récupérer l'instance mais ne pas encore sauvegarder
        instance = super().save(commit=False)
        
        # Définir automatiquement la position dans le bilan en fonction du numéro selon le plan comptable OHADA
        number = instance.number
        
        # 1 : Passif (Comptes de ressources durables)
        if number == 1:
            instance.position_bilan = "Passif"
        
        # 2 et 3 : Actif (Comptes d'actif immobilisé et Comptes de stocks)
        elif number == 2 or number == 3:
            instance.position_bilan = "Actif"
        
        # 4 : Peut être Actif ou Passif, mais Passif par défaut (Comptes de tiers)
        elif number == 4:
            instance.position_bilan = "Passif"
        
        # 5 : Peut être Actif ou Passif, mais Actif par défaut (Comptes de trésorerie)
        elif number == 5:
            instance.position_bilan = "Actif"
        
        # 6 : Charges (Comptes de charges des activités ordinaires)
        elif number == 6:
            instance.position_bilan = "Charges"
        
        # 7 : Produits (Comptes de produits des activités ordinaires)
        elif number == 7:
            instance.position_bilan = "Produits"
        
        # 8 : Peut être Charges ou Produits, mais Charges par défaut (Autres charges et produits)
        elif number == 8:
            instance.position_bilan = "Charges"
        
        # Définir actif à True par défaut
        instance.actif = True
        
        # Sauvegarder si commit est True
        if commit:
            instance.save()
        
        return instance

# Ajouter le décorateur pour enregistrer le modèle dans l'administration
@admin.register(AccountClass)
class AccountClassAdmin(admin.ModelAdmin):
    form = AccountClassForm
    # Ajoutez les champs que vous souhaitez afficher dans la liste
    list_display = ('number', 'get_original_name', 'position_bilan', 'actif', 'date_creation')
    list_filter = ('position_bilan', 'actif')
    search_fields = ('name', 'number')
    readonly_fields = ('name', 'description', 'position_bilan', 'actif', 'date_creation')

    # Méthode pour afficher le nom original du dictionnaire NOMS_CLASSES
    def get_original_name(self, obj):
        return AccountClass.NOMS_CLASSES.get(obj.number, "")
    get_original_name.short_description = "NOM"  # Titre de la colonne
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_class_info/<int:number>/', self.admin_site.admin_view(self.get_class_info), name='get_class_info'),
        ]
        return custom_urls + urls
    
    def get_class_info(self, request, number):
        """Renvoie les informations de classe basées sur le numéro selon le plan comptable OHADA"""
        try:
            number = int(number)
            if 1 <= number <= 8:
                # Position dans le bilan selon le numéro
                position = ""
                
                # 1 : Passif (Comptes de ressources durables)
                if number == 1:
                    position = "Passif"
                
                # 2 et 3 : Actif (Comptes d'actif immobilisé et Comptes de stocks)
                elif number == 2 or number == 3:
                    position = "Actif"
                
                # 4 : Peut être Actif ou Passif, mais Passif par défaut (Comptes de tiers)
                elif number == 4:
                    position = "Passif"
                
                # 5 : Peut être Actif ou Passif, mais Actif par défaut (Comptes de trésorerie)
                elif number == 5:
                    position = "Actif"
                
                # 6 : Charges (Comptes de charges des activités ordinaires)
                elif number == 6:
                    position = "Charges"
                
                # 7 : Produits (Comptes de produits des activités ordinaires)
                elif number == 7:
                    position = "Produits"
                
                # 8 : Peut être Charges ou Produits, mais Charges par défaut (Autres charges et produits)
                elif number == 8:
                    position = "Charges"
                    
                return JsonResponse({
                    'name': AccountClass.NOMS_CLASSES.get(number, ""),
                    'description': AccountClass.DESCRIPTIONS_CLASSES.get(number, ""),
                    'position': position
                })
        except (ValueError, TypeError):
            pass
            
        return JsonResponse({'error': 'Numéro de classe invalide'}, status=400)
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': ('number',),
                'description': 'Sélectionnez un numéro de classe comptable. Les autres informations seront générées automatiquement.',
            }),
        ]
        
        # Si on est en mode édition, ajouter les champs en lecture seule
        if obj:
            fieldsets.extend([
                ('Informations générées automatiquement', {
                    'fields': ('name', 'description', 'position_bilan', 'actif'),
                    'description': 'Ces informations ont été générées automatiquement à partir du numéro de classe.',
                }),
                ('Métadonnées', {
                    'fields': ('date_creation',),
                    'classes': ('collapse',),
                }),
            ])
        
        return fieldsets
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Injecter le script JavaScript directement dans le contexte
        extra_context['javascript'] = """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Créer les champs d'affichage
                function createDisplayFields() {
                    const formRow = document.querySelector('.form-row.field-number');
                    if (!formRow) return;

                    // Créer le champ pour le libellé
                    const nameRow = document.createElement('div');
                    nameRow.className = 'form-row field-preview_name';
                    nameRow.innerHTML = `
                        <div>
                            <label style="white-space: nowrap;">Libellé (généré automatiquement) :</label>
                            <div class="readonly" id="preview_name" style="padding: 10px; background: #f5f9ff; border: 1px solid #ddd; min-height: 20px; margin-top: 5px;"></div>
                        </div>
                    `;
                                        // Créer le champ pour la description
                    const descRow = document.createElement('div');
                    descRow.className = 'form-row field-preview_description';
                    descRow.innerHTML = `
                        <div>
                            <label style="white-space: nowrap;">Description (générée automatiquement) :</label>
                            <div class="readonly" id="preview_description" style="padding: 10px; background: #f5f9ff; border: 1px solid #ddd; min-height: 100px; margin-top: 5px;"></div>
                        </div>
                    `;

                    // Créer le champ pour la position dans le bilan
                    const positionRow = document.createElement('div');
                    positionRow.className = 'form-row field-preview_position';
                    positionRow.innerHTML = `
                        <div>
                            <label style="white-space: nowrap;">Position dans le bilan (générée automatiquement) :</label>
                            <div class="readonly" id="preview_position" style="padding: 10px; background: #f5f9ff; border: 1px solid #ddd; min-height: 20px; margin-top: 5px;"></div>
                        </div>
                    `;
                    
                    // Insérer les champs après le champ numéro
                    formRow.after(nameRow);
                    nameRow.after(descRow);
                    descRow.after(positionRow);
                }
                
                // Fonction pour mettre à jour les champs en fonction du numéro sélectionné
                function updateInfo() {
                    const number = document.getElementById('id_number').value;
                    if (!number) return;
                    
                    // Appeler l'API pour obtenir les informations
                    fetch(`/admin/accounts/accountclass/get_class_info/${number}/`)
                        .then(response => response.json())
                        .then(data => {
                            // Mettre à jour les champs de prévisualisation
                            document.getElementById('preview_name').textContent = data.name;
                            document.getElementById('preview_description').textContent = data.description;
                            document.getElementById('preview_position').textContent = data.position;
                        })
                        .catch(error => {
                            console.error('Erreur lors de la récupération des informations:', error);
                        });
                }
                
                // Créer les champs
                createDisplayFields();
                
                // Ajouter un écouteur d'événement au champ de numéro
                const numberSelect = document.getElementById('id_number');
                if (numberSelect) {
                    numberSelect.addEventListener('change', updateInfo);
                    
                    // Déclencher la mise à jour initiale
                    updateInfo();
                }
            });
        </script>
        """
        
        return super().add_view(request, form_url, extra_context)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        
        # Assurez-vous que notre JavaScript est inclus dans le modèle
        response = super().changeform_view(request, object_id, form_url, extra_context)
        
        if hasattr(response, 'context_data') and 'javascript' in extra_context:
            response.context_data['javascript'] = extra_context['javascript']
            
        return response