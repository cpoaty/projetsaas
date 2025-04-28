from django.test import TestCase
from ...models.account_class import AccountClass
from ...models.account_group import AccountGroup

class AccountGroupModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Créer les objets nécessaires pour les tests
        account_class = AccountClass.objects.create(
            number=1,
            name="Comptes de capitaux"
        )
        AccountGroup.objects.create(
            account_class=account_class,
            number=0,
            name="Capital et réserves",
            description="Capital, réserves et report à nouveau"
        )

    def test_get_full_number(self):
        account_group = AccountGroup.objects.get(number=0)
        self.assertEqual(account_group.get_full_number(), "10")

    def test_object_name_is_full_number_dash_name(self):
        account_group = AccountGroup.objects.get(number=0)
        expected_object_name = f"{account_group.get_full_number()} - {account_group.name}"
        self.assertEqual(str(account_group), expected_object_name)