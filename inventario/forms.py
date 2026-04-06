from datetime import timedelta

from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils import timezone

from .models import Usuario


class RegistroForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'nombres',
            'apellidos',
            'telefono',
            'documento_identidad',
            'direccion',
            'ciudad',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['foto_perfil', 'nombres', 'apellidos', 'email', 'telefono', 'direccion', 'ciudad']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CambioPasswordSemanalForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super().clean()
        ultima_actualizacion = getattr(self.user, 'ultima_actualizacion_password', None)

        if ultima_actualizacion:
            proximo_cambio = ultima_actualizacion + timedelta(days=7)
            if timezone.now() < proximo_cambio:
                raise forms.ValidationError(
                    f'Solo puedes cambiar tu contraseña una vez por semana. Inténtalo nuevamente después del {proximo_cambio.strftime("%d/%m/%Y %H:%M")}.',
                )

        return cleaned_data


class EliminarCuentaForm(forms.Form):
    password_actual = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirmar = forms.BooleanField(
        label='Entiendo que mi cuenta y mis apartados se eliminarán del sistema.',
        required=True,
    )