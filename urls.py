from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # Pour une page simple

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # Autres URLs de votre projet
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
