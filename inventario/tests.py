from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import Apartado, Categoria, Producto


class ApartadoStockAutomationTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.usuario = user_model.objects.create_user(
            username='cliente_test',
            password='ClaveSegura123!',
            email='cliente@test.com',
            nombres='Cliente',
            apellidos='Prueba',
            telefono='3000000000',
            documento_identidad='123456789',
            direccion='Calle 1',
            ciudad='Bogotá',
        )
        self.categoria = Categoria.objects.create(
            nombre='Pruebas',
            descripcion='Categoría de prueba',
            activa=True,
        )
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            descripcion='Producto para validar stock',
            precio=1500,
            stock_total=10,
            stock_disponible=10,
            categoria=self.categoria,
            activo=True,
        )

    def test_cancelar_apartado_repone_stock(self):
        apartado = Apartado.objects.create(
            usuario=self.usuario,
            producto=self.producto,
            cantidad=2,
            estado='pendiente',
            fecha_expiracion=timezone.now() + timezone.timedelta(hours=24),
        )

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_disponible, 8)

        apartado.estado = 'cancelado'
        apartado.save()

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_disponible, 10)

    def test_expirar_apartados_vencidos_repone_stock(self):
        apartado = Apartado.objects.create(
            usuario=self.usuario,
            producto=self.producto,
            cantidad=3,
            estado='pendiente',
            fecha_expiracion=timezone.now() - timezone.timedelta(hours=2),
        )

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_disponible, 7)

        actualizados = Apartado.actualizar_apartados_vencidos()

        apartado.refresh_from_db()
        self.producto.refresh_from_db()

        self.assertEqual(actualizados, 1)
        self.assertEqual(apartado.estado, 'expirado')
        self.assertEqual(self.producto.stock_disponible, 10)
