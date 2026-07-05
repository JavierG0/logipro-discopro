from django import forms
from django.contrib.auth.models import User

from .models import Departamento, Usuario


class UsuarioSistemaForm(forms.ModelForm):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo', required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Obligatoria al crear. Al editar, déjela vacía para no cambiar.',
    )
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Usuario
        fields = ['rut', 'telefono', 'rol', 'departamento', 'estado']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario_instance = kwargs.pop('usuario_instance', None)
        super().__init__(*args, **kwargs)
        self.fields['rol'].choices = list(Usuario.ROLES)
        if self.usuario_instance:
            user = self.usuario_instance.user
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['password'].required = False

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('password_confirm')
        if not self.usuario_instance and not password:
            self.add_error('password', 'La contraseña es obligatoria al crear un usuario.')
        if password and password != confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')
        username = cleaned.get('username')
        if username:
            qs = User.objects.filter(username=username)
            if self.usuario_instance:
                qs = qs.exclude(pk=self.usuario_instance.user_id)
            if qs.exists():
                self.add_error('username', 'Este nombre de usuario ya existe.')
        rut = cleaned.get('rut')
        if rut:
            qs = Usuario.objects.filter(rut=rut)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('rut', 'Este RUT ya está registrado.')
        return cleaned

    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        if self.usuario_instance:
            user = self.usuario_instance.user
        else:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=password,
                email=self.cleaned_data.get('email') or '',
                first_name=self.cleaned_data.get('first_name', ''),
                last_name=self.cleaned_data.get('last_name', ''),
            )
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email') or ''
        user.is_active = self.cleaned_data.get('estado', True)
        if password:
            user.set_password(password)
        user.save()

        perfil = self.instance if self.instance.pk else Usuario(user=user)
        perfil.rut = self.cleaned_data['rut']
        perfil.telefono = self.cleaned_data.get('telefono', '')
        perfil.rol = self.cleaned_data['rol']
        perfil.departamento = self.cleaned_data.get('departamento')
        perfil.estado = self.cleaned_data.get('estado', True)
        if commit:
            perfil.save()
        return perfil
