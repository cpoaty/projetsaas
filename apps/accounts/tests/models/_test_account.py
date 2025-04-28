from django.test import TestCase
from ...models.account_class import AccountClass
from ...models.account_group import AccountGroup
from ...models.account_type import AccountType
from ...models.account import Account

class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Créer les objets nécessaires pour les tests
        account_class = AccountClass.objects.create(
            number=1,
            name="Comptes de capitaux"
        )
        account_group = AccountGroup.objects.create(
            account_class=account_class,
            number=0,
            name="Capital et réserves"
        )
        account_type = AccountType.objects.create(
            code="passif",
            name="Passif"
        )
        Account.objects.create(
            account_group=account_group,
            number="100",
            name="Capital social",
            description="Capital de l'entreprise",
            account_type=account_type,
            is_active=True
        )

    def test_get_full_number(self):
        account = Account.objects.get(number="100")
        self.assertEqual(account.get_full_number(), "10100")

    def test_object_name_is_full_number_dash_name(self):
        account = Account.objects.get(number="100")
        expected_object_name = f"{account.get_full_number()} - {account.name}"
        self.assertEqual(str(account), expected_object_name)

    def test_save_validate_number_length(self):
        account_class = AccountClass.objects.get(number=1)
        account_group = AccountGroup.objects.get(account_class=account_class)
        account_type = AccountType.objects.get(code="passif")
        
        # Test avec un numéro trop long
        with self.assertRaises(ValueError):
            account = Account(
                account_group=account_group,
                number="1234567",  # Trop long, car 10 + 1234567 = 8 chiffres (limite)
                name="Test numéro trop long",
                account_type=account_type
            )
            account.save()