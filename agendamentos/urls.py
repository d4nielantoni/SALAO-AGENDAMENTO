from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('agendamentos/', views.lista_agendamentos, name='lista_agendamentos'),
    path('agendamentos/novo/', views.novo_agendamento, name='novo_agendamento'),
    path('agendamentos/deletar/<int:agendamento_id>/', views.deletar_agendamento, name='deletar_agendamento'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
