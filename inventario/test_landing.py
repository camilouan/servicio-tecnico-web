from django.test import TestCase
from django.urls import reverse

from inventario.models import Categoria


class LandingViewTests(TestCase):
    def test_landing_view_status_code(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_includes_categoria(self):
        Categoria.objects.create(nombre='Celulares', descripcion='Telefonos', activa=True)
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Celulares')
