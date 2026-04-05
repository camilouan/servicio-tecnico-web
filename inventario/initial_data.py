import cloudinary.uploader
from django.conf import settings
from django.utils.text import slugify

from .models import Categoria, Producto

CATEGORY_IMAGES = {
    "Celulares": "https://picsum.photos/seed/celulares/1200/800",
    "Accesorios": "https://picsum.photos/seed/accesorios/1200/800",
    "Consolas": "https://picsum.photos/seed/consolas/1200/800",
    "Computadores": "https://picsum.photos/seed/computadores/1200/800",
}

PRODUCT_IMAGES = {
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


def upload_remote_image(source_url, public_id):
    if not settings.CLOUDINARY_STORAGE.get('CLOUD_NAME'):
        return None

    try:
        result = cloudinary.uploader.upload(
            source_url,
            public_id=public_id,
            overwrite=True,
            resource_type='image'
        )
        return result.get('public_id')
    except Exception:
        return None


def ensure_initial_data():
    categorias = [
        "Celulares",
        "Accesorios",
        "Consolas",
        "Computadores"
    ]

    for nombre in categorias:
        categoria, _ = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={
                "descripcion": f"Categoría {nombre}",
                "activa": True,
            }
        )

        if not categoria.imagen:
            image_url = CATEGORY_IMAGES.get(nombre)
            if image_url:
                public_id = upload_remote_image(
                    image_url,
                    f"servicio_tecnico/categorias/{slugify(nombre)}"
                )
                if public_id:
                    categoria.imagen = public_id
                    categoria.save()

    productos = [
        ("iPhone 14", "Celulares", 4500000, 10),
        ("Samsung Galaxy S23", "Celulares", 4200000, 10),
        ("Xiaomi Redmi Note 12", "Celulares", 1200000, 10),
        ("Motorola Edge 40", "Celulares", 2000000, 10),
        ("Audifonos Bluetooth", "Accesorios", 120000, 20),
        ("Teclado Mecanico RGB", "Accesorios", 250000, 15),
        ("Mouse Gamer", "Accesorios", 90000, 20),
        ("Cargador Rapido", "Accesorios", 50000, 25),
        ("PlayStation 5", "Consolas", 2800000, 5),
        ("Xbox Series X", "Consolas", 2700000, 5),
        ("Nintendo Switch", "Consolas", 1800000, 5),
        ("Laptop HP", "Computadores", 2500000, 7),
        ("MacBook Air", "Computadores", 5200000, 5),
        ("Asus ROG", "Computadores", 4800000, 5),
        ("Monitor Gamer", "Computadores", 900000, 10),
        ("Tablet Samsung", "Computadores", 1500000, 8),
        ("Smartwatch", "Accesorios", 350000, 10),
        ("Parlante JBL", "Accesorios", 300000, 10),
        ("Camara Web", "Accesorios", 180000, 10),
        ("Control PS5", "Accesorios", 280000, 10),
    ]

    for nombre, categoria_nombre, precio, stock in productos:
        categoria = Categoria.objects.get(nombre=categoria_nombre)
        producto, _ = Producto.objects.get_or_create(
            nombre=nombre,
            defaults={
                "descripcion": f"{nombre} disponible",
                "precio": precio,
                "stock_total": stock,
                "stock_disponible": stock,
                "categoria": categoria,
                "activo": True,
            }
        )

        if not producto.imagen:
            image_url = PRODUCT_IMAGES.get(nombre)
            if image_url:
                public_id = upload_remote_image(
                    image_url,
                    f"servicio_tecnico/productos/{slugify(nombre)}"
                )
                if public_id:
                    producto.imagen = public_id
                    producto.save()
