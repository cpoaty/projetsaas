# apps/accounts/management/commands/init_account_types.py

# apps/accounts/management/commands/init_account_types.py

from django.core.management.base import BaseCommand
from accounts.models.account_type import AccountType

class Command(BaseCommand):
    help = 'Initialise les types de compte de base'

    def handle(self, *args, **options):
        types_created = 0
        types_updated = 0
        
        # Les types sont déjà définis dans le modèle, il suffit de les créer
        for code, name in AccountType.TYPE_CHOICES:
            obj, created = AccountType.objects.update_or_create(
                code=code
                # Pas besoin de defaults car le name est généré automatiquement
            )
            
            if created:
                types_created += 1
                self.stdout.write(self.style.SUCCESS(f"Créé type de compte: {code} - {obj.name}"))
            else:
                types_updated += 1
                self.stdout.write(self.style.WARNING(f"Mis à jour type de compte: {code} - {obj.name}"))
        
        self.stdout.write(self.style.SUCCESS(f"{types_created} types de compte créés, {types_updated} mis à jour."))