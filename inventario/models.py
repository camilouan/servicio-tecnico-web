from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Usuario(AbstractUser):

    ROLES = (
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    )

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    documento_identidad = models.CharField(max_length=20)
    direccion = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)

    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    fecha_registro = models.DateTimeField(default=timezone.now)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Categoria(models.Model):

    nombre = models.CharField(max_length=100)

    descripcion = models.TextField()

    imagen = CloudinaryField('imagen', blank=True, null=True)

    activa = models.BooleanField(default=True)

    FALLBACK_IMAGES = {
        "Celulares": "https://source.unsplash.com/featured/?cellphone&auto=format&fit=crop&w=1200&q=80",
        "Accesorios": "https://source.unsplash.com/featured/?tech-accessories&auto=format&fit=crop&w=1200&q=80",
        "Consolas": "https://source.unsplash.com/featured/?gaming-console&auto=format&fit=crop&w=1200&q=80",
        "Computadores": "https://source.unsplash.com/featured/?computer&auto=format&fit=crop&w=1200&q=80",
    }

    @property
    def imagen_url(self):
        if self.imagen and getattr(self.imagen, 'url', None):
            return self.imagen.url
        return self.FALLBACK_IMAGES.get(self.nombre, "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80")

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    ESTADOS = (
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    )

    nombre = models.CharField(max_length=150)

    descripcion = models.TextField()

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    stock_total = models.IntegerField()

    stock_disponible = models.IntegerField()

    # 👇 Imagen almacenada en Cloudinary
    imagen = CloudinaryField('imagen', blank=True, null=True)

    fecha_creacion = models.DateTimeField(default=timezone.now)

    activo = models.BooleanField(default=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    FALLBACK_IMAGES = {
        "iPhone 14": "https://source.unsplash.com/featured/?iphone&auto=format&fit=crop&w=1200&q=80",
        "Samsung Galaxy S23": "https://source.unsplash.com/featured/?samsung-phone&auto=format&fit=crop&w=1200&q=80",
        "Xiaomi Redmi Note 12": "https://source.unsplash.com/featured/?xiaomi-phone&auto=format&fit=crop&w=1200&q=80",
        "Motorola Edge 40": "https://source.unsplash.com/featured/?motorola-phone&auto=format&fit=crop&w=1200&q=80",
        "Audifonos Bluetooth": "https://source.unsplash.com/featured/?bluetooth-headphones&auto=format&fit=crop&w=1200&q=80",
        "Teclado Mecanico RGB": "https://source.unsplash.com/featured/?mechanical-keyboard&auto=format&fit=crop&w=1200&q=80",
        "Mouse Gamer": "https://source.unsplash.com/featured/?gaming-mouse&auto=format&fit=crop&w=1200&q=80",
        "Cargador Rapido": "https://source.unsplash.com/featured/?phone-charger&auto=format&fit=crop&w=1200&q=80",
        "PlayStation 5": "https://source.unsplash.com/featured/?playstation-5&auto=format&fit=crop&w=1200&q=80",
        "Xbox Series X": "https://source.unsplash.com/featured/?xbox-series-x&auto=format&fit=crop&w=1200&q=80",
        "Nintendo Switch": "https://source.unsplash.com/featured/?nintendo-switch&auto=format&fit=crop&w=1200&q=80",
        "Laptop HP": "https://source.unsplash.com/featured/?hp-laptop&auto=format&fit=crop&w=1200&q=80",
        "MacBook Air": "https://source.unsplash.com/featured/?macbook-air&auto=format&fit=crop&w=1200&q=80",
        "Asus ROG": "https://source.unsplash.com/featured/?asus-rog-laptop&auto=format&fit=crop&w=1200&q=80",
        "Monitor Gamer": "https://source.unsplash.com/featured/?gaming-monitor&auto=format&fit=crop&w=1200&q=80",
        "Tablet Samsung": "https://source.unsplash.com/featured/?samsung-tablet&auto=format&fit=crop&w=1200&q=80",
        "Smartwatch": "https://source.unsplash.com/featured/?smartwatch&auto=format&fit=crop&w=1200&q=80",
        "Parlante JBL": "https://source.unsplash.com/featured/?jbl-speaker&auto=format&fit=crop&w=1200&q=80",
        "Camara Web": "https://source.unsplash.com/featured/?webcam&auto=format&fit=crop&w=1200&q=80",
        "Control PS5": "https://source.unsplash.com/featured/?ps5-controller&auto=format&fit=crop&w=1200&q=80",
    }

    @property
    def imagen_url(self):
        if self.imagen and getattr(self.imagen, 'url', None):
            return self.imagen.url
        return self.FALLBACK_IMAGES.get(self.nombre, "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80")

    def __str__(self):
        return self.nombre


class Apartado(models.Model):

    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('expirado', 'Expirado'),
        ('entregado', 'Entregado'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    cantidad = models.IntegerField()

    fecha_apartado = models.DateTimeField(default=timezone.now)

    fecha_expiracion = models.DateTimeField()

    fecha_confirmacion = models.DateTimeField(blank=True, null=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    motivo_cancelacion = models.TextField(blank=True, null=True)

    confirmado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apartados_confirmados'
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"