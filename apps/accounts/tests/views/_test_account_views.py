from django.test import TestCase
from django.urls import reverse
from ...models.account_class import AccountClass
from ...models.account_group import AccountGroup
from ...models.account_type import AccountType
from ...models.account import Account

class AccountListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Créer quelques classes de comptes pour les tests
        number_of_classes = 3
        for class_num in range(1, number_of_classes + 1):
            account_class = AccountClass.objects.create(
                number=class_num,
                name=f'Classe {class_num}',
                description=f'Description de la classe {class_num}'
            )
            
            # Ajouter des groupes à chaque classe
            for group_num in range(1, 3):
                group = AccountGroup.objects.create(
                    account_class=account_class,
                    number=group_num,
                    name=f'Groupe {class_num}{group_num}',
                    description=f'Description du groupe {class_num}{group_num}'
                )
                
                # Ajouter un type de compte
                account_type = AccountType.objects.create(
                    code=f'type{class_num}{group_num}',
                    name='Actif' if class_num % 2 == 0 else 'Passif'
                )
                
                # Ajouter des comptes à chaque groupe
                for account_num in range(1, 3):
                    Account.objects.create(
                        account_group=group,
                        number=f'{account_num}00',
                        name=f'Compte {class_num}{group_num}{account_num}00',
                        description=f'Description du compte {class_num}{group_num}{account_num}00',
                        account_type=account_type,
                        is_active=True
                    )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/account_list.html')

    def test_context_contains_account_classes(self):
        response = self.client.get(reverse('account_list'))
        self.assertTrue('account_classes' in response.context)
        self.assertEqual(len(response.context['account_classes']), 3)
        
    def test_account_classes_contain_groups(self):
        response = self.client.get(reverse('account_list'))
        account_classes = response.context['account_classes']
        # Vérifier que chaque classe a des groupes
        for account_class in account_classes:
            self.assertTrue(hasattr(account_class, 'groups'))
            self.assertEqual(account_class.groups.count(), 2)