from django import forms
from .models import Reporte
from django.utils import timezone


class GenerarReporteForm(forms.ModelForm):
    periodo_desde = forms.DateField(
        label='Fecha desde',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    periodo_hasta = forms.DateField(
        label='Fecha hasta',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Reporte
        fields = ['titulo', 'tipo', 'periodo_desde', 'periodo_hasta']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del reporte'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        periodo_desde = cleaned_data.get('periodo_desde')
        periodo_hasta = cleaned_data.get('periodo_hasta')

        if periodo_desde and periodo_hasta:
            if periodo_desde > periodo_hasta:
                raise forms.ValidationError('La fecha "desde" no puede ser mayor a la fecha "hasta".')
            
            # Validar que no sea una fecha futura
            if periodo_hasta > timezone.now().date():
                raise forms.ValidationError('La fecha "hasta" no puede ser una fecha futura.')

        return cleaned_data


class FiltroReporteForm(forms.Form):
    TIPO_CHOICES = [
        ('', '-- Todos los tipos --'),
        ('movimientos', 'Movimientos'),
        ('motoristas', 'Motoristas'),
        ('general', 'General'),
    ]
    
    tipo = forms.ChoiceField(
        label='Tipo de reporte',
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    fecha_desde = forms.DateField(
        label='Desde',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        label='Hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    ordenar_por = forms.ChoiceField(
        label='Ordenar por',
        choices=[
            ('-fecha_generacion', 'Más recientes'),
            ('fecha_generacion', 'Más antiguos'),
            ('titulo', 'Título (A-Z)'),
            ('-titulo', 'Título (Z-A)'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_desde = cleaned_data.get('fecha_desde')
        fecha_hasta = cleaned_data.get('fecha_hasta')

        if fecha_desde and fecha_hasta:
            if fecha_desde > fecha_hasta:
                raise forms.ValidationError('La fecha "desde" no puede ser mayor a la fecha "hasta".')

        return cleaned_data
