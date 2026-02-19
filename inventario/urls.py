from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apartar/<int:producto_id>/', views.apartar_producto, name='apartar'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),


]
