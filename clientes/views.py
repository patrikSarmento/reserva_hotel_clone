from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser, Reserva  # Modelo corrigido

VAGAS_TOTAIS = 10

def cadastrar_cliente(request):
    clientes = CustomUser.objects.count()
    vagas_disponiveis = VAGAS_TOTAIS - clientes
    mensagens_erro = []

    if request.method == 'POST':
        if vagas_disponiveis > 0:
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            cpf = request.POST.get('cpf')
            senha = request.POST.get('senha')

            try:
                # Usar create_user para criar e salvar usuário com senha corretamente
                usuario = CustomUser.objects.create_user(
                    nome=nome,
                    email=email,
                    cpf=cpf,
                    password=senha
                )
                messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
                return redirect('login')
            except ValidationError as e:
                for campo, erros in e.message_dict.items():
                    for erro in erros:
                        mensagens_erro.append(f"{campo}: {erro}")
            except Exception as e:
                mensagens_erro.append(f"Erro inesperado: {str(e)}")
        else:
            mensagens_erro.append("Não há vagas disponíveis no momento.")

    return render(request, 'clientes/cadastro.html', {
        'vagas_disponiveis': vagas_disponiveis,
        'mensagens_erro': mensagens_erro,
        'mostrar_navbar': False,
    })

@login_required
def listar_clientes(request):
    clientes = CustomUser.objects.all().order_by('-data_cadastro')
    return render(request, 'clientes/lista.html', {'clientes': clientes})

def logout_usuario(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect('login')

def raiz(request):
    return redirect('cadastro')

def quartos(request):
    dias = request.GET.get('dias', 1)
    try:
        dias = int(dias)
    except ValueError:
        dias = 1

    quartos_lista = [
        {'nome': 'Quarto Standard', 'valor': 500, 'imagem': 'https://via.placeholder.com/350x200?text=Quarto+Standard'},
        {'nome': 'Quarto Luxo', 'valor': 1000, 'imagem': 'https://via.placeholder.com/350x200?text=Quarto+Luxo'},
        {'nome': 'Suíte Presidencial', 'valor': 2000, 'imagem': 'https://via.placeholder.com/350x200?text=Suíte+Presidencial'},
    ]

    context = {
        'quartos_disponiveis': len(quartos_lista),
        'quartos': quartos_lista,
        'dias': dias,
    }

    return render(request, 'clientes/quartos.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # assume que usa email como username
        senha = request.POST.get('password')

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
            login(request, usuario)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('quartos')
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, 'clientes/login.html', {
        'mostrar_navbar': False
    })

def quarto_standard(request):
    quarto = {
        'nome': 'Quarto Standard',
        'valor': 500,
        'descricao': 'Este é o quarto standard...',
        'imagem': 'https://via.placeholder.com/700x400?text=Quarto+Standard',
    }
    return render(request, 'clientes/quarto_standard.html', {'quarto': quarto})

def quarto_luxo(request):
    quarto = {
        'nome': 'Quarto Luxo',
        'valor': 850,
        'descricao': 'Este é o quarto luxo...',
        'imagem': 'clientes/images/quarto_luxo1.jpeg',
    }
    return render(request, 'clientes/quarto_luxo.html', {'quarto': quarto})

def suite_presidencial(request):
    suite = {
        'nome': 'Suíte Presidencial',
        'valor': 2000,
        'descricao': 'A Suíte Presidencial é o que há de mais luxuoso...',
        'imagem1': 'clientes/images/suite_presidencial1.jpeg',
        'imagem2': 'clientes/images/suite_presidencial2.jpeg',
    }
    return render(request, 'clientes/suite_presidencial.html', {'quarto': suite})

@login_required
def confirmar_reserva(request, tipo_quarto):
    if request.method == 'POST':
        dias = request.POST.get('dias')

        if not dias:
            messages.error(request, "Preencha a quantidade de dias.")
            return redirect('confirmar_reserva', tipo_quarto=tipo_quarto)

        try:
            dias = int(dias)
            if dias < 1:
                raise ValueError()
        except ValueError:
            messages.error(request, "Quantidade de dias inválida.")
            return redirect('confirmar_reserva', tipo_quarto=tipo_quarto)

        cliente = CustomUser.objects.filter(email=request.user.email).first()
        if not cliente:
            messages.error(request, "Cliente não encontrado para o usuário logado.")
            return redirect('quartos')

        Reserva.objects.create(
            cliente=cliente,
            quarto=tipo_quarto,
            dias=dias
        )

        messages.success(request, "Reserva confirmada com sucesso!")
        return redirect('sucesso')

    return render(request, 'clientes/confirmar_reserva.html', {'quarto': tipo_quarto})

@login_required
def sucesso(request):
    return render(request, 'clientes/sucesso.html')

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva cancelada com sucesso!")
        return redirect('listar_reservas')

    return render(request, 'clientes/cancelar_reserva.html', {'reserva': reserva})

@login_required
def listar_reservas(request):
    cliente = CustomUser.objects.filter(email=request.user.email).first()
    if not cliente:
        messages.error(request, "Cliente não encontrado para o usuário.")
        return redirect('quartos')

    reservas = Reserva.objects.filter(cliente=cliente).order_by('-data_reserva')
    return render(request, 'clientes/lista_reservas.html', {'reservas': reservas})
