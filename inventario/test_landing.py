import pytest
from django.urls import reverse
from inventario.models import Categoria

pytestmark = pytest.mark.django_db


def test_landing_view_status_code(client):
    url = reverse('landing')
    response = client.get(url)
    assert response.status_code == 200


def test_landing_includes_categoria(client):
    Categoria.objects.create(nombre='Celulares', descripcion='Telefonos', activa=True)
    response = client.get(reverse('landing'))
    assert b'Celulares' in response.content
