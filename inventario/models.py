import random

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.core.cache import cache


# Acá están los modelos principales del sistema y algunas reglas básicas del negocio.


def _fallback_image_path(prefix, name, fallback_map):
    # Si no hay imagen subida, intento devolver una ruta segura o una imagen por defecto.
    if name in fallback_map:
        return fallback_map[name]

    normalized_name = slugify(name)
    for key, value in fallback_map.items():
        if slugify(key) == normalized_name:
            return value

    return f"inventario/images/{prefix}-{normalized_name}.svg"


class Usuario(AbstractUser):

    ROLES = (
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    )

    # Campos extra que necesita el sistema además de los datos normales de Django.
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

    # Cada categoría agrupa productos y puede tener una imagen visible en el catálogo.
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
        return _fallback_image_path('categoria', self.nombre, self.FALLBACK_IMAGES)

    @property
    def imagen_is_absolute(self):
        if self.imagen:
            try:
                return bool(getattr(self.imagen, 'url', None))
            except Exception:
                return False
        return False

    def clean(self):
        # Valido antes de guardar para no dejar categorías vacías en la base.
        errors = {}

        if not self.nombre or not self.nombre.strip():
            errors['nombre'] = 'El nombre de la categoría es obligatorio.'

        if not self.descripcion or not self.descripcion.strip():
            errors['descripcion'] = 'La descripción de la categoría es obligatoria.'

        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        # Paso por full_clean() para que se apliquen las validaciones del modelo.
        self.full_clean()  # Ejecuta validaciones antes de guardar
        super().save(*args, **kwargs)



    def __str__(self):
        return self.nombre


class Producto(models.Model):

    # Producto que se muestra en el catálogo y que después se puede apartar.
    ESTADOS = (
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    )

    nombre = models.CharField(max_length=150)

    descripcion = models.TextField()

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    stock_total = models.IntegerField()

    stock_disponible = models.IntegerField()

    #  Imagen almacenada en Cloudinary
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
        return _fallback_image_path('producto', self.nombre, self.FALLBACK_IMAGES)

    @property
    def imagen_is_absolute(self):
        if self.imagen:
            try:
                return bool(getattr(self.imagen, 'url', None))
            except Exception:
                return False
        return False

    def clean(self):
        # Acá reviso que los números de stock tengan sentido antes de guardar.
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
        # Igual que en categoría, guardo solo si los datos pasan las validaciones.
        self.full_clean()  # Ejecuta validaciones antes de guardar
        super().save(*args, **kwargs)



    def __str__(self):
        return self.nombre


class HeroBanner(models.Model):
    # Banner principal que aparece en la portada.
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

    # Un apartado es la reserva de un producto por parte de un usuario.
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

    class Meta:
        indexes = [
            models.Index(fields=['estado', 'fecha_expiracion']),
            models.Index(fields=['estado', 'fecha_apartado']),
            models.Index(fields=['usuario', 'fecha_apartado']),
        ]

    @classmethod
    def actualizar_apartados_vencidos(cls):
        # Aquí se liberan los apartados vencidos y se devuelve el stock al producto.
        motivo_expirado = 'Apartado expirado automáticamente por superar el tiempo límite.'

        with transaction.atomic():
            vencidos = (
                cls.objects.select_for_update()
                .filter(
                    estado='pendiente',
                    fecha_expiracion__lt=timezone.now(),
                )
            )

            total_actualizados = vencidos.count()
            if total_actualizados == 0:
                return 0

            cantidades_por_producto = vencidos.values('producto_id').annotate(
                total=models.Sum('cantidad')
            )

            for item in cantidades_por_producto:
                # Sumo el stock por producto para no hacer un update por cada fila.
                Producto.objects.select_for_update().filter(pk=item['producto_id']).update(
                    stock_disponible=models.F('stock_disponible') + item['total']
                )

            vencidos.filter(
                models.Q(motivo_cancelacion__isnull=True) | models.Q(motivo_cancelacion='')
            ).update(motivo_cancelacion=motivo_expirado)

            vencidos.update(estado='expirado')

            return total_actualizados

    @classmethod
    def actualizar_apartados_vencidos_si_corresponde(cls, throttle_seconds=60):
        # Evita que esta limpieza se ejecute demasiadas veces seguidas.
        if cache.add('apartados:expiracion:global_lock', '1', timeout=throttle_seconds):
            return cls.actualizar_apartados_vencidos()
        return 0

    def generar_codigo_verificacion(self):
        while True:
            codigo = f"{random.randint(0, 999999):06d}"
            if not Apartado.objects.filter(codigo_verificacion=codigo).exclude(pk=self.pk).exists():
                return codigo

    def _cantidad_reservada_para_estado(self, estado, cantidad=None):
        cantidad = self.cantidad if cantidad is None else cantidad
        return cantidad if estado in self.ESTADOS_CON_STOCK_OCUPADO else 0

    def _ajustar_stock_producto(self, producto_id, delta_consumo):
        # Ajusto el stock del producto con bloqueo de fila para no pisar cambios.
        if delta_consumo == 0:
            return

        producto = Producto.objects.select_for_update().get(pk=producto_id)

        if delta_consumo > 0 and producto.stock_disponible < delta_consumo:
            raise ValidationError(f'No hay suficiente stock disponible para {producto.nombre}.')

        producto.stock_disponible -= delta_consumo
        producto.save(update_fields=['stock_disponible'])

    def save(self, *args, **kwargs):
        # El guardado del apartado toca stock, estado y datos de confirmación.
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