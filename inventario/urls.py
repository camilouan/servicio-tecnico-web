from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Rutas públicas, privadas y de soporte del proyecto.
urlpatterns = [

    path('healthz/', views.healthz, name='healthz'),
    path('readyz/', views.readyz, name='readyz'),

    path('', views.landing, name='landing'),

    # vista original de productos disponible en /home/ para mantener compatibilidad
    path('home/', views.home, name='home'),

    path('productos/', views.productos, name='productos'),

    path('apartar/<int:producto_id>/', views.apartar_producto, name='apartar'),

    path('registro/', views.registro, name='registro'),
    path('api/auth/email-exists/', views.email_exists_api, name='email_exists_api'),

    path('login/', views.login_view, name='login'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),

    path('logout/', views.logout_view, name='logout'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-servicio/', views.terminos_servicio, name='terminos_servicio'),
    path('mis-apartados/', views.mis_apartados, name='mis_apartados'),
    path('mis-apartados/estado/', views.estado_apartados_api, name='estado_apartados_api'),
    path('panel-admin/apartados/resumen/', views.admin_apartados_resumen_api, name='admin_apartados_resumen_api'),
    path('mi-perfil/', views.mi_perfil, name='mi_perfil'),

]

# sólo servir media durante desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)