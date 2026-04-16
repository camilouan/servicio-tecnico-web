import random

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
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
    foto_perfil = CloudinaryField('foto de perfil', blank=True, null=True)

    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion_password = models.DateTimeField(blank=True, null=True)

    activo = models.BooleanField(default=True)
    acepta_politicas = models.BooleanField(default=False)
    fecha_aceptacion_politicas = models.DateTimeField(blank=True, null=True)

    @property
    def foto_perfil_url(self):
        if self.foto_perfil:
            try:
                url = getattr(self.foto_perfil, 'url', None)
                if url:
                    return url
            except Exception:
                pass
        return None

    def __str__(self):
        return self.username


class Categoria(models.Model):

    nombre = models.CharField(max_length=100)

    descripcion = models.TextField()

    imagen = CloudinaryField('imagen', blank=True, null=True)

    activa = models.BooleanField(default=True)

    FALLBACK_IMAGES = {
        "Celulares": "https://commons.wikimedia.org/wiki/Special:FilePath/Mobile_Phone_Evolution_1992_-_2014.jpg",
        "Accesorios": "https://commons.wikimedia.org/wiki/Special:FilePath/SanDisk-Cruzer-USB-4GB-ThumbDrive.jpg",
        "Consolas": "https://commons.wikimedia.org/wiki/Special:FilePath/Gaming_Section_1_-_Retrosystems_2010.jpg",
        "Computadores": "https://commons.wikimedia.org/wiki/Special:FilePath/Laptop_collage.jpg",
    }

    @property
    def imagen_url(self):
        if self.imagen:
            try:
                url = getattr(self.imagen, 'url', None)
                if url:
                    return url
            except Exception:
                pass
        return f"inventario/images/categoria-{slugify(self.nombre)}.svg"

    @property
    def imagen_is_absolute(self):
        if self.imagen:
            try:
                return bool(getattr(self.imagen, 'url', None))
            except Exception:
                return False
        return False

    def clean(self):
        errors = {}
        
        # Validar que el precio no sea negativo
        if self.precio < 0:
            errors['precio'] = 'El precio no puede ser negativo.'
        
        # Validar que el stock total no sea negativo
        if self.stock_total < 0:
            errors['stock_total'] = 'El stock total no puede ser negativo.'
        
        # Validar que el stock disponible no sea negativo
        if self.stock_disponible < 0:
            errors['stock_disponible'] = 'El stock disponible no puede ser negativo.'
        
        # Validar que el stock disponible no sea mayor al stock total
        if self.stock_disponible > self.stock_total:
            errors['stock_disponible'] = 'El stock disponible no puede ser mayor al stock total.'
        
        if errors:
            from django.core.exceptions import ValidationError
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta validaciones antes de guardar
        super().save(*args, **kwargs)



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

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    activo = models.BooleanField(default=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    FALLBACK_IMAGES = {
        "iPhone 14": "https://commons.wikimedia.org/wiki/Special:FilePath/IPhone_14_vector.svg",
        "Samsung Galaxy S23": "https://commons.wikimedia.org/wiki/Special:FilePath/Galaxy_S23.png",
        "Xiaomi Redmi Note 12": "https://commons.wikimedia.org/wiki/Special:FilePath/Redmi_Note_12_front.jpg",
        "Motorola Edge 40": "https://commons.wikimedia.org/wiki/Special:FilePath/Motorola_Edge.png",
        "Audífonos Bluetooth": "https://commons.wikimedia.org/wiki/Special:FilePath/Plantronics_headset.jpg",
        "Teclado Mecanico RGB": "https://commons.wikimedia.org/wiki/Special:FilePath/Keyboard_Construction.JPG",
        "Mouse Gamer": "https://commons.wikimedia.org/wiki/Special:FilePath/3-Tasten-Maus_Microsoft.jpg",
        "Cargador Rapido": "https://commons.wikimedia.org/wiki/Special:FilePath/Notebook-Computer-AC-Adapter.jpg",
        "PlayStation 5": "https://commons.wikimedia.org/wiki/Special:FilePath/Black_and_white_Playstation_5_base_edition_with_controller.png",
        "Xbox Series X": "https://commons.wikimedia.org/wiki/Special:FilePath/Xbox_Series_X_S_color.svg",
        "Nintendo Switch": "https://commons.wikimedia.org/wiki/Special:FilePath/Nintendo_Switch_2_in_Handheld_Mode.jpg",
        "Laptop HP": "https://commons.wikimedia.org/wiki/Special:FilePath/Laptop_collage.jpg",
        "MacBook Air": "https://commons.wikimedia.org/wiki/Special:FilePath/Macbook_Air_15_inch_-_2_(blurred).jpg",
        "Asus ROG": "https://commons.wikimedia.org/wiki/Special:FilePath/ROG_ALLY_-_11.jpg",
        "Monitor Gamer": "https://commons.wikimedia.org/wiki/Special:FilePath/MonitorLCDlcd.svg",
        "Tablet Samsung": "https://commons.wikimedia.org/wiki/Special:FilePath/IPad_Mini_6_-_1.jpg",
        "Smartwatch": "https://commons.wikimedia.org/wiki/Special:FilePath/Samsung_Galaxy_Watch.jpg",
        "Parlante JBL": "https://commons.wikimedia.org/wiki/Special:FilePath/JBL_Paragon_(edited_and_cropped).jpg",
        "Camara Web": "https://commons.wikimedia.org/wiki/Special:FilePath/Logicool_StreamCam_(cropped).jpg",
        "Control PS5": "https://commons.wikimedia.org/wiki/Special:FilePath/PS4-Console-wDS4.jpg",
    }

    @property
    def imagen_url(self):
        if self.imagen:
            try:
                url = getattr(self.imagen, 'url', None)
                if url:
                    return url
            except Exception:
                pass
        return f"inventario/images/producto-{slugify(self.nombre)}.svg"

    @property
    def imagen_is_absolute(self):
        if self.imagen:
            try:
                return bool(getattr(self.imagen, 'url', None))
            except Exception:
                return False
        return False

    def clean(self):
        errors = {}
        
        # Validar que el precio no sea negativo
        if self.precio < 0:
            errors['precio'] = 'El precio no puede ser negativo.'
        
        # Validar que el stock total no sea negativo
        if self.stock_total < 0:
            errors['stock_total'] = 'El stock total no puede ser negativo.'
        
        # Validar que el stock disponible no sea negativo
        if self.stock_disponible < 0:
            errors['stock_disponible'] = 'El stock disponible no puede ser negativo.'
        
        # Validar que el stock disponible no sea mayor al stock total
        if self.stock_disponible > self.stock_total:
            errors['stock_disponible'] = 'El stock disponible no puede ser mayor al stock total.'
        
        if errors:
            from django.core.exceptions import ValidationError
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecuta validaciones antes de guardar
        super().save(*args, **kwargs)



    def __str__(self):
        return self.nombre


class HeroBanner(models.Model):
    titulo = models.CharField(
        max_length=255,
        default='Encuentra accesorios y dispositivos con la mejor experiencia de compra'
    )
    subtitulo = models.TextField(
        default='Accesorios gamer, celulares, consolas y computadores listos para apartar con atención presencial y soporte profesional.'
    )
    imagen_fondo = CloudinaryField('imagen de fondo', blank=True, null=True)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Banner de Hero'
        verbose_name_plural = 'Banners de Hero'
        ordering = ['-orden', '-fecha_actualizacion']

    @property
    def fondo_url(self):
        if self.imagen_fondo:
            try:
                url = getattr(self.imagen_fondo, 'url', None)
                if url:
                    return url
            except Exception:
                pass
        return None

    def __str__(self):
        return f'Banner Hero {self.titulo[:40]}'


class Apartado(models.Model):

    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('expirado', 'Expirado'),
        ('entregado', 'Entregado'),
    )
    ESTADOS_CON_STOCK_OCUPADO = {'pendiente', 'confirmado', 'entregado'}

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    cantidad = models.IntegerField()

    codigo_verificacion = models.CharField(max_length=6, unique=True, blank=True, null=True)

    fecha_apartado = models.DateTimeField(auto_now_add=True)

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

    @classmethod
    def actualizar_apartados_vencidos(cls):
        vencidos = cls.objects.filter(
            estado='pendiente',
            fecha_expiracion__lt=timezone.now(),
        )

        total_actualizados = 0
        for apartado in vencidos:
            apartado.estado = 'expirado'
            if not apartado.motivo_cancelacion:
                apartado.motivo_cancelacion = 'Apartado expirado automáticamente por superar el tiempo límite.'
            apartado.save(update_fields=['estado', 'motivo_cancelacion'])
            total_actualizados += 1

        return total_actualizados

    def generar_codigo_verificacion(self):
        while True:
            codigo = f"{random.randint(0, 999999):06d}"
            if not Apartado.objects.filter(codigo_verificacion=codigo).exclude(pk=self.pk).exists():
                return codigo

    def _cantidad_reservada_para_estado(self, estado, cantidad=None):
        cantidad = self.cantidad if cantidad is None else cantidad
        return cantidad if estado in self.ESTADOS_CON_STOCK_OCUPADO else 0

    def _ajustar_stock_producto(self, producto_id, delta_consumo):
        if delta_consumo == 0:
            return

        producto = Producto.objects.select_for_update().get(pk=producto_id)

        if delta_consumo > 0 and producto.stock_disponible < delta_consumo:
            raise ValidationError(f'No hay suficiente stock disponible para {producto.nombre}.')

        producto.stock_disponible -= delta_consumo
        producto.save(update_fields=['stock_disponible'])

    def save(self, *args, **kwargs):
        if not self.codigo_verificacion:
            self.codigo_verificacion = self.generar_codigo_verificacion()

        previo = None
        if self.pk:
            previo = Apartado.objects.filter(pk=self.pk).first()

        # Lógica para confirmación automática
        if previo and previo.estado != 'confirmado' and self.estado == 'confirmado':
            self.fecha_confirmacion = timezone.now()
            # El confirmado_por se establecerá desde el admin
        elif self.estado != 'confirmado':
            # Si ya no está confirmado, limpiar los campos de confirmación
            self.fecha_confirmacion = None
            self.confirmado_por = None

        with transaction.atomic():
            if previo is None:
                consumo_nuevo = self._cantidad_reservada_para_estado(self.estado)
                self._ajustar_stock_producto(self.producto_id, consumo_nuevo)
            else:
                consumo_anterior = self._cantidad_reservada_para_estado(previo.estado, previo.cantidad)
                consumo_actual = self._cantidad_reservada_para_estado(self.estado, self.cantidad)

                if previo.producto_id == self.producto_id:
                    self._ajustar_stock_producto(self.producto_id, consumo_actual - consumo_anterior)
                else:
                    self._ajustar_stock_producto(previo.producto_id, -consumo_anterior)
                    self._ajustar_stock_producto(self.producto_id, consumo_actual)

            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"