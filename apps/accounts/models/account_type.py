from django.db import models

class AccountType(models.Model):
    """
    Type de compte (Actif, Passif, Charge, Produit, Capitaux propres)
    """
    # Codes techniques
    AC = 'AC'
    PA = 'PA'
    CH = 'CH'
    PR = 'PR'
    CP = 'CP'
    
    # Options pour le champ code - affiche les codes techniques
    CODE_CHOICES = [
        (AC, AC),  # Affiche 'AC' dans le sélecteur
        (PA, PA),  # Affiche 'PA' dans le sélecteur
        (CH, CH),  # Affiche 'CH' dans le sélecteur
        (PR, PR),  # Affiche 'PR' dans le sélecteur
        (CP, CP)   # Affiche 'CP' dans le sélecteur
    ]
    
    # Correspondance entre codes et noms descriptifs
    TYPE_NAMES = {
        AC: 'Actif',
        PA: 'Passif',
        CH: 'Charge',
        PR: 'Produit',
        CP: 'Capitaux propres'
    }

    # Descriptions détaillées des types de comptes
    DESCRIPTIONS = {
        AC: "Éléments qui représentent une valeur économique positive pour l'entreprise",
        PA: "Dettes et obligations financières de l'entreprise",
        CH: "Dépenses encourues pour générer des revenus",
        PR: "Produits générés par l'activité de l'entreprise",
        CP: "Valeur résiduelle des actifs après déduction des passifs"
    }
    
    code = models.CharField(
        max_length=5, 
        unique=True, 
        primary_key=True,
        choices=CODE_CHOICES,
        help_text="Code unique du type de compte (AC, PA, CH, PR, CP)"
    )
    
    name = models.CharField(
        max_length=50,
        help_text="Nom descriptif du type de compte"
    )

    description = models.CharField(
        max_length=255,  # ou toute autre longueur appropriée
        blank=True,
        verbose_name="Description",
        editable=False,
        help_text="Description détaillée du type de compte (générée automatiquement)"
    )
    
    class Meta:
        app_label = 'accounts'
        verbose_name = "Type de compte"
        verbose_name_plural = "Types de comptes"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} = {self.name}"
    
    def save(self, *args, **kwargs):
        # Définir automatiquement le nom d'après le code
        self.name = self.TYPE_NAMES.get(self.code, self.code)
        super().save(*args, **kwargs)
        
    def get_description(self):
        """Retourne la description du type de compte"""
        return self.DESCRIPTIONS.get(self.code, "")
