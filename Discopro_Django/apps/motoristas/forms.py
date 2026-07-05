from django import forms
from django.contrib.auth.models import User

from apps.usuarios.models import Usuario
from .geografia import GEOGRAFIA_CHILE, comunas, provincias, regiones
from .models import AsignacionOperativa, Motorista, Moto, Sucursal, sincronizar_asignacion


class GeografiaFormMixin:
    """Selects en cascada Región → Provincia → Comuna."""

    def _configurar_geografia(self, instance=None):
        region_val = self.data.get('region') or (instance.region if instance else '')
        provincia_val = self.data.get('provincia') or (instance.provincia if instance else '')

        self.fields['region'] = forms.ChoiceField(
            label='Región',
            choices=[('', 'Seleccione región...')] + [(r, r) for r in regiones()],
            required=True,
        )
        prov_choices = [(p, p) for p in provincias(region_val)] if region_val else []
        self.fields['provincia'] = forms.ChoiceField(
            label='Provincia',
            choices=[('', 'Seleccione provincia...')] + prov_choices,
            required=True,
        )
        com_choices = [(c, c) for c in comunas(region_val, provincia_val)] if region_val and provincia_val else []
        self.fields['comuna'] = forms.ChoiceField(
            label='Comuna',
            choices=[('', 'Seleccione comuna...')] + com_choices,
            required=True,
        )
        for name in ('region', 'provincia', 'comuna'):
            self.fields[name].widget.attrs.update({'class': 'form-control geografia-select', 'data-geografia': name})

        if instance:
            self.fields['region'].initial = instance.region
            self.fields['provincia'].initial = instance.provincia
            self.fields['comuna'].initial = instance.comuna

    def clean(self):
        cleaned = super().clean()
        region = cleaned.get('region')
        provincia = cleaned.get('provincia')
        comuna = cleaned.get('comuna')
        if region and provincia and provincia not in provincias(region):
            self.add_error('provincia', 'Provincia no válida para la región seleccionada.')
        if region and provincia and comuna and comuna not in comunas(region, provincia):
            self.add_error('comuna', 'Comuna no válida para la provincia seleccionada.')
        return cleaned


class SucursalForm(GeografiaFormMixin, forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'region', 'provincia', 'comuna', 'direccion', 'telefono', 'encargado_nombre', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la farmacia origen'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle y número (origen de despacho)'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'}),
            'encargado_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del encargado (solo referencia)'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configurar_geografia(self.instance if self.instance.pk else None)


class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        fields = ['placa', 'marca', 'modelo', 'año', 'color', 'estado', 'activo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa del vehículo'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa:
            qs = Moto.objects.filter(placa=placa)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Esta placa ya está registrada.')
        return placa


class MotoristaForm(GeografiaFormMixin, forms.ModelForm):
    moto = forms.ModelChoiceField(
        queryset=Moto.objects.filter(activo=True),
        required=False,
        label='Moto asignada',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    sucursal = forms.ModelChoiceField(
        queryset=Sucursal.objects.filter(activo=True),
        required=True,
        label='Farmacia origen asignada',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Motorista
        fields = [
            'licencia', 'tipo_licencia', 'vigencia_licencia',
            'region', 'provincia', 'comuna', 'direccion',
            'estado', 'activo',
        ]
        widgets = {
            'licencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de licencia'}),
            'tipo_licencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de licencia'}),
            'vigencia_licencia': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección particular del motorista'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configurar_geografia(self.instance if self.instance.pk else None)
        if self.instance.pk:
            asignacion = self.instance.asignaciones.filter(activa=True).first()
            if asignacion:
                self.fields['moto'].initial = asignacion.moto_id
                self.fields['sucursal'].initial = asignacion.sucursal_id

    def clean_licencia(self):
        licencia = self.cleaned_data.get('licencia')
        if licencia:
            qs = Motorista.objects.filter(licencia=licencia)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Esta licencia ya está registrada.')
        return licencia

    def save(self, commit=True):
        motorista = super().save(commit=commit)
        if commit:
            sincronizar_asignacion(
                motorista,
                self.cleaned_data.get('moto'),
                self.cleaned_data.get('sucursal'),
            )
        return motorista


class MotoristaCreateForm(MotoristaForm):
    """Crea perfil operativo vinculado a un usuario ya registrado (sin credenciales aquí)."""
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(rol='motorista', estado=True).select_related('user'),
        label='Usuario del sistema (motorista)',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='El acceso (usuario/contraseña) se gestiona en Administración de usuarios.',
    )

    class Meta(MotoristaForm.Meta):
        fields = MotoristaForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(
            rol='motorista', estado=True, motorista__isnull=True,
        ).select_related('user')

    def save(self, commit=True):
        if not commit:
            raise ValueError('MotoristaCreateForm requiere commit=True')
        usuario = self.cleaned_data['usuario']
        motorista = super(MotoristaForm, self).save(commit=False)
        motorista.usuario = usuario
        motorista.save()
        sincronizar_asignacion(
            motorista,
            self.cleaned_data.get('moto'),
            self.cleaned_data.get('sucursal'),
        )
        return motorista
