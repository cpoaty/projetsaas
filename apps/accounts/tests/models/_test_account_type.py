from django.test import TestCase
from ...models.account_type import AccountType

class AccountTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Créer un objet AccountType pour les tests
        AccountType.objects.create(
            code="actif",
            name="Actif"
        )

    def test_code_label(self):
        account_type = AccountType.objects.get(code="actif")
        field_label = account_type._meta.get_field('code').verbose_name
        self.assertEqual(field_label, 'code')

    def test_name_label(self):
        account_type = AccountType.objects.get(code="actif")
        field_label = account_type._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_object_name_is_name(self):
        account_type = AccountType.objects.get(code="actif")
        self.assertEqual(str(account_type), account_type.get_name_display())