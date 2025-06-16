from django import forms
from django.contrib.auth.models import User
from .models import Quarto, Cliente, Hotel

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
    usuario = forms.CharField(label='Usuário', max_length=150)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    email = forms.EmailField(label='E-mail')
    telefone = forms.CharField(label='Telefone', max_length=15, required=False)

    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone']

    def save(self, commit=True):
        usuario = User.objects.create_user(
            usuario = self.cleaned_data['usuario'],
            senha = self.cleaned_data['senha'],
            email = self.cleaned_data['email'],
            telefone = self.cleaned_data['telefone']
        )
        cliente = super().save(commit=False)
        cliente.usuario = usuario
        if commit:
            cliente.save()
        return cliente



class HotelUserForm(forms.ModelForm):
    usuario = forms.CharField(label='Usuário')
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    endereco = forms.CharField(label='Endereço', max_length=255)

    class Meta:
        model = Hotel
        fields = ['endereco']

    def save(self, commit=True):
        usuario = User.objects.create_user(
            usuario=self.cleaned_data['usuario'],
            password=self.cleaned_data['senha'],
            endereco=self.cleaned_data['endereço']
        )
        hotel = super().save(commit=False)
        hotel.nome = usuario
        if commit:
            hotel.save()
        return hotel