from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.http import HttpResponseForbidden

from .models import Hotel, Quarto, Cliente, Reserva, Gerente
from .forms import QuartoForm, ClienteForm, CustomAuthForm
from datetime import datetime



#----------------Interface--------------------#
class paginaInicial(ListView):
    model = Hotel
    template_name = 'ReserVou/interface/pagina_inicial.html'
    context_object_name = 'hoteis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        return context

class selecionarDatas(View):
    template_name = 'ReserVou/interface/selecionar_datas.html'

    def get(self, request):
        cliente_id = request.GET.get('cliente_id')
        return render(request, self.template_name, {'cliente_id': cliente_id})
    
    def post(self, request):
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        cliente_id = request.POST.get('cliente_id')

        if checkin and checkout and cliente_id:
            url = reverse('reservar_listar_hoteis')
            return redirect(f"{url}?cliente_id={cliente_id}&checkin={checkin}&checkout={checkout}")
        else:
            erro = "Preencha todas as datas."
            return render(request, self.template_name, {'erro': erro, 'cliente_id': cliente_id})

class reservarListarHoteis(ListView):
    model = Hotel
    template_name = 'ReserVou/hotel/reservar_listar_hoteis.html'
    context_object_name = 'hoteis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cliente_id': self.request.GET.get('cliente_id'),
            'checkin': self.request.GET.get('checkin'),
            'checkout': self.request.GET.get('checkout'),
        })
        return context
    
class listarQuartos(ListView):
    template_name = 'ReserVou/hotel/listar_quartos.html'

    def get(self, request, pk):
        hotel = get_object_or_404(Hotel, id=pk)
        cliente_id = request.GET.get('cliente_id')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')

        quartos_disponiveis = []
        if checkin and checkout and checkin != 'None' and checkout != 'None':
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
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
        return render(request, self.template_name, context)              
        
class fazerReserva(View):
    template_name = 'ReserVou/interface/fazer_reserva.html'

    def get(self, request, quarto_id):
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

        return render(request, self.template_name, context)
    
class fazerPagamento(View):
    template_name = 'ReserVou/interface/fazer_pagamento.html'

    def get(self, request):
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

        return render(request, self.template_name, context)
    
    def post(self, request):
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

        return render(request, 'ReserVou/interface/confirmacao_pagamento.html', {
            'reserva': reserva,
            'tipo_pagamento': tipo_pagamento,
            'total': total,
        })

class cancelarReserva(View):
    template_name = 'ReserVou/cliente/confirmar_cancelar_reserva.html'

    def get(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)
        return render(request, self.template_name, {'reserva': reserva})

    def post(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)
        reserva.status = 'cancelada'
        reserva.save()

        quarto = reserva.quarto
        quarto.status = 'disponível'
        quarto.save()
        
        if hasattr(reserva, 'pagamento'):
            pagamento = reserva.pagamento
            pagamento.status = 'cancelado'
            pagamento.save()
        
        return redirect('perfil_cliente', reserva.cliente.id)


#----------------Gerente------------------#
class cadastrarGerente(FormView):
    form_class = UserCreationForm
    template_name = 'ReserVou/gerente/cadastrar_gerente.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        Gerente.objects.create(nome=user)
        return super().form_valid(form)
    
class editarGerente(UpdateView):
    model = Gerente
    form_class = CustomAuthForm
    template_name = 'ReserVou/gerente/editar_gerente.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        gerente = self.get_object()
        if not request.user.is_authenticated or not hasattr(request.user, 'gerente') or gerente != request.user.gerente:
            return HttpResponseForbidden('Você não tem permissão para editar este gerente.')
        return super().dispatch(request, *args, **kwargs)
    
class deletarGerente(DeleteView):
    model = Gerente
    template_name = 'ReserVou/gerente/confirmar_deletar_gerente.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        gerente = self.get_object()
        if not request.user.is_authenticated or not hasattr(request.user, 'gerente') or gerente != request.user.gerente:
            return HttpResponseForbidden('Você não tem permissão para deletar este gerente.')
        return super().dispatch(request, *args, **kwargs)


class loginGerente(LoginView):
    template_name = 'ReserVou/gerente/login_gerente.html'
    authentication_form = CustomAuthForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')
    
class logoutGerente(LogoutView):
    next_page = reverse_lazy('home')

class perfilGerente(DetailView):
    model = Gerente
    template_name = 'ReserVou/gerente/perfil_gerente.html'
    context_object_name = 'gerente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gerente = self.get_object()
        context['hoteis'] = Hotel.objects.filter(gerente=gerente).prefetch_related('quarto')
        return context

#----------------Hotel------------------#
class gerenciarHoteis(ListView):
    model = Hotel
    template_name = 'ReserVou/hotel/gerenciar_hoteis.html'
    context_object_name = 'hoteis'

    def get_queryset(self):
        return Hotel.objects.prefetch_related('quarto').all()

class cadastrarHotel(CreateView):
    model = Hotel
    fields = ['nome', 'endereco']
    template_name = 'ReserVou/hotel/cadastrar_hotel.html'
    success_url = reverse_lazy('gerenciar_hoteis')

    def form_valid(self, form):
        gerente = Gerente.objects.get(nome=self.request.user)
        form.instance.gerente = gerente
        return super().form_valid(form)
    

class editarHotel(UpdateView):
    model = Hotel
    fields = ['nome', 'endereco']
    template_name = 'ReserVou/hotel/editar_hotel.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        hotel = self.get_object()
        if not request.user.is_authenticated or not hasattr(request.user, 'gerente') or hotel.gerente != request.user.gerente:
            return HttpResponseForbidden('Você não tem permissão para editar este hotel.')
        return super().dispatch(request, *args, **kwargs)

class deletarHotel(DeleteView):
    model = Hotel
    template_name = 'ReserVou/hotel/confirmar_deletar_hotel.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        hotel = self.get_object()
        if not request.user.is_authenticated or not hasattr(request.user, 'gerente') or hotel.gerente != request.user.gerente:
            return HttpResponseForbidden('Você não tem permissão para deletar este hotel.')
        return super().dispatch(request, *args, **kwargs)


#----------------Quarto------------------#
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

class editarQuarto(UpdateView):
    model = Quarto
    fields = ['numero', 'tipo', 'preco_diaria', 'status']
    form_class = QuartoForm
    template_name = 'ReserVou/hotel/editar_quarto.html'
    success_url = reverse_lazy('gerenciar_hoteis')

    def get(self, request, pk):
        quarto = get_object_or_404(Quarto, id=pk)
        return render(request, self.template_name, {'quarto': quarto})
    
    def post(self, request, pk):
        quarto = get_object_or_404(Quarto, id=pk)
        form = self.form_class(request.POST, instance=quarto)
        
        if form.is_valid():
            form.save()
            return redirect('gerenciar_hoteis')
        else:
            return render(request, self.template_name, {'quarto': quarto, 'form': form})

class deletarQuarto(DeleteView):
    model = Quarto
    template_name = 'ReserVou/hotel/confirmar_deletar_quarto.html'
    success_url = reverse_lazy('gerenciar_hoteis')


#----------------Cliente------------------#
class cadastrarCliente(FormView):
    form_class = UserCreationForm
    template_name = 'ReserVou/cliente/cadastrar_cliente.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        email = self.request.POST.get('email')
        telefone = self.request.POST.get('telefone')
        user.email = email
        user.save()
        Cliente.objects.create(
            nome=user,
            email=email,
            telefone=telefone
        )
        return super().form_valid(form)
    
class loginCliente(LoginView):
    template_name = 'ReserVou/cliente/login_cliente.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')

class editarCliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'ReserVou/cliente/editar_cliente.html'
    success_url = reverse_lazy('home')

class deletarCliente(DeleteView):
    model = Cliente
    template_name = 'ReserVou/cliente/confirmar_deletar_cliente.html'
    success_url = reverse_lazy('home')

class perfilCliente(DetailView):
    model = Cliente
    template_name = 'ReserVou/cliente/perfil_cliente.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context['reservas'] = Reserva.objects.filter(cliente=cliente).select_related('quarto', 'hotel')
        return context
    
class logoutCliente(LogoutView):
    next_page = reverse_lazy('home')

