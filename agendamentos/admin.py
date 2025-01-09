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
    list_display = ('nome_cliente', 'profissional', 'get_servicos', 'data_hora')
    list_filter = ('profissional', 'data_hora', 'servicos')
    search_fields = ('nome_cliente', 'contato_cliente')
    filter_horizontal = ('servicos',)

    def get_servicos(self, obj):
        return ", ".join([s.nome for s in obj.servicos.all()])
    get_servicos.short_description = 'Serviços'
