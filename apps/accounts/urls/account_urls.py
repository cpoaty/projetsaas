from django.urls import path
from ..views.account_views import account_list

urlpatterns = [
    path('', account_list, name='account_list'),
]
