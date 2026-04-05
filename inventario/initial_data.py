import cloudinary.uploader
from django.conf import settings
from django.utils.text import slugify

from .models import Categoria, Producto

CATEGORY_IMAGES = {
    "Celulares": "https://commons.wikimedia.org/wiki/Special:FilePath/Mobile_Phone_Evolution_1992_-_2014.jpg",
    "Accesorios": "https://commons.wikimedia.org/wiki/Special:FilePath/SanDisk-Cruzer-USB-4GB-ThumbDrive.jpg",
    "Consolas": "https://commons.wikimedia.org/wiki/Special:FilePath/Gaming_Section_1_-_Retrosystems_2010.jpg",
    "Computadores": "https://commons.wikimedia.org/wiki/Special:FilePath/Laptop_collage.jpg",
}

PRODUCT_IMAGES = {
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
