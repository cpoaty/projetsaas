from django.db import models
from .account_group import AccountGroup
from .account_type import AccountType

class Account(models.Model):
    """
    Compte comptable
    """
    account_group = models.ForeignKey(AccountGroup, on_delete=models.CASCADE, related_name='accounts')
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'accounts'
        ordering = ['number']
        unique_together = [['account_group', 'number']]
        verbose_name = "Compte"
        verbose_name_plural = "Comptes"
    
    def __str__(self):
        return f"{self.get_full_number()} - {self.name}"
    
    def get_full_number(self):
        """Retourne le numéro complet du compte (ex: 101200)"""
        return f"{self.account_group.get_full_number()}{self.number}"
    
    def save(self, *args, **kwargs):
        # Validation pour s'assurer que le numéro ne dépasse pas 8 chiffres au total
        full_number = f"{self.account_group.get_full_number()}{self.number}"
        if len(full_number) > 8:
            raise ValueError("Le numéro de compte ne peut pas dépasser 8 chiffres au total")
        super().save(*args, **kwargs)
