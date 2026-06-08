"""
Configuración ASGI para el proyecto servicio_tecnico.

Deja disponible una variable llamada application que es lo que usan
servicios/asynchronous servers (como Uvicorn) para comunicarse con Django.

ASGI es parecido a WSGI pero pensado para cosas
más modernas como conexiones en tiempo real. Aquí creamos la puerta
application por donde entran las solicitudes o conexiones.

Más info: https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Le indicamos a Django qué configuración usar (base de datos, apps,
# middlewares, etc.). Es como ponerle una etiqueta para saber dónde están
# las opciones del proyecto.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicio_tecnico.settings')

# get_asgi_application() crea la aplicación ASGI que el servidor usará.
# Piensa en application como la entrada principal para todo lo que llega
# al proyecto (peticiones HTTP, websockets si se usan, etc.).
application = get_asgi_application()
