from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Hotel, Quarto, Cliente, Reserva, Pagamento

# Create your views here.
def pagina_inicial(request):
    clientes = Cliente.objects.all()
    return render(request, 'ReserVou/pagina_inicial.html', {'clientes': clientes})

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
            return render(request, 'ReserVou/cadastrar_cliente.html', {'erro': erro})

    return render(request, 'ReserVou/cadastrar_cliente.html')
            
def perfil_cliente(request, id):
    cliente = Cliente.objects.get(id = id)
    reservas = Reserva.objects.filter(cliente = cliente).select_related('quarto', 'hotel')
    
    return render(request, 'ReserVou/perfil_cliente.html', {
        'cliente': cliente,
        'reservas': reservas,
    })
    
def listar_hoteis(request):
    cliente_id = request.GET.get('cliente_id')
    hoteis = Hotel.objects.all()
    
    return render(request, 'ReserVou/listar_hoteis.html', {
        'hoteis' : hoteis,
        'cliente_id' : cliente_id
    })