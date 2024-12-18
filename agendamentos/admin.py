from django.contrib import admin
from .models import Profissional, Servico, Agendamento

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade', 'usuario')
    search_fields = ('nome', 'especialidade')

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    search_fields = ('nome',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'profissional', 'servico', 'data_hora')
    list_filter = ('profissional', 'servico', 'data_hora')
    search_fields = ('nome_cliente', 'contato_cliente')
