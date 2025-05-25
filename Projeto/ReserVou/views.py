from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View

from .models import Hotel, Quarto, Cliente, Reserva
from .forms import QuartoForm, ClienteForm
from datetime import datetime

# Create your views here.

# -------------- Página Inicial ----------------
#---------------Codgo novo (CBV)----------------
class paginaInicial(ListView):
    model = Hotel
    template_name = 'ReserVou/pagina_inicial.html'
    context_object_name = 'hoteis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        return context

#----------Codgo antigo (FBV)----------------------
#def pagina_inicial(request):
#    clientes = Cliente.objects.all()
#    hoteis = Hotel.objects.all()
#    return render(request, 'ReserVou/pagina_inicial.html', {'clientes': clientes, 'hoteis': hoteis})

#--------------------Hotel------------------------
#-----------------Codgo novo (CBV)----------------
class gerenciarHoteis(ListView):
    model = Hotel
    template_name = 'ReserVou/hotel/gerenciar_hoteis.html'
    context_object_name = 'hoteis'

    def get_queryset(self):
        return Hotel.objects.prefetch_related('quarto').all()

#----------------Codgo antigo (FBV)----------------
#def gerenciar_hoteis(request):
#    hoteis = Hotel.objects.prefetch_related('quarto').all()
#    return render(request, 'ReserVou/hotel/gerenciar_hoteis.html', {'hoteis': hoteis})

#-----------------Codgo novo (CBV)----------------
class cadastrarHotel(CreateView):
    model = Hotel
    fields = ['nome', 'endereco']
    template_name = 'ReserVou/hotel/cadastrar_hotel.html'
    success_url = reverse_lazy('gerenciar_hoteis')

#-----------------Codgo antigo (FBV)----------------
#def cadastrar_hotel(request):
#    if request.method == 'POST':
#        nome = request.POST.get('nome')
#        endereco = request.POST.get('endereco')
#
#        if nome and endereco:
#            Hotel.objects.create(nome=nome, endereco=endereco)
#            return redirect('gerenciar_hoteis')
#        else:
#            erro = "Todos os campos são obrigatórios."
#            return render(request, 'ReserVou/hotel/cadastrar_hotel.html', {'erro': erro})
#
#    return render(request, 'ReserVou/hotel/cadastrar_hotel.html')

#-----------------Codgo novo (CBV)----------------
class editarHotel(UpdateView):
    model = Hotel
    fields = ['nome', 'endereco']
    template_name = 'ReserVou/hotel/editar_hotel.html'
    success_url = reverse_lazy('home')



#-----------------Codgo antigo (FBV)----------------
#def editar_hotel(request, hotel_id):
#    hotel = get_object_or_404(Hotel, id=hotel_id)
#    if request.method == 'POST':
#        nome = request.POST.get('nome')
#        endereco = request.POST.get('endereco')
#        if nome and endereco:
#            hotel.nome = nome
#            hotel.endereco = endereco
#            hotel.save()
#            return redirect('gerenciar_hoteis')
#        else:
#            erro = "Todos os campos são obrigatórios."
#            return render(request, 'ReserVou/hotel/editar_hotel.html', {'hotel': hotel, 'erro': erro})
#    return render(request, 'ReserVou/hotel/editar_hotel.html', {'hotel': hotel})

#-----------------Codgo novo (CBV)----------------
class deletarHotel(DeleteView):
    model = Hotel
    template_name = 'ReserVou/hotel/confirmar_deletar_hotel.html'
    success_url = reverse_lazy('home')
    

#-----------------Codgo antigo (FBV)----------------
#def deletar_hotel(request, hotel_id):
#    hotel = get_object_or_404(Hotel, id=hotel_id)
#    if request.method == 'POST':
#        hotel.delete()
#        return redirect('gerenciar_hoteis')
#    return render(request, 'ReserVou/hotel/confirmar_deletar_hotel.html', {'hotel': hotel})

#Quartos

#-----------------Codgo novo (CBV)----------------
class cadastrarQuarto(CreateView):
    model = Quarto
    form_class = QuartoForm
    template_name = 'ReserVou/hotel/cadastrar_quarto.html'
    success_url = reverse_lazy('gerenciar_hoteis')

    def form_valid(self, form):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'])
        form.instance.hotel = hotel
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = get_object_or_404(Hotel, id=self.kwargs['hotel_id'])
        return context

#-----------------Codgo antigo (FBV)----------------
#def cadastrar_quarto(request, hotel_id):
#    hotel = Hotel.objects.get(id=hotel_id)
#
#    if request.method == 'POST':
#        form = QuartoForm(request.POST)
#        if form.is_valid():
#            novo_quarto = form.save(commit=False)
#            novo_quarto.hotel = hotel
#            novo_quarto.save()
#            return redirect('gerenciar_hoteis')
#    else:
#        form = QuartoForm()
#
#    return render(request, 'ReserVou/hotel/cadastrar_quarto.html', {'form': form, 'hotel': hotel})

#-----------------Codgo novo (CBV)----------------
class editarQuarto(UpdateView):
    model = Quarto
    form_class = QuartoForm
    template_name = 'ReserVou/hotel/editar_quarto.html'
    success_url = reverse_lazy('gerenciar_hoteis')

    def get(self, request, quarto_id):
        quarto = get_object_or_404(Quarto, id=quarto_id)
        return render(request, self.template_name, {'quarto': quarto})
    
    def post(self, request, quarto_id):
        quarto = get_object_or_404(Quarto, id=quarto_id)
        form = self.form_class(request.POST, instance=quarto)
        
        if form.is_valid():
            form.save()
            return redirect('gerenciar_hoteis')
        else:
            return render(request, self.template_name, {'quarto': quarto, 'form': form})

#-----------------Codgo antigo (FBV)----------------
#def editar_quarto(request, quarto_id):
#    quarto = get_object_or_404(Quarto, id=quarto_id)
#    if request.method == 'POST':
#        numero = request.POST.get('numero')
#        tipo = request.POST.get('tipo')
#        preco_diaria = request.POST.get('preco_diaria')
#        status = request.POST.get('status')
#        if numero and tipo and preco_diaria and status:
#            quarto.numero = numero
#            quarto.tipo = tipo
#            quarto.preco_diaria = preco_diaria
#            quarto.status = status
#            quarto.save()
#            return redirect('gerenciar_hoteis')
#        else:
#            erro = "Todos os campos são obrigatórios."
#            return render(request, 'ReserVou/hotel/editar_quarto.html', {'quarto': quarto, 'erro': erro})
#    return render(request, 'ReserVou/hotel/editar_quarto.html', {'quarto': quarto})

#-----------------Codgo novo (CBV)----------------
class deletarQuarto(DeleteView):
    model = Quarto
    template_name = 'ReserVou/hotel/confirmar_deletar_quarto.html'
    success_url = reverse_lazy('gerenciar_hoteis')
    pk_url_kwarg = 'quarto_id'

#-----------------Codgo antigo (FBV)----------------
#def deletar_quarto(request, quarto_id):
#    quarto = get_object_or_404(Quarto, id=quarto_id)
#    if request.method == 'POST':
#        quarto.delete()
#        return redirect('gerenciar_hoteis')
#    return render(request, 'ReserVou/hotel/confirmar_deletar_quarto.html', {'quarto': quarto})
    


#Cliente 

#-----------------Codgo antigo (FBV)----------------
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


#-----------------Codgo antigo (FBV)----------------           
def perfil_cliente(request, id):
    cliente = Cliente.objects.get(id = id)
    reservas = Reserva.objects.filter(cliente = cliente).select_related('quarto', 'hotel')
    
    return render(request, 'ReserVou/cliente/perfil_cliente.html', {
        'cliente': cliente,
        'reservas': reservas,
    })


#-----------------Codgo antigo (FBV)----------------
def selecionar_datas(request):
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        cliente_id = request.POST.get('cliente_id')
        if checkin and checkout and cliente_id:
            # Redireciona para a listagem de hotéis, passando as datas e o cliente
            url = reverse('reservar_listar_hoteis')
            return redirect(f"{url}?cliente_id={cliente_id}&checkin={checkin}&checkout={checkout}")
        else:
            erro = "Preencha todas as datas."
            return render(request, 'ReserVou/selecionar_datas.html', {'erro': erro, 'cliente_id': request.GET.get('cliente_id')})
    return render(request, 'ReserVou/selecionar_datas.html', {'cliente_id': request.GET.get('cliente_id')})


#-----------------Codgo antigo (FBV)----------------
def reservar_listar_hoteis(request):
    cliente_id = request.GET.get('cliente_id')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    hoteis = Hotel.objects.all()
    context = {
        'hoteis': hoteis,
        'cliente_id': cliente_id,
        'checkin': checkin,
        'checkout': checkout,
    }
    return render(request, 'ReserVou/hotel/reservar_listar_hoteis.html', context)


#-----------------Codgo antigo (FBV)----------------
def listar_quartos(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    cliente_id = request.GET.get('cliente_id')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    quartos_disponiveis = []

    if checkin and checkout and checkin != 'None' and checkout != 'None':
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()

        # Corrigido: só exclui quartos com reservas ativas que conflitam com o período
        quartos_disponiveis = Quarto.objects.filter(hotel=hotel).exclude(
            reservas__status='ativa',
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


#-----------------Codgo antigo (FBV)----------------
def fazer_reserva(request, quarto_id):
    cliente_id = request.GET.get('cliente_id')
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

    return render(request, 'ReserVou/fazer_reserva.html', context)


#-----------------Codgo antigo (FBV)----------------
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

        
        reserva = Reserva.objects.create(
            cliente=cliente,
            hotel=hotel,
            quarto=quarto,
            check_in=data_in,
            check_out=data_out
        )
        quarto.status = 'reservado'
        quarto.save()
        from .models import Pagamento
        
        metodo = tipo_pagamento.lower() if tipo_pagamento else 'pix'
        if metodo not in ['pix', 'boleto', 'credito', 'debito']:
            metodo = 'pix'
        Pagamento.objects.create(
            reserva=reserva,
            valor=total,
            metodo=metodo,
            status='pago'
        )

        
        return render(request, 'ReserVou/confirmacao_pagamento.html', {
            'reserva': reserva,
            'tipo_pagamento': tipo_pagamento,
            'total': total,
        })
    else:
        
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

        from .models import Pagamento
        context = {
            'cliente': cliente,
            'hotel': hotel,
            'quarto': quarto,
            'checkin': checkin,
            'checkout': checkout,
            'total': total,
            'metodos_pagamento': Pagamento.METODO_ESCOLHIDO,
        }

        return render(request, 'ReserVou/fazer_pagamento.html', context)


#-----------------Codgo antigo (FBV)----------------
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        if nome and email and telefone:
            cliente.nome = nome
            cliente.email = email
            cliente.telefone = telefone
            cliente.save()
            return redirect('perfil_cliente', id=cliente.id)
        else:
            erro = "Todos os campos são obrigatórios."
            return render(request, 'ReserVou/cliente/editar_cliente.html', {'cliente': cliente, 'erro': erro})
    return render(request, 'ReserVou/cliente/editar_cliente.html', {'cliente': cliente})


#-----------------Codgo antigo (FBV)----------------
def deletar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('home')
    return render(request, 'ReserVou/cliente/confirmar_deletar_cliente.html', {'cliente': cliente})


#-----------------Codgo antigo (FBV)----------------
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.status = 'cancelada'
        reserva.save()
        quarto = reserva.quarto
        quarto.status = 'disponível'
        quarto.save()
        
        if hasattr(reserva, 'pagamento'):
            pagamento = reserva.pagamento
            pagamento.status = 'cancelado'
            pagamento.save()
        return redirect('perfil_cliente', id=reserva.cliente.id)
    return render(request, 'ReserVou/cliente/confirmar_cancelar_reserva.html', {'reserva': reserva})