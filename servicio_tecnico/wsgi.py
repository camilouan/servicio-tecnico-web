"""
WSGI config for servicio_tecnico project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicio_tecnico.settings')

# Wrap the standard Django application with WhiteNoise so that static
# files (and optionally media) can be served directly by the WSGI app.
# Render's docs recommend using an object store for media, but it's
# convenient during testing or if you mount a persistent volume.
application = get_wsgi_application()

try:
    # only import whitenoise if it's installed; it is already used for
    # static files via middleware, this just extends it to media.
    from whitenoise import WhiteNoise
    from django.conf import settings

    # add media directory under the /media/ URL prefix
    application = WhiteNoise(application, root=settings.STATIC_ROOT)
    application.add_files(settings.MEDIA_ROOT, prefix=settings.MEDIA_URL)
except ImportError:
    pass  # whitenoise not available, rely on Django or external server

