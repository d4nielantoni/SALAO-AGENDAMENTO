from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Profissional, Servico, Agendamento

def home(request):
    return render(request, 'agendamentos/home.html')

def gerar_horarios():
    """Gera uma lista de horários entre 9:00 e 18:00 em intervalos de 30 minutos."""
    horarios = []
    hora = datetime.strptime("09:00", "%H:%M")
    fim = datetime.strptime("18:00", "%H:%M")
    while hora <= fim:
        horarios.append(hora.strftime("%H:%M"))
        hora += timedelta(minutes=30)
    return horarios

def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all() 
    return render(request, 'agendamentos/lista.html', {'agendamentos': agendamentos})


def novo_agendamento(request):
    if request.method == 'POST':
        profissional_id = request.POST['profissional']
        servico_id = request.POST['servico']
        data = request.POST['data']
        horario = request.POST['horario']
        nome_cliente = request.POST['nome_cliente']
        contato_cliente = request.POST['contato_cliente']

        profissional = Profissional.objects.get(id=profissional_id)
        servico = Servico.objects.get(id=servico_id)

        data_hora = f"{data} {horario}"
        data_hora = datetime.strptime(data_hora, "%Y-%m-%d %H:%M")

        Agendamento.objects.create(
            profissional=profissional,
            servico=servico,
            data_hora=data_hora,
            nome_cliente=nome_cliente,
            contato_cliente=contato_cliente
        )
        return redirect('lista_agendamentos')

    profissionais = Profissional.objects.all()
    servicos = Servico.objects.all()
    horarios = gerar_horarios() 
    return render(request, 'agendamentos/novo.html', {
        'profissionais': profissionais,
        'servicos': servicos,
        'horarios': horarios
    })
