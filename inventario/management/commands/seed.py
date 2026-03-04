from django.core.management.base import BaseCommand
from inventario.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Cargar datos iniciales'

    def handle(self, *args, **kwargs):

        categorias = [
            "Celulares",
            "Accesorios",
            "Consolas",
            "Computadores"
        ]

        for nombre in categorias:
            Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={"descripcion": f"Categoria {nombre}"}
            )

        celulares = Categoria.objects.get(nombre="Celulares")
        accesorios = Categoria.objects.get(nombre="Accesorios")
        consolas = Categoria.objects.get(nombre="Consolas")
        computadores = Categoria.objects.get(nombre="Computadores")

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
            Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": f"{nombre} disponible",
                    "precio": precio,
                    "stock_total": stock,
                    "stock_disponible": stock,
                    "categoria": categoria
                }
            )

        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados correctamente"))