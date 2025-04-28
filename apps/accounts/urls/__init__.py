# Simplifiez pour commencer
from django.urls import path
from ..views.account_views import account_list, account_create, account_detail, account_update

urlpatterns = [
    path('', account_list, name='account_list'),
    path('create/', account_create, name='account_create'),
    path('<int:pk>/', account_detail, name='account_detail'),
    path('<int:pk>/update/', account_update, name='account_update'),
]
