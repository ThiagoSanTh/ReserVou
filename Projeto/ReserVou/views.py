from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Hotel, Quarto, Cliente, Reserva
from .forms import QuartoForm, ClienteForm
from datetime import datetime

# Create your views here.
def pagina_inicial(request):
    clientes = Cliente.objects.all()
    hoteis = Hotel.objects.all()
    return render(request, 'ReserVou/pagina_inicial.html', {'clientes': clientes, 'hoteis': hoteis})

def gerenciar_hoteis(request):
    hoteis = Hotel.objects.prefetch_related('quarto').all()  # Otimiza a busca dos quartos
    return render(request, 'ReserVou/hotel/gerenciar_hoteis.html', {'hoteis': hoteis})

def cadastrar_hotel(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')

        if nome and endereco:
            Hotel.objects.create(nome=nome, endereco=endereco)
            return redirect('gerenciar_hoteis')
        else:
            erro = "Todos os campos são obrigatórios."
            return render(request, 'ReserVou/hotel/cadastrar_hotel.html', {'erro': erro})

    return render(request, 'ReserVou/hotel/cadastrar_hotel.html')

def cadastrar_quarto(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    if request.method == 'POST':
        form = QuartoForm(request.POST)
        if form.is_valid():
            novo_quarto = form.save(commit=False)
            novo_quarto.hotel = hotel
            novo_quarto.save()
            return redirect('gerenciar_hoteis')
    else:
        form = QuartoForm()

    return render(request, 'ReserVou/hotel/cadastrar_quarto.html', {'form': form, 'hotel': hotel})


def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if nome and email and telefone:
            Cliente.objects.create(nome=nome, email=email, telefone=telefone)
            return redirect('home')
        else:
            erro = "Todos os campos são obrigatórios."
            return render(request, 'ReserVou/cliente/cadastrar_cliente.html', {'erro': erro})

    return render(request, 'ReserVou/cliente/cadastrar_cliente.html')
            
def perfil_cliente(request, id):
    cliente = Cliente.objects.get(id = id)
    reservas = Reserva.objects.filter(cliente = cliente).select_related('quarto', 'hotel')
    
    return render(request, 'ReserVou/cliente/perfil_cliente.html', {
        'cliente': cliente,
        'reservas': reservas,
    })
    
def reservar_listar_hoteis(request):
    cliente_id = request.GET.get('cliente_id')
    hoteis = Hotel.objects.all()
    
    return render(request, 'ReserVou/hotel/reservar_listar_hoteis.html', {
        'hoteis' : hoteis,
        'cliente_id' : cliente_id
    })
    
def listar_quartos(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    cliente_id = request.GET.get('cliente_id')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    quartos_disponiveis = []

    if checkin and checkout:
        # Converte as datas de string para objeto date
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()

        # Busca quartos disponíveis
        quartos_disponiveis = Quarto.objects.filter(hotel=hotel).exclude(
            reservas__check_in__lt=checkout_date,
            reservas__check_out__gt=checkin_date
        )

    context = {
        'hotel': hotel,
        'cliente_id': cliente_id,
        'checkin': checkin,
        'checkout': checkout,
        'quartos_disponiveis': quartos_disponiveis,
    }
    return render(request, 'ReserVou/hotel/listar_quartos.html', context)

def fazer_reserva(request, quarto_id):
    cliente_id = request.GET.get('cliente_id')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    cliente = get_object_or_404(Cliente, id=cliente_id)
    quarto = get_object_or_404(Quarto, id=quarto_id)
    hotel = quarto.hotel

    # Calcular total da reserva
    data_in = datetime.strptime(checkin, "%Y-%m-%d").date()
    data_out = datetime.strptime(checkout, "%Y-%m-%d").date()
    dias = (data_out - data_in).days
    total = dias * quarto.preco_diaria

    context = {
        'cliente': cliente,
        'hotel': hotel,
        'quarto': quarto,
        'checkin': checkin,
        'checkout': checkout,
        'total': total,
    }

    return render(request, 'ReserVou/fazer_reserva.html', context)

def fazer_pagamento(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        quarto_id = request.POST.get('quarto_id')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        tipo_pagamento = request.POST.get('tipo_pagamento')

        cliente = get_object_or_404(Cliente, id=cliente_id)
        quarto = get_object_or_404(Quarto, id=quarto_id)
        hotel = quarto.hotel

        data_in = datetime.strptime(checkin, "%Y-%m-%d").date()
        data_out = datetime.strptime(checkout, "%Y-%m-%d").date()
        dias = (data_out - data_in).days
        total = dias * quarto.preco_diaria

        # Salvar a reserva
        reserva = Reserva.objects.create(
            cliente=cliente,
            hotel=hotel,
            quarto=quarto,
            check_in=data_in,
            check_out=data_out
        )

        # Exibir confirmação (ou redirecionar para outra página de sucesso)
        return render(request, 'ReserVou/confirmacao_pagamento.html', {
            'reserva': reserva,
            'tipo_pagamento': tipo_pagamento,
            'total': total,
        })

    else:
        # GET: carregar os dados para exibir o formulário
        cliente_id = request.GET.get('cliente_id')
        quarto_id = request.GET.get('quarto_id')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')

        cliente = get_object_or_404(Cliente, id=cliente_id)
        quarto = get_object_or_404(Quarto, id=quarto_id)
        hotel = quarto.hotel

        data_in = datetime.strptime(checkin, "%Y-%m-%d").date()
        data_out = datetime.strptime(checkout, "%Y-%m-%d").date()
        dias = (data_out - data_in).days
        total = dias * quarto.preco_diaria

        context = {
            'cliente': cliente,
            'hotel': hotel,
            'quarto': quarto,
            'checkin': checkin,
            'checkout': checkout,
            'total': total,
        }

        return render(request, 'ReserVou/fazer_pagamento.html', context)

def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('perfil_cliente', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ReserVou/cliente/editar_cliente.html', {'form': form, 'cliente': cliente})

def deletar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('home')
    return render(request, 'ReserVou/cliente/confirmar_deletar_cliente.html', {'cliente': cliente})