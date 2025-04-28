from django.test import TestCase
from ...models.account_class import AccountClass

class AccountClassModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Créer un objet AccountClass pour les tests
        AccountClass.objects.create(
            number=1,
            name="Comptes de capitaux",
            description="Capitaux propres, autres fonds propres, etc."
        )

    def test_number_label(self):
        account_class = AccountClass.objects.get(number=1)
        field_label = account_class._meta.get_field('number').verbose_name
        self.assertEqual(field_label, 'number')

    def test_name_label(self):
        account_class = AccountClass.objects.get(number=1)
        field_label = account_class._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        account_class = AccountClass.objects.get(number=1)
        field_label = account_class._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_object_name_is_number_dash_name(self):
        account_class = AccountClass.objects.get(number=1)
        expected_object_name = f"{account_class.number} - {account_class.name}"
        self.assertEqual(str(account_class), expected_object_name)