from django.db import models
from django.utils import timezone
from datetime import timedelta

class Profissional(models.Model):
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
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    nome_cliente = models.CharField(max_length=100) 
    contato_cliente = models.CharField(max_length=15) 
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profissional} - {self.servico} em {self.data_hora}"
