from django.db import models

class AccountClass(models.Model):
    """
    Classe de compte (1-8) selon le plan comptable général.
    Ex: 1 = Comptes de capitaux, 2 = Immobilisations, etc.
    """
    number = models.PositiveSmallIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        app_label = 'accounts'
        ordering = ['number']
        verbose_name = "Classe de compte"
        verbose_name_plural = "Classes de comptes"
    
    def __str__(self):
        return f"{self.number} - {self.name}"