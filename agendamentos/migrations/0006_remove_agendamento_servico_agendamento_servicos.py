# Generated by Django 5.0 on 2025-01-09 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agendamentos", "0005_alter_agendamento_criado_em"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agendamento",
            name="servico",
        ),
        migrations.AddField(
            model_name="agendamento",
            name="servicos",
            field=models.ManyToManyField(to="agendamentos.servico"),
        ),
    ]
