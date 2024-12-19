from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Profissional, Servico, Agendamento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'agendamentos/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'profissional'):
            login(request, user)
            return redirect('lista_agendamentos')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'agendamentos/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def is_horario_disponivel(data, horario, profissional_id):
    """Verifica se o horário está disponível para agendamento."""
    data_hora = datetime.strptime(f"{data} {horario}", "%Y-%m-%d %H:%M")
    
    # Verifica se é domingo (0 = segunda, 6 = domingo)
    if data_hora.weekday() == 6:
        return False
    
    # Verifica se o horário está dentro do horário de funcionamento
    hora = data_hora.hour
    minuto = data_hora.minute
    
    # Verifica se está no intervalo do almoço (12:00 às 14:00)
    if hora >= 12 and hora < 14:
        return False
    
    # Verifica se está fora do horário de funcionamento
    if hora < 9 or (hora == 19 and minuto > 0) or hora >= 19:
        return False
    
    # Verifica se já existe agendamento para este horário e profissional
    agendamento_existente = Agendamento.objects.filter(
        profissional_id=profissional_id,
        data_hora=data_hora
    ).exists()
    
    return not agendamento_existente

def gerar_horarios():
    """Gera uma lista de horários entre 9:00 e 19:00, excluindo o intervalo de 12:00 às 14:00."""
    horarios = []
    # Período da manhã (9:00 às 12:00)
    hora = datetime.strptime("09:00", "%H:%M")
    fim_manha = datetime.strptime("12:00", "%H:%M")
    while hora < fim_manha:
        horarios.append(hora.strftime("%H:%M"))
        hora += timedelta(minutes=30)
    
    # Período da tarde (14:00 às 19:00)
    hora = datetime.strptime("14:00", "%H:%M")
    fim_tarde = datetime.strptime("19:00", "%H:%M")
    while hora < fim_tarde:
        horarios.append(hora.strftime("%H:%M"))
        hora += timedelta(minutes=30)
    return horarios

@login_required(login_url='login')
def lista_agendamentos(request):
    # Verifica se o usuário é um profissional
    if not hasattr(request.user, 'profissional'):
        messages.error(request, 'Acesso restrito a profissionais.')
        return redirect('home')
        
    # Mostra apenas os agendamentos do profissional logado
    agendamentos = Agendamento.objects.filter(
        profissional=request.user.profissional
    ).order_by('data_hora')
    return render(request, 'agendamentos/lista.html', {'agendamentos': agendamentos})

def novo_agendamento(request):
    if request.method == 'POST':
        profissional_id = request.POST['profissional']
        servico_id = request.POST['servico']
        data = request.POST['data']
        horario = request.POST['horario']
        nome_cliente = request.POST['nome_cliente']
        contato_cliente = request.POST['contato_cliente']

        # Validação do horário
        if not is_horario_disponivel(data, horario, profissional_id):
            return render(request, 'agendamentos/novo.html', {
                'profissionais': Profissional.objects.all(),
                'servicos': Servico.objects.all(),
                'horarios': gerar_horarios(),
                'error': 'Horário não disponível. Por favor, escolha outro horário.',
                'today': datetime.now().date()
            })

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
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('home')

    profissionais = Profissional.objects.all()
    servicos = Servico.objects.all()
    horarios = gerar_horarios()
    today = datetime.now().date()
    return render(request, 'agendamentos/novo.html', {
        'profissionais': profissionais,
        'servicos': servicos,
        'horarios': horarios,
        'today': today
    })
