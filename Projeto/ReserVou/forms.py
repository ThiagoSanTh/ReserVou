from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Quarto, Cliente

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'tipo', 'preco_diaria', 'status']
        widgets = {
            'preco_diaria': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Digite o valor da diária',
            }),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite seu email'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Digite seu telefone'}),
        }