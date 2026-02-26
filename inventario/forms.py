from django import forms
from django.contrib.auth.forms import UserCreationForm
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
            'password2',
        ]
