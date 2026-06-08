"""
Configuración para pytest en este proyecto.
este archivo prepara Django para que las pruebas
puedan usar los modelos y todo lo relacionado con el framework. Sin esto,
los tests no tendrían acceso a la configuración ni a la base de datos.

También contiene una pequeña regla para decirle a pytest que ignore un
script específico scripts/test_admin_request.py porque ese archivo se
ejecuta de forma independiente y no es una prueba normal.
"""

import os

import django


# Le decimos a Django cuál es el módulo de settings a usar. Es como poner
# el mapa de configuración para que sepa dónde están la BD, apps, y demás.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicio_tecnico.settings')
# Inicializamos Django para que los siguientes imports y pruebas funcionen.
django.setup()


def pytest_ignore_collect(collection_path, config):
    # Evitamos que pytest recoja el script que está en `scripts/test_admin_request.py`.
    # Ese archivo no es una prueba estándar, es un script que se lanza a mano,
    # así que lo saltamos durante la recolección de tests.
    return collection_path.as_posix().endswith('scripts/test_admin_request.py')