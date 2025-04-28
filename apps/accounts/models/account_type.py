from django.db import models

class AccountType(models.Model):
    """
    Type de compte (Actif, Passif, Dépense, Revenu)
    """
    ACTIF = 'actif'
    PASSIF = 'passif'
    CHARGE = 'charge'
    PRODUIT = 'produit'
    CAPITAUX_PROPRES = 'capitaux_propres'
    
    TYPE_CHOICES = [
        (ACTIF, 'Actif'),
        (PASSIF, 'passif'),
        (CHARGE, 'Dépense'),
        (PRODUIT, 'Revenu'),
        (CAPITAUX_PROPRES, 'Capitaux propres')
    ]
    
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=50, choices=TYPE_CHOICES)
    
    class Meta:
        app_label = 'accounts'
        verbose_name = "Type de compte"
        verbose_name_plural = "Types de comptes"
    
    def __str__(self):
        return self.get_name_display()
