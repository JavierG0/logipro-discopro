from django import forms
from .models import Motorista, Moto, Sucursal
from apps.usuarios.models import Usuario


class SucursalForm(forms.ModelForm):
    """Formulario para crear/editar sucursales"""
    class Meta:
        model = Sucursal
        fields = ['nombre', 'ciudad', 'direccion', 'telefono', 'encargado', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la sucursal'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'encargado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class MotoForm(forms.ModelForm):
    """Formulario para crear/editar motos"""
    class Meta:
        model = Moto
        fields = ['placa', 'marca', 'modelo', 'año', 'color', 'sucursal', 'estado', 'activo']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Placa del vehículo'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo'
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Año'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
            'sucursal': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if placa:
            if self.instance.pk:
                if Moto.objects.filter(placa=placa).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Esta placa ya está registrada.')
            else:
                if Moto.objects.filter(placa=placa).exists():
                    raise forms.ValidationError('Esta placa ya está registrada.')
        return placa


class MotoristaForm(forms.ModelForm):
    """Formulario para editar motoristas"""
    class Meta:
        model = Motorista
        fields = [
            'usuario', 'licencia', 'tipo_licencia', 'vigencia_licencia',
            'estado', 'ubicacion_actual', 'latitud', 'longitud', 'activo'
        ]
        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccionar usuario'
            }),
            'licencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de licencia'
            }),
            'tipo_licencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de licencia'
            }),
            'vigencia_licencia': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ubicacion_actual': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación actual'
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Latitud'
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Longitud'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_licencia(self):
        licencia = self.cleaned_data.get('licencia')
        if licencia:
            # Verificar que no exista otra licencia igual
            if self.instance.pk:
                if Motorista.objects.filter(licencia=licencia).exclude(pk=self.instance.pk).exists():
                    raise forms.ValidationError('Esta licencia ya está registrada.')
            else:
                if Motorista.objects.filter(licencia=licencia).exists():
                    raise forms.ValidationError('Esta licencia ya está registrada.')
        return licencia


class MotoristaCreateForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    )
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    rut = forms.CharField(
        label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'RUT'
        })
    )
    telefono = forms.CharField(
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono'
        })
    )

    class Meta:
        model = Motorista
        fields = [
            'licencia', 'tipo_licencia', 'vigencia_licencia',
            'estado', 'ubicacion_actual', 'latitud', 'longitud', 'activo'
        ]
        widgets = {
            'licencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de licencia'
            }),
            'tipo_licencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de licencia'
            }),
            'vigencia_licencia': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ubicacion_actual': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación actual'
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Latitud'
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Longitud'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')

        return cleaned_data

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        from apps.usuarios.models import Usuario
        if rut and Usuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este RUT ya está registrado.')
        return rut

    def clean_username(self):
        username = self.cleaned_data.get('username')
        from django.contrib.auth.models import User
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe.')
        return username

    def save(self, commit=True):
        from django.contrib.auth.models import User
        from apps.usuarios.models import Usuario

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data.get('email') or '',
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', ''),
        )

        usuario = Usuario.objects.create(
            user=user,
            rut=self.cleaned_data['rut'],
            telefono=self.cleaned_data.get('telefono', ''),
            rol='motorista',
            estado=True
        )

        motorista = super().save(commit=False)
        motorista.usuario = usuario
        if commit:
            motorista.save()
        return motorista
