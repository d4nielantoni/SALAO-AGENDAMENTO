from django.contrib import admin
from django.urls import path, include
from agendamentos.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('agendamentos/', include('agendamentos.urls')), 
]
