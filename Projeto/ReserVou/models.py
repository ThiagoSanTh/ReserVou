from django.db import models
from django.contrib.auth.models import User
from django import forms

   
class Hotel (models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel', null=False, blank=False)
    endereco = models.CharField(max_length = 150, null = False, blank = False)
    
    @property
    def qtd_quartos_disponiveis(self):
        return self.quarto.filter(status='disponível').count()
    
    def __str__(self):
        return self.nome
    
class Quarto (models.Model):
    STATUS_ATUAL = [
        ('disponível', 'Disponível'),
        ('reservado', 'Reservado'),
    ]
    
    numero = models.CharField(max_length = 10, null = False, blank = False)
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE, related_name = 'quarto')
    tipo = models.CharField(max_length = 20, null = False, blank = False,  choices = [
        ('tradicional', 'Tradicional'),
        ('premium', 'Premium'),
        ('luxo', 'Luxo'),
        ])
    preco_diaria = models.DecimalField(max_digits = 8, decimal_places = 2, null = False, blank = False)
    status = models.CharField(max_length = 20, choices = STATUS_ATUAL, default = 'Disponível')    
    
    def __str__(self):
        return f"Quarto {self.numero} - {self.hotel.nome}"
    
class Cliente (models.Model):
    nome = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente', null=False, blank=False)
    email = models.EmailField(unique = True, max_length = 100, null = False, blank = False)
    telefone = models.CharField(max_length = 11, null = False, blank = False)
    
    def __str__(self):
        return self.nome        
    
class Reserva (models.Model):
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE, related_name = 'reservas')
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE, related_name = 'reservas')
    quarto = models.ForeignKey(Quarto, on_delete = models.CASCADE, related_name = 'reservas')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=[('ativa', 'Ativa'), ('cancelada', 'Cancelada')], default='ativa')
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.hotel.nome} - Quarto {self.quarto.numero} ({self.check_in} a {self.check_out})"
    
class Pagamento (models.Model):
    METODO_ESCOLHIDO = [
        ('pix', 'Pix'),
        ('boleto', 'Boleto'),
        ('credito', 'Cartão de Crédito'),
        ('debito', 'Cartão de Débito'),        
    ]
    
    reserva = models.OneToOneField(Reserva, on_delete = models.CASCADE, related_name = 'pagamento')
    valor = models.DecimalField(max_digits = 10, decimal_places = 2)
    metodo = models.CharField(max_length = 20, choices = METODO_ESCOLHIDO)
    status = models.CharField(max_length = 20, choices = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ], default = 'pendente')
    
    def __str__(self):
        return f"Pagamento da Reserva {self.reserva.id} - {self.status}"