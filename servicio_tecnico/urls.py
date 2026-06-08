"""
URL configuration for servicio_tecnico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


    Este archivo decide qué vistas se muestran según la dirección web que
      escriba el usuario. Es como un menú que dice "si visitas /admin/ muestra
      la página de administración".
     urlpatterns es simplemente una lista con reglas: cada regla dice qué
      función o conjunto de rutas usar cuando la URL coincide.
     es solo una lista de instrucciones que Django sigue para encontrarla vista correcta.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
]

#  Aquí se colocan las entradas del menú de la web.
# Cada path() dice: cuando veas esta parte de la URL, llama a esto
#  Por ejemplo, la segunda línea incluye todas las rutas definidas en
#   la app inventario para la raíz del sitio.

# serve static and media files only when DEBUG is enabled (debug controlled via env vars)
# in production Render should be configured with an object store or volume
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)