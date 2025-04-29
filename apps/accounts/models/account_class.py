from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class AccountClass(models.Model):
    """
    Classe de compte (1-8) selon le plan comptable général.
    Ex: 1 = Comptes de capitaux, 2 = Immobilisations, etc.
    """
    # Dictionnaire contenant les noms et descriptions standard des classes de comptes
    # Dictionnaire contenant les noms et descriptions standard des classes de comptes OHADA
    NOMS_CLASSES = {
        1: "Comptes de ressources durables",
        2: "Comptes d'actif immobilisé",
        3: "Comptes de stocks",
        4: "Comptes de tiers",
        5: "Comptes de trésorerie",
        6: "Comptes de charges des activités ordinaires",
        7: "Comptes de produits des activités ordinaires",
        8: "Comptes des autres charges et des autres produits"
    }
    
    DESCRIPTIONS_CLASSES = {
        1: "Regroupe les comptes de capitaux propres, provisions, emprunts et dettes financières diverses.",
        2: "Regroupe les comptes d'immobilisations incorporelles, corporelles et financières.",
        3: "Regroupe les comptes de stocks de marchandises, matières premières et autres approvisionnements.",
        4: "Regroupe les comptes de fournisseurs, clients et autres débiteurs ou créditeurs.",
        5: "Regroupe les comptes de banque, établissements financiers, caisse et autres valeurs.",
        6: "Regroupe les comptes d'achats, services extérieurs, impôts et taxes, charges de personnel.",
        7: "Regroupe les comptes de ventes, subventions d'exploitation et autres produits.",
        8: "Regroupe les comptes de charges et produits hors activités ordinaires."
    }
    
    POSITION_CHOICES = [
        ("Actif", "Actif"),
        ("Passif", "Passif"),
        ("Charges", "Charges"),
        ("Produits", "Produits"),
    ]
    
    number = models.PositiveSmallIntegerField(
        unique=True, 
        primary_key=True,
        validators=[
            MinValueValidator(1, message="Le numéro de classe doit être au minimum 1."),
            MaxValueValidator(8, message="Le numéro de classe doit être au maximum 8.")
        ],
        verbose_name="Numéro",
        help_text="Entrez un chiffre entre 1 et 8 conformément au plan comptable OHADA."
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="Nom",
        editable=False,  # Rend le champ non modifiable dans l'interface
        help_text="Nom de la classe de comptable."
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Description",
        editable=False,  # Rend le champ non modifiable dans l'interface
        help_text="Description optionnelle détaillant la nature et l'utilisation de cette classe de compte."
    )

    position_bilan = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        verbose_name="Position dans le bilan",
        help_text="Indique si la classe est dans l'Actif, Passif, Charges ou Produits",
        default="Actif"  # Ajout d'une valeur par défaut
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Indique si cette classe est active dans le plan comptable"
    )

    date_creation = models.DateTimeField(
        verbose_name="Date de création",
        auto_now_add=True
    )


    class Meta:
        app_label = 'accounts'
        ordering = ['number']
        verbose_name = "Classe de compte"
        verbose_name_plural = "Classes de comptes"
    
    def __str__(self):
        return f"{self.number} - {self.name}"
    
    def save(self, *args, **kwargs):
        # Automatiquement définir le nom et la description en fonction du numéro
        if self.number in self.NOMS_CLASSES:
            self.name = self.NOMS_CLASSES[self.number]
            self.description = self.DESCRIPTIONS_CLASSES[self.number]
        
        # Déterminer automatiquement la position dans le bilan selon le plan comptable OHADA
        # 1 : Passif (Comptes de ressources durables)
        if self.number == 1:
            self.position_bilan = "Passif"
        
        # 2 et 3 : Actif (Comptes d'actif immobilisé et Comptes de stocks)
        elif self.number == 2 or self.number == 3:
            self.position_bilan = "Actif"
        
        # 4 : Peut être Actif ou Passif, mais Passif par défaut (Comptes de tiers)
        elif self.number == 4:
            self.position_bilan = "Passif"
        
        # 5 : Peut être Actif ou Passif, mais Actif par défaut (Comptes de trésorerie)
        elif self.number == 5:
            self.position_bilan = "Actif"
        
        # 6 : Charges (Comptes de charges des activités ordinaires)
        elif self.number == 6:
            self.position_bilan = "Charges"
        
        # 7 : Produits (Comptes de produits des activités ordinaires)
        elif self.number == 7:
            self.position_bilan = "Produits"
        
        # 8 : Peut être Charges ou Produits, mais Charges par défaut (Autres charges et produits)
        elif self.number == 8:
            self.position_bilan = "Charges"
                
        super().save(*args, **kwargs)
    
    
    def clean(self):
        # Validation supplémentaire au niveau de l'objet si nécessaire
        if self.number < 1 or self.number > 8:
            raise ValidationError({"number": "Le numéro de classe doit être compris entre 1 et 8."})
        
        # Vous pourriez ajouter d'autres validations spécifiques ici
        super().clean()