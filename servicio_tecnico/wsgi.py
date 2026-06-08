"""
Configuración WSGI para el proyecto servicio_tecnico.

Esto deja disponible una variable llamada ``application`` que es lo que
el servidor web (por ejemplo Gunicorn o cualquier servidor WSGI) usa para
enviar solicitudes a Django.

WSGI es como el traductor entre el servidor y
la app. Aquí creamos el traductor (`application`) para que el servidor
pueda preguntarle a Django "¿qué respondo cuando llega esta petición?".

Más info: https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Le decimos a Django qué configuración usar. Es como ponerle una etiqueta
# al proyecto para que sepa dónde están las opciones (base de datos, apps,
# etc.).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicio_tecnico.settings')

# `get_wsgi_application()` crea la aplicación WSGI que el servidor usará.
# Piensa en application como la puerta de entrada a Django para todas
# las peticiones HTTP.
application = get_wsgi_application()

try:
    # WhiteNoise permite servir archivos estáticos y (opcionalmente) media
    # directamente desde la misma aplicación WSGI. Esto es útil para pruebas
    # o despliegues simples. Si no está instalado, seguimos sin él.
    from whitenoise import WhiteNoise
    from django.conf import settings

    # Añadimos los archivos estáticos y la carpeta de media para que se
    # puedan servir desde las rutas `STATIC_URL` y `MEDIA_URL`.
    application = WhiteNoise(application, root=settings.STATIC_ROOT)
    application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
except ImportError:
    # Si WhiteNoise no está disponible, se asumirá que otro servidor (o
    # la configuración de Django) se encargará de los archivos estáticos.
    pass

