from django.contrib import admin
from django.urls import path, include
from agendamentos.views import home  # Importe a view home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Rota principal
    path('agendamentos/', include('agendamentos.urls')),  # Inclui URLs do app agendamentos
]
