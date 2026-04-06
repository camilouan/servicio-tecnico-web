from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Usuario, Producto, Apartado, Categoria, HeroBanner


admin.site.site_header = 'Administración Servicio Técnico'
admin.site.site_title = 'Servicio Técnico Admin'
admin.site.index_title = 'Gestión interna del sistema'
admin.site.logout_template = 'admin/logged_out.html'


def render_image_preview(url):
    if not url:
        return 'Sin imagen'
    if not str(url).startswith('http'):
        url = f"{settings.STATIC_URL}{url}"
    return format_html(
        '<img src="{}" style="width:48px;height:48px;object-fit:cover;border-radius:10px;border:1px solid #dbeafe;" />',
        url,
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock_disponible', 'activo', 'imagen_preview')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre', 'descripcion', 'categoria__nombre')
    ordering = ('nombre',)
    list_per_page = 20

    def imagen_preview(self, obj):
        return render_image_preview(obj.imagen_url)

    imagen_preview.short_description = 'Imagen'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'imagen_preview')
    list_filter = ('activa',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

    def imagen_preview(self, obj):
        return render_image_preview(obj.imagen_url)

    imagen_preview.short_description = 'Imagen'


@admin.register(Apartado)
class ApartadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'codigo_verificacion', 'cantidad', 'estado', 'fecha_apartado', 'fecha_expiracion')
    list_filter = ('estado', 'fecha_apartado')
    search_fields = ('usuario__username', 'producto__nombre', 'codigo_verificacion')
    autocomplete_fields = ('usuario', 'producto', 'confirmado_por')
    list_select_related = ('usuario', 'producto', 'confirmado_por')
    ordering = ('-fecha_apartado',)
    list_per_page = 25
    readonly_fields = ('codigo_verificacion',)


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'orden', 'fecha_actualizacion', 'imagen_preview')
    list_editable = ('activo', 'orden')
    search_fields = ('titulo', 'subtitulo')
    ordering = ('-orden', '-fecha_actualizacion')

    def imagen_preview(self, obj):
        return render_image_preview(obj.fondo_url)

    imagen_preview.short_description = 'Fondo'


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'nombres', 'apellidos', 'rol', 'activo', 'is_staff')
    list_filter = ('rol', 'activo', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'nombres', 'apellidos', 'documento_identidad')
    ordering = ('username',)
    readonly_fields = ('fecha_registro', 'ultima_actualizacion_password')

    fieldsets = UserAdmin.fieldsets + (
        (
            'Información personal adicional',
            {
                'fields': (
                    'nombres',
                    'apellidos',
                    'telefono',
                    'documento_identidad',
                    'direccion',
                    'ciudad',
                    'foto_perfil',
                    'rol',
                    'activo',
                    'fecha_registro',
                    'ultima_actualizacion_password',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Datos del usuario',
            {
                'fields': (
                    'nombres',
                    'apellidos',
                    'email',
                    'telefono',
                    'documento_identidad',
                    'direccion',
                    'ciudad',
                    'rol',
                    'activo',
                )
            },
        ),
    )