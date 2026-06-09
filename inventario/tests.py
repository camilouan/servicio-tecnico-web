from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import CambioPasswordSemanalForm, RegistroForm
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
        # CP18 / RF17: este caso valida que, al cancelar un apartado,
        # el stock del producto vuelve a subir como se espera.
        # Se valida mirando que stock_disponible baje cuando se crea el
        # apartado y luego vuelva al valor original cuando el estado cambia.
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
        # CP18 / RF17: revisa la reposición automática cuando un apartado
        # ya venció y el sistema lo marca como expirado.
        # Se valida comprobando tres cosas: cuántos apartados se actualizaron,
        # que el estado pase a `expirado` y que el stock regrese completo.
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

    def test_expiracion_throttled_evita_ejecuciones_repetidas(self):
        # CP18 / RF17: comprueba que la limpieza de apartados vencidos no
        # se ejecute dos veces seguidas por accidente.
        # Se valida esperando que la primera ejecución procese 1 apartado y
        # la segunda devuelva 0 por el bloqueo temporal de caché.
        Apartado.objects.create(
            usuario=self.usuario,
            producto=self.producto,
            cantidad=1,
            estado='pendiente',
            fecha_expiracion=timezone.now() - timezone.timedelta(hours=2),
        )

        primero = Apartado.actualizar_apartados_vencidos_si_corresponde(throttle_seconds=60)
        segundo = Apartado.actualizar_apartados_vencidos_si_corresponde(throttle_seconds=60)

        self.assertEqual(primero, 1)
        self.assertEqual(segundo, 0)


class LoginSecurityTests(BaseInventarioTestCase):
    @override_settings(
        LOGIN_MAX_FAILED_ATTEMPTS=3,
        LOGIN_LOCKOUT_SECONDS=60,
        SESSION_INACTIVITY_TIMEOUT=1200,
        SESSION_COOKIE_AGE=1200,
        SESSION_SAVE_EVERY_REQUEST=True,
    )
    def test_login_is_temporarily_blocked_after_max_failed_attempts(self):
        # CP04 / RF3: este caso representa el inicio de sesión fallido y
        # confirma que el sistema bloquea temporalmente el acceso.
        # Se valida haciendo varios intentos fallidos y revisando que el
        # mensaje de bloqueo aparezca y que la sesión no quede autenticada.
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
        # CP03 / RF3 y CP04 / RF3: ayuda a verificar que, después del login,
        # una sesión inactiva se cierre al volver a usar el sistema.
        # Se valida forzando una actividad vieja en la sesión y comprobando
        # que el siguiente acceso redirige al login.
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
        # CP01 / RF1 y CP02 / RF2: el registro pide aceptar políticas para
        # crear la cuenta y evita guardar usuarios incompletos.
        # Se valida enviando el formulario sin aceptar políticas, esperando
        # un error en pantalla y confirmando que el usuario no se crea.
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
        # CP01 / RF1: comprueba que el banner legal se muestre al entrar por
        # primera vez, como parte del registro y la aceptación de políticas.
        # Se valida revisando que el texto legal y el ID del banner salgan en
        # la respuesta de la landing.
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Al continuar navegando en esta plataforma')
        self.assertContains(response, 'legalConsentBanner')

class AdminPopupRenderingTests(TestCase):
    def test_staff_admin_renderiza_popup_de_apartados(self):
        """Asegura que Jazzmin renderice el popup dentro del bloque correcto."""
        usuario = get_user_model().objects.create_user(
            username='staff_popup',
            password='ClaveSegura123!',
            email='staff-popup@test.com',
            nombres='Staff',
            apellidos='Popup',
            telefono='3000000000',
            documento_identidad='555555555',
            direccion='Calle Admin',
            ciudad='Bogotá',
            is_staff=True,
        )

        self.client.force_login(usuario)
        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'adminApartadosOverlay')
        self.assertContains(response, 'openAdminApartadosPopup')


class HealthChecksTests(TestCase):
    def test_healthz_responde_ok(self):
        # Este test no está dentro del cuadro funcional, pero sirve para
        # revisar que el sistema siga vivo y responda correctamente.
        # Se valida con un `200` y con un JSON que diga `status: ok`.
        response = self.client.get(reverse('healthz'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})

    def test_readyz_responde_ready(self):
        # Igual que el anterior, este chequea que la app esté lista para usar.
        # Se valida con un `200` y con un JSON que diga `status: ready`.
        response = self.client.get(reverse('readyz'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ready'})


class ModelValidationTests(TestCase):
    def test_categoria_clean_rechaza_campos_obligatorios_vacios(self):
        """Evita guardar categorías incompletas y documenta la validación de datos.

        Este test protege la calidad del catálogo porque confirma que el modelo
        no acepta categorías sin nombre ni descripción.
        """
        # CP06 / RF5 y CP09 / RF8: aunque no crea productos todavía, este
        # test asegura que la base de categorías del inventario no se guarde mal.
        # Se valida llamando `full_clean()` y esperando un ValidationError
        categoria = Categoria(nombre=' ', descripcion=' ', activa=True)

        with self.assertRaises(ValidationError) as context:
            categoria.full_clean()

        self.assertIn('El nombre de la categoría es obligatorio.', str(context.exception))

    def test_producto_clean_rechaza_stock_inconsistente(self):
        """Detecta errores de stock antes de guardar productos inconsistentes.

        Sirve para evitar que el stock disponible sea mayor al stock total, una
        condición que después rompe la lógica de apartados.
        """
        # CP06 / RF5, CP07 / RF6 y CP10 / RF9: este control ayuda a que el
        # inventario se cree y se edite con números coherentes.
        # Se valida ejecutando full_clean() y comprobando que el error de
        # stock inconsistente realmente aparezca.
        categoria = Categoria.objects.create(
            nombre='Accesorios',
            descripcion='Prueba de validación de producto',
            activa=True,
        )
        producto = Producto(
            nombre='Mouse Gamer',
            descripcion='Producto inválido para validar stock',
            precio=1500,
            stock_total=2,
            stock_disponible=5,
            categoria=categoria,
            activo=True,
        )

        with self.assertRaises(ValidationError) as context:
            producto.full_clean()

        self.assertIn('El stock disponible no puede ser mayor al stock total.', str(context.exception))


class FormValidationTests(TestCase):
    def test_registro_form_guarda_aceptacion_legal(self):
        """Comprueba que el registro obliga a aceptar políticas y deja trazabilidad.

        Ayuda a detectar regresiones en el alta de usuarios y confirma que el
        formulario marca la aceptación legal al crear la cuenta.
        """
        # CP01 / RF1 y CP02 / RF2: cubre el registro de usuario y la parte
        # legal que pide aceptar políticas antes de crear la cuenta.
        # Se valida con form.is_valid(), luego save(), y revisando los
        # campos acepta_politicas y fecha_aceptacion_politicas
        form = RegistroForm(
            data={
                'username': 'cliente_nuevo',
                'email': 'cliente_nuevo@test.com',
                'nombres': 'Cliente',
                'apellidos': 'Nuevo',
                'telefono': '3001112222',
                'documento_identidad': '123456780',
                'direccion': 'Calle 10',
                'ciudad': 'Bogotá',
                'password1': 'ClaveSegura123!',
                'password2': 'ClaveSegura123!',
                'acepta_politicas': 'on',
            }
        )

        self.assertTrue(form.is_valid())
        usuario = form.save()

        self.assertTrue(usuario.acepta_politicas)
        self.assertIsNotNone(usuario.fecha_aceptacion_politicas)

    def test_cambio_password_form_bloquea_cambio_semanal(self):
        """Bloquea cambios de contraseña demasiado frecuentes.

        Este test protege la regla de seguridad que limita la frecuencia de
        cambio de clave para reducir abusos o cambios accidentales.
        """
        # CP03 / RF3: no es login como tal, pero sí protege la seguridad del
        # acceso al impedir cambios de contraseña demasiado seguidos.
        # Se valida dejando una fecha reciente de cambio y esperando que el
        # formulario salga inválido con el mensaje de bloqueo semanal.
        usuario = get_user_model().objects.create_user(
            username='seguridad_test',
            password='ClaveSegura123!',
            email='seguridad@test.com',
            nombres='Seguridad',
            apellidos='Prueba',
            telefono='3002223333',
            documento_identidad='987654321',
            direccion='Calle 11',
            ciudad='Bogotá',
        )
        usuario.ultima_actualizacion_password = timezone.now()
        usuario.save(update_fields=['ultima_actualizacion_password'])

        form = CambioPasswordSemanalForm(
            user=usuario,
            data={
                'old_password': 'ClaveSegura123!',
                'new_password1': 'NuevaClave123!',
                'new_password2': 'NuevaClave123!',
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Solo puedes cambiar tu contraseña una vez por semana.', form.errors.as_text())


class CatalogoYApartadosTests(BaseInventarioTestCase):
    def setUp(self):
        super().setUp()
        self.categoria_celulares = Categoria.objects.create(
            nombre='Celulares',
            descripcion='Catálogo de celulares',
            activa=True,
        )
        self.categoria_accesorios = Categoria.objects.create(
            nombre='Accesorios',
            descripcion='Catálogo de accesorios',
            activa=True,
        )
        self.producto_disponible = Producto.objects.create(
            nombre='Samsung Galaxy S23',
            descripcion='Producto disponible',
            precio=3500000,
            stock_total=5,
            stock_disponible=5,
            categoria=self.categoria_celulares,
            activo=True,
        )
        self.producto_agotado = Producto.objects.create(
            nombre='Cargador Rápido',
            descripcion='Producto agotado',
            precio=50000,
            stock_total=3,
            stock_disponible=0,
            categoria=self.categoria_accesorios,
            activo=True,
        )

    def test_productos_view_filtra_por_categoria_y_disponibilidad(self):
        """Comprueba que el catálogo responde a filtros públicos reales.

        Sirve para detectar regresiones en la vista de productos, especialmente
        en el filtrado por categoría y por existencia de stock.
        """
        # CP09 / RF8 y CP10 / RF9: esta prueba confirma que el catálogo se ve
        # y que los filtros por categoría, disponibilidad y orden funcionan.
        # Se valida consultando la vista con parámetros y revisando qué
        # productos aparecen o no aparecen en la respuesta.
        response = self.client.get(
            reverse('productos'),
            {'categoria': 'Celulares', 'disponibilidad': 'disponibles', 'orden': 'precio_desc'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Samsung Galaxy S23')
        self.assertNotContains(response, 'Cargador Rápido')

    def test_apartar_producto_descuenta_stock_y_crea_apartado(self):
        """Valida el flujo integrado de apartar un producto autenticado.

        Este test protege el comportamiento central del negocio: crear un
        apartado debe bajar el stock disponible y generar el registro asociado.
        """
        # CP11 / RF10, CP12 / RF11, CP13 / RF12 y CP14 / RF13: este es el
        # flujo principal de apartados, porque crea la reserva y descuenta stock.
        # Se valida iniciando sesión, enviando la cantidad a apartar y
        # comprobando que exista el Apartado y que el stock baje.
        self.client.force_login(self.usuario)

        response = self.client.post(
            reverse('apartar', args=[self.producto_disponible.id]),
            {'cantidad': 2},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Apartado.objects.filter(usuario=self.usuario, producto=self.producto_disponible, cantidad=2).exists())
        self.producto_disponible.refresh_from_db()
        self.assertEqual(self.producto_disponible.stock_disponible, 3)

    def test_estado_apartados_api_retorna_solo_apartados_del_usuario(self):
        """Comprueba que la API privada devuelve solo datos del usuario autenticado.

        Esto ayuda a detectar fugas de información entre usuarios en el panel de
        seguimiento de apartados.
        """
        # CP15 / RF14: revisa la consulta de apartados del usuario para que
        # solo se muestren sus datos en la respuesta.
        # Se valida autenticando al usuario, creando un apartado y revisando
        # que el JSON traiga exactamente ese registro con sus campos correctos.
        self.client.force_login(self.usuario)
        apartado = Apartado.objects.create(
            usuario=self.usuario,
            producto=self.producto_disponible,
            cantidad=1,
            estado='pendiente',
            fecha_expiracion=timezone.now() + timezone.timedelta(hours=24),
        )

        response = self.client.get(reverse('estado_apartados_api'))
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload['apartados'][0]['id'], apartado.id)
        self.assertEqual(payload['apartados'][0]['producto'], 'Samsung Galaxy S23')
        self.assertEqual(payload['apartados'][0]['cantidad'], 1)
        self.assertEqual(payload['apartados'][0]['estado'], 'pendiente')
        self.assertEqual(payload['apartados'][0]['estado_display'], 'Pendiente')
