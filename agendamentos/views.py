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
        raise ValueError("Desculpe, não funcionamos aos domingos.")
    
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
    ).prefetch_related('servicos').select_related('profissional').order_by('data_hora')
    return render(request, 'agendamentos/lista.html', {'agendamentos': agendamentos})

@login_required(login_url='login')
def deletar_agendamento(request, agendamento_id):
    # Verifica se o usuário é um profissional
    if not hasattr(request.user, 'profissional'):
        messages.error(request, 'Acesso restrito a profissionais.')
        return redirect('home')
    
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id, profissional=request.user.profissional)
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso!')
    except Agendamento.DoesNotExist:
        messages.error(request, 'Agendamento não encontrado.')
    
    return redirect('lista_agendamentos')

def novo_agendamento(request):
    profissionais = Profissional.objects.all()
    servicos = Servico.objects.all()
    horarios = gerar_horarios()
    today = datetime.now().date()

    context = {
        'profissionais': profissionais,
        'servicos': servicos,
        'horarios': horarios,
        'today': today
    }

    if request.method == 'POST':
        try:
            profissional_id = request.POST['profissional']
            servicos_ids = request.POST.getlist('servicos')
            data = request.POST['data']
            horario = request.POST['horario']
            nome_cliente = request.POST['nome_cliente']
            contato_cliente = request.POST['contato_cliente']

            # Validação dos campos obrigatórios
            if not all([profissional_id, servicos_ids, data, horario, nome_cliente, contato_cliente]):
                context['error'] = 'Todos os campos são obrigatórios.'
                return render(request, 'agendamentos/novo.html', context)

            # Validação do horário
            try:
                if not is_horario_disponivel(data, horario, profissional_id):
                    context['error'] = 'Horário não disponível. Por favor, escolha outro horário.'
                    return render(request, 'agendamentos/novo.html', context)
            except ValueError as e:
                context['error'] = str(e)
                return render(request, 'agendamentos/novo.html', context)

            try:
                profissional = Profissional.objects.get(id=profissional_id)
                servicos_selecionados = Servico.objects.filter(id__in=servicos_ids)

                if not servicos_selecionados:
                    context['error'] = 'Selecione pelo menos um serviço.'
                    return render(request, 'agendamentos/novo.html', context)

                data_hora = f"{data} {horario}"
                data_hora = datetime.strptime(data_hora, "%Y-%m-%d %H:%M")

                # Validar se a data não é passada
                if data_hora < datetime.now():
                    context['error'] = 'Não é possível agendar para uma data passada.'
                    return render(request, 'agendamentos/novo.html', context)

                # Criar o agendamento
                agendamento = Agendamento.objects.create(
                    profissional=profissional,
                    data_hora=data_hora,
                    nome_cliente=nome_cliente,
                    contato_cliente=contato_cliente
                )
                # Adicionar os serviços selecionados
                agendamento.servicos.set(servicos_selecionados)

                messages.success(request, 'Agendamento realizado com sucesso!')
                if request.user.is_authenticated and hasattr(request.user, 'profissional'):
                    return redirect('lista_agendamentos')
                return redirect('home')

            except Profissional.DoesNotExist:
                context['error'] = 'Profissional não encontrado.'
                return render(request, 'agendamentos/novo.html', context)
            except Exception as e:
                context['error'] = f'Erro ao criar agendamento: {str(e)}'
                return render(request, 'agendamentos/novo.html', context)

        except KeyError as e:
            context['error'] = f'Campo obrigatório não preenchido: {str(e)}'
            return render(request, 'agendamentos/novo.html', context)
        except Exception as e:
            context['error'] = f'Erro inesperado: {str(e)}'
            return render(request, 'agendamentos/novo.html', context)

    return render(request, 'agendamentos/novo.html', context)
