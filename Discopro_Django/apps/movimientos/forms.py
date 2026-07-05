from django import forms
from .models import Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['numero_despacho', 'direccion_destino']
        widgets = {
            'numero_despacho': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código de despacho'
            }),
            'direccion_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección destino'
            }),
        }

    def clean_numero_despacho(self):
        numero_despacho = self.cleaned_data.get('numero_despacho')
        if numero_despacho:
            if self.instance.pk:
                if Movimiento.objects.filter(numero_despacho=numero_despacho).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Este número de despacho ya existe.')
            else:
                if Movimiento.objects.filter(numero_despacho=numero_despacho).exists():
                    raise forms.ValidationError('Este número de despacho ya existe.')
        return numero_despacho
