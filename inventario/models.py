from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Producto(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('no_disponible', 'No Disponible'),
    ]

    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Apartado(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('entregado', 'Entregado'),
        ('expirado', 'Expirado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_apartado = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def save(self, *args, **kwargs):
        if not self.fecha_expiracion:
            self.fecha_expiracion = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} - {self.usuario.username}"

