from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from ..models.account_class import AccountClass
from ..models.account import Account
from ..forms.account_forms import AccountForm

class AccountListView(ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_classes'] = AccountClass.objects.prefetch_related(
            'groups', 'groups__accounts'
        ).all()
        return context

account_list = AccountListView.as_view()

class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'

account_detail = AccountDetailView.as_view()

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account_list')

account_create = AccountCreateView.as_view()

class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account_list')

account_update = AccountUpdateView.as_view()
