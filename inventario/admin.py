from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Producto, Apartado, Categoria


admin.site.register(Producto)
admin.site.register(Apartado)
admin.site.register(Categoria)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    pass