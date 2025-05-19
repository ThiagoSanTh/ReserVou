from django import forms
from .models import Quarto

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
