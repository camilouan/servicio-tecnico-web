from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Apartado, Categoria, Producto


class BaseInventarioTestCase(TestCase):
    def setUp(self):
        cache.clear()
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
        self.login_url = reverse('login')


class ApartadoStockAutomationTests(BaseInventarioTestCase):
    def setUp(self):
        super().setUp()
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


class LoginSecurityTests(BaseInventarioTestCase):
    @override_settings(
        LOGIN_MAX_FAILED_ATTEMPTS=3,
        LOGIN_LOCKOUT_SECONDS=60,
        SESSION_INACTIVITY_TIMEOUT=1200,
        SESSION_COOKIE_AGE=1200,
        SESSION_SAVE_EVERY_REQUEST=True,
    )
    def test_login_is_temporarily_blocked_after_max_failed_attempts(self):
        for _ in range(3):
            response = self.client.post(
                self.login_url,
                {'username': self.usuario.username, 'password': 'incorrecta123'},
            )

        self.assertContains(response, 'bloqueado temporalmente')

        blocked_response = self.client.post(
            self.login_url,
            {'username': self.usuario.username, 'password': 'ClaveSegura123!'},
        )
        self.assertContains(blocked_response, 'bloqueado temporalmente')
        self.assertNotIn('_auth_user_id', self.client.session)

    @override_settings(
        SESSION_INACTIVITY_TIMEOUT=60,
        SESSION_COOKIE_AGE=60,
        SESSION_SAVE_EVERY_REQUEST=True,
    )
    def test_inactive_session_is_closed_on_next_request(self):
        self.client.post(
            self.login_url,
            {'username': self.usuario.username, 'password': 'ClaveSegura123!'},
        )

        session = self.client.session
        session['last_activity'] = (timezone.now() - timezone.timedelta(minutes=5)).isoformat()
        session.save()

        response = self.client.get(reverse('mis_apartados'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
        self.assertNotIn('_auth_user_id', self.client.session)


class LegalAcceptanceTests(BaseInventarioTestCase):
    def test_registration_requires_legal_acceptance(self):
        response = self.client.post(
            reverse('registro'),
            {
                'username': 'nuevo_cliente',
                'email': 'nuevo@test.com',
                'nombres': 'Nuevo',
                'apellidos': 'Cliente',
                'telefono': '3011111111',
                'documento_identidad': '987654321',
                'direccion': 'Calle 99',
                'ciudad': 'Bogotá',
                'password1': 'ClaveSegura123!',
                'password2': 'ClaveSegura123!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Debes aceptar la Política de Privacidad y los Términos de Servicio')
        self.assertFalse(get_user_model().objects.filter(username='nuevo_cliente').exists())

    def test_legal_banner_is_visible_on_first_visit(self):
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Al continuar navegando en esta plataforma')
        self.assertContains(response, 'legalConsentBanner')
