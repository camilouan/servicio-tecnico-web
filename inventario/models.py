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
        "Celulares": "https://picsum.photos/seed/celulares/1200/800",
        "Accesorios": "https://picsum.photos/seed/accesorios/1200/800",
        "Consolas": "https://picsum.photos/seed/consolas/1200/800",
        "Computadores": "https://picsum.photos/seed/computadores/1200/800",
    }

    @property
    def imagen_url(self):
        if self.imagen and getattr(self.imagen, 'url', None):
            return self.imagen.url
        return self.FALLBACK_IMAGES.get(self.nombre, "https://picsum.photos/seed/default/1200/800")

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
        "iPhone 14": "https://picsum.photos/seed/iphone14/1200/800",
        "Samsung Galaxy S23": "https://picsum.photos/seed/samsung-s23/1200/800",
        "Xiaomi Redmi Note 12": "https://picsum.photos/seed/xiaomi-redmi/1200/800",
        "Motorola Edge 40": "https://picsum.photos/seed/motorola-edge/1200/800",
        "Audífonos Bluetooth": "https://picsum.photos/seed/audifonos-bluetooth/1200/800",
        "Teclado Mecanico RGB": "https://picsum.photos/seed/teclado-rgb/1200/800",
        "Mouse Gamer": "https://picsum.photos/seed/mouse-gamer/1200/800",
        "Cargador Rapido": "https://picsum.photos/seed/cargador-rapido/1200/800",
        "PlayStation 5": "https://picsum.photos/seed/ps5/1200/800",
        "Xbox Series X": "https://picsum.photos/seed/xbox-series-x/1200/800",
        "Nintendo Switch": "https://picsum.photos/seed/nintendo-switch/1200/800",
        "Laptop HP": "https://picsum.photos/seed/hp-laptop/1200/800",
        "MacBook Air": "https://picsum.photos/seed/macbook-air/1200/800",
        "Asus ROG": "https://picsum.photos/seed/asus-rog/1200/800",
        "Monitor Gamer": "https://picsum.photos/seed/monitor-gamer/1200/800",
        "Tablet Samsung": "https://picsum.photos/seed/tablet-samsung/1200/800",
        "Smartwatch": "https://picsum.photos/seed/smartwatch/1200/800",
        "Parlante JBL": "https://picsum.photos/seed/parlante-jbl/1200/800",
        "Camara Web": "https://picsum.photos/seed/camara-web/1200/800",
        "Control PS5": "https://picsum.photos/seed/control-ps5/1200/800",
    }

    @property
    def imagen_url(self):
        if self.imagen and getattr(self.imagen, 'url', None):
            return self.imagen.url
        return self.FALLBACK_IMAGES.get(self.nombre, "https://picsum.photos/seed/default/1200/800")

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