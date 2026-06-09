from django import forms
from .models import Movimiento
from apps.motoristas.models import Sucursal


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['despacho_numero', 'motorista', 'sucursal', 'tipo', 'estado', 'observaciones']
        widgets = {
            'despacho_numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de despacho'
            }),
            'motorista': forms.Select(attrs={
                'class': 'form-control'
            }),
            'sucursal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales',
                'rows': 4
            }),
        }

    def clean_despacho_numero(self):
        despacho_numero = self.cleaned_data.get('despacho_numero')
        if despacho_numero:
            # Verificar que el número sea único
            if self.instance.pk:
                if Movimiento.objects.filter(despacho_numero=despacho_numero).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Este número de despacho ya existe.')
            else:
                if Movimiento.objects.filter(despacho_numero=despacho_numero).exists():
                    raise forms.ValidationError('Este número de despacho ya existe.')
        return despacho_numero

    def clean(self):
        cleaned_data = super().clean()
        motorista = cleaned_data.get('motorista')
        
        # Validar que el motorista esté disponible
        if motorista and motorista.estado == 'inactivo':
            raise forms.ValidationError('No se puede asignar un movimiento a un motorista inactivo.')
        
        return cleaned_data


class ActualizarEstadoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['estado', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones sobre el cambio de estado',
                'rows': 3
            }),
        }


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'ciudad', 'telefono', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la sucursal'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono',
                'type': 'tel'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
