from django.db import models
from .account_class import AccountClass

class AccountGroup(models.Model):
    """
    Groupe de compte (ex: 10, 11, 40, etc.)
    """
    account_class = models.ForeignKey(AccountClass, on_delete=models.CASCADE, related_name='groups')
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        app_label = 'accounts'
        ordering = ['number']
        unique_together = [['account_class', 'number']]
        verbose_name = "Groupe de comptes"
        verbose_name_plural = "Groupes de comptes"
    
    def __str__(self):
        return f"{self.account_class.number}{self.number} - {self.name}"
    
    def get_full_number(self):
        return f"{self.account_class.number}{self.number}"
