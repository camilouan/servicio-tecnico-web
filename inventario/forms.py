from datetime import timedelta

from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import Usuario


class RegistroForm(UserCreationForm):
    acepta_politicas = forms.BooleanField(
        required=True,
        label=mark_safe(
            'He leído y acepto la <a href="/politica-privacidad/" target="_blank" rel="noopener noreferrer">Política de Privacidad</a> y los <a href="/terminos-servicio/" target="_blank" rel="noopener noreferrer">Términos de Servicio</a>.'
        ),
        error_messages={
            'required': 'Debes aceptar la Política de Privacidad y los Términos de Servicio para crear tu cuenta.',
        },
    )

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
        self.order_fields([
            'username',
            'email',
            'nombres',
            'apellidos',
            'telefono',
            'documento_identidad',
            'direccion',
            'ciudad',
            'password1',
            'password2',
            'acepta_politicas',
        ])

        for name, field in self.fields.items():
            if field.widget.input_type == 'checkbox':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.acepta_politicas = True
        user.fecha_aceptacion_politicas = timezone.now()
        if commit:
            user.save()
        return user


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