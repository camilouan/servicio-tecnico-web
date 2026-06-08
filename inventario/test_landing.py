from django.test import TestCase
from django.urls import reverse

from inventario.models import Categoria


class LandingViewTests(TestCase):
    # Este archivo se ejecuta con pytest para revisar que la landing siga
    # funcionando bien. Sirve para detectar errores rápido antes de que se
    # rompa la página principal cuando cambiemos vistas, templates o modelos.
    def test_landing_view_status_code(self):
        # Reviso que la página principal abra bien y no tire error.
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_includes_categoria(self):
        # Creo una categoría de prueba para ver si luego aparece en la landing.
        Categoria.objects.create(nombre='Celulares', descripcion='Telefonos', activa=True)
        response = self.client.get(reverse('landing'))
        # Confirmo que el texto sí se muestre en la página.
        self.assertContains(response, 'Celulares')

#cd "C:\Users\CLIENTE PC\servicio_tecnico"
#& "C:\Users\CLIENTE PC\servicio_tecnico\venv\Scripts\Activate.ps1"
#pytest inventario/test_landing.py
