import cloudinary.uploader
from django.conf import settings
from django.utils.text import slugify

from .models import Categoria, Producto

CATEGORY_IMAGES = {
    "Celulares": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1200&q=80",
    "Accesorios": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=1200&q=80",
    "Consolas": "https://images.unsplash.com/photo-1606813908076-767438e1eb14?auto=format&fit=crop&w=1200&q=80",
    "Computadores": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
}

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
