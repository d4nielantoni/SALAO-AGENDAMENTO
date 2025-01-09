from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

class Profissional(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    nome = models.CharField(max_length=50)
    duracao = models.DurationField(help_text="Duração do serviço (ex: 01:00 para 1 hora)")
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    servicos = models.ManyToManyField(Servico)
    data_hora = models.DateTimeField()
    nome_cliente = models.CharField(max_length=100)
    contato_cliente = models.CharField(max_length=15)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        servicos_str = ", ".join([s.nome for s in self.servicos.all()])
        return f"{self.nome_cliente} - {servicos_str} com {self.profissional} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    @property
    def preco_total(self):
        return sum(servico.preco for servico in self.servicos.all())
