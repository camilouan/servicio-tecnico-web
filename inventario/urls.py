from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', views.landing, name='landing'),

    # vista original de productos disponible en /home/ para mantener compatibilidad
    path('home/', views.home, name='home'),

    path('productos/', views.productos, name='productos'),

    path('apartar/<int:producto_id>/', views.apartar_producto, name='apartar'),

    path('registro/', views.registro, name='registro'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('mis-apartados/', views.mis_apartados, name='mis_apartados'),
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),

]

# sólo servir media durante desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)