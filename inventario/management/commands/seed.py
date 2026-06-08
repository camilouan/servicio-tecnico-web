import cloudinary.uploader
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from inventario.models import Categoria, Producto

# Estas imágenes son solo de ejemplo para que el catálogo no se vea vacío
# cuando se cargan datos iniciales.
CATEGORY_IMAGES = {
    "Celulares": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80",
    "Accesorios": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Consolas": "https://images.unsplash.com/photo-1606813908076-767438e1eb14?auto=format&fit=crop&w=1200&q=80",
    "Computadores": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
}


# Mapa con imágenes de muestra para productos. Se usa cuando se quiere
# poblar la base de datos con contenido visual rápido.
PRODUCT_IMAGES = {
    "iPhone 14": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80",
    "Samsung Galaxy S23": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80",
    "Xiaomi Redmi Note 12": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Motorola Edge 40": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Audifonos Bluetooth": "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=1200&q=80",
    "Teclado Mecanico RGB": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Mouse Gamer": "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=1200&q=80",
    "Cargador Rapido": "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=1200&q=80",
    "PlayStation 5": "https://images.unsplash.com/photo-1606813908076-767438e1eb14?auto=format&fit=crop&w=1200&q=80",
    "Xbox Series X": "https://images.unsplash.com/photo-1616375826390-5f4df3382b6b?auto=format&fit=crop&w=1200&q=80",
    "Nintendo Switch": "https://images.unsplash.com/photo-1555617117-08e0a9b7c55d?auto=format&fit=crop&w=1200&q=80",
    "Laptop HP": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "MacBook Air": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Asus ROG": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "Monitor Gamer": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Tablet Samsung": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
    "Smartwatch": "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=1200&q=80",
    "Parlante JBL": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80",
    "Camara Web": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Control PS5": "https://images.unsplash.com/photo-1606813908076-767438e1eb14?auto=format&fit=crop&w=1200&q=80",
}


def upload_remote_image(source_url, public_id):
    # Si no hay Cloudinary configurado, no intento subir nada.
    if not settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'):
        return None

    try:
        # Subo la imagen desde una URL externa y guardo el identificador
        # que luego se usa en el modelo.
        result = cloudinary.uploader.upload(
            source_url,
            public_id=public_id,
            overwrite=True,
            resource_type='image'
        )
        return result.get('public_id')
    except Exception:
        # Si algo falla, no detengo todo el seed; simplemente sigo sin imagen.
        return None


def get_first_or_create(model_class, lookup_field, lookup_value, defaults):
    # Busco primero si ya existe el registro para no duplicar datos.
    queryset = model_class.objects.filter(**{lookup_field: lookup_value}).order_by('id')
    instance = queryset.first()

    if instance is not None:
        return instance, False

    # Si no existe, lo creo con los datos por defecto.
    return model_class.objects.create(**{lookup_field: lookup_value, **defaults}), True


class Command(BaseCommand):
    # Este comando carga categorías y productos base para arrancar el proyecto
    # con datos listos.
    help = 'Cargar datos iniciales y subir imágenes a Cloudinary para Render'

    def add_arguments(self, parser):
        # Opción para subir imágenes de ejemplo además de los registros.
        parser.add_argument(
            '--with-images',
            action='store_true',
            help='Sube imágenes de ejemplo a Cloudinary y las asigna a productos y categorías.'
        )
        # Opción para volver a subir imágenes aunque ya existan.
        parser.add_argument(
            '--force-images',
            action='store_true',
            help='Reemplaza imágenes existentes y vuelve a subir el catálogo completo a Cloudinary.'
        )

    def handle(self, *args, **kwargs):
        # Leo las opciones del comando para saber si debo cargar imágenes.
        with_images = kwargs.get('with_images', False)
        force_images = kwargs.get('force_images', False)

        # Categorías base que necesita el catálogo.
        categorias = [
            "Celulares",
            "Accesorios",
            "Consolas",
            "Computadores"
        ]

        for nombre in categorias:
            # Creo la categoría si no existe, o reutilizo la que ya está.
            categoria, _ = get_first_or_create(
                Categoria,
                'nombre',
                nombre,
                {
                    "descripcion": f"Categoría {nombre}",
                    "activa": True,
                }
            )

            # Si activé imágenes, subo una imagen de ejemplo para la categoría.
            if with_images and (force_images or not categoria.imagen):
                image_url = CATEGORY_IMAGES.get(nombre)
                if image_url:
                    public_id = upload_remote_image(
                        image_url,
                        f"servicio_tecnico/categorias/{slugify(nombre)}"
                    )
                    if public_id:
                        categoria.imagen = public_id
                        categoria.save()

        # Busco las categorías base para usarlas al crear productos.
        celulares = Categoria.objects.filter(nombre="Celulares").order_by('id').first()
        accesorios = Categoria.objects.filter(nombre="Accesorios").order_by('id').first()
        consolas = Categoria.objects.filter(nombre="Consolas").order_by('id').first()
        computadores = Categoria.objects.filter(nombre="Computadores").order_by('id').first()

        # Si falta una categoría base, paro el comando porque el catálogo quedaría incompleto.
        if not all([celulares, accesorios, consolas, computadores]):
            raise self.CommandError("No se encontraron todas las categorías base requeridas.")

        # Lista de productos iniciales para que el frontend tenga contenido real.
        productos = [
            ("iPhone 14", celulares, 4500000, 10),
            ("Samsung Galaxy S23", celulares, 4200000, 10),
            ("Xiaomi Redmi Note 12", celulares, 1200000, 10),
            ("Motorola Edge 40", celulares, 2000000, 10),

            ("Audifonos Bluetooth", accesorios, 120000, 20),
            ("Teclado Mecanico RGB", accesorios, 250000, 15),
            ("Mouse Gamer", accesorios, 90000, 20),
            ("Cargador Rapido", accesorios, 50000, 25),

            ("PlayStation 5", consolas, 2800000, 5),
            ("Xbox Series X", consolas, 2700000, 5),
            ("Nintendo Switch", consolas, 1800000, 5),

            ("Laptop HP", computadores, 2500000, 7),
            ("MacBook Air", computadores, 5200000, 5),
            ("Asus ROG", computadores, 4800000, 5),
            ("Monitor Gamer", computadores, 900000, 10),
            ("Tablet Samsung", computadores, 1500000, 8),
            ("Smartwatch", accesorios, 350000, 10),
            ("Parlante JBL", accesorios, 300000, 10),
            ("Camara Web", accesorios, 180000, 10),
            ("Control PS5", accesorios, 280000, 10),
        ]

        for nombre, categoria, precio, stock in productos:
            # Igual que con las categorías: si ya existe, lo reutilizo.
            producto, _ = get_first_or_create(
                Producto,
                'nombre',
                nombre,
                {
                    "descripcion": f"{nombre} disponible",
                    "precio": precio,
                    "stock_total": stock,
                    "stock_disponible": stock,
                    "categoria": categoria,
                    "activo": True,
                }
            )

            # Si pedí imágenes, subo una imagen de ejemplo para cada producto.
            if with_images and (force_images or not producto.imagen):
                image_url = PRODUCT_IMAGES.get(nombre)
                if image_url:
                    public_id = upload_remote_image(
                        image_url,
                        f"servicio_tecnico/productos/{slugify(nombre)}"
                    )
                    if public_id:
                        producto.imagen = public_id
                        producto.save()

        # Mensaje final para saber que el seed terminó bien.
        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados correctamente."))

        if with_images:
            self.stdout.write(self.style.SUCCESS("Imágenes de ejemplo cargadas en Cloudinary."))
        else:
            # Aviso para recordar que las imágenes son opcionales.
            self.stdout.write(self.style.WARNING(
                "Ejecuta el comando con --with-images para subir imágenes de muestra a Cloudinary."
            ))
