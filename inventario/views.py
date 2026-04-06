from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Producto, Apartado, Categoria, HeroBanner
from .forms import RegistroForm, PerfilUsuarioForm, CambioPasswordSemanalForm, EliminarCuentaForm
from .initial_data import ensure_initial_data


def home(request):
    ensure_initial_data()
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # redirige al catálogo, no existe 'home' en urls
            return redirect('productos')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if getattr(user, 'rol', '') == 'administrador' or user.is_staff or user.is_superuser:
                return redirect('/admin/')

            return redirect('productos')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('landing')  # landing es página inicial pública


@login_required
def apartar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (TypeError, ValueError):
        messages.error(request, 'La cantidad ingresada no es válida.')
        return redirect('productos')

    if cantidad < 1:
        messages.error(request, 'Debes apartar al menos una unidad.')
        return redirect('productos')

    if cantidad > 5:
        messages.error(request, 'Solo puedes solicitar hasta 5 unidades por intento.')
        return redirect('productos')

    estados_activos = ['pendiente', 'confirmado']
    apartados_activos_usuario = Apartado.objects.filter(
        usuario=request.user,
        estado__in=estados_activos,
    ).exclude(fecha_expiracion__lt=timezone.now(), estado='pendiente')

    productos_distintos_activos = set(apartados_activos_usuario.values_list('producto_id', flat=True))
    if producto.id not in productos_distintos_activos and len(productos_distintos_activos) >= 3:
        messages.warning(request, 'Solo puedes tener 3 tipos diferentes de productos activos al mismo tiempo. Espera a que uno se entregue, cancele o expire para apartar otro distinto.')
        return redirect('productos')

    cantidad_ya_apartada = apartados_activos_usuario.filter(producto=producto).values_list('cantidad', flat=True)
    total_apartado = sum(cantidad_ya_apartada)

    if total_apartado >= 5:
        messages.warning(request, 'Ya tienes el máximo permitido de 5 unidades activas para este producto.')
        return redirect('productos')

    if total_apartado + cantidad > 5:
        disponibles_para_ti = 5 - total_apartado
        messages.warning(request, f'Solo puedes apartar {disponibles_para_ti} unidad(es) más de este producto hasta que tus apartados se entreguen, cancelen o expiren.')
        return redirect('productos')

    if producto.stock_disponible >= cantidad:
        Apartado.objects.create(
            usuario=request.user,
            producto=producto,
            cantidad=cantidad,
            fecha_expiracion=timezone.now() + timezone.timedelta(hours=24)
        )

        producto.stock_disponible -= cantidad
        producto.save()
        messages.success(request, f'Se apartaron correctamente {cantidad} unidad(es) de {producto.nombre}.')
    else:
        messages.error(request, 'No hay suficiente stock disponible para completar el apartado.')

    return redirect('productos')

def landing(request):
    ensure_initial_data()
    categorias = Categoria.objects.filter(activa=True)
    hero = HeroBanner.objects.filter(activo=True).order_by('-orden', '-fecha_actualizacion').first()
    return render(request, 'landing.html', {'categorias': categorias, 'hero': hero})


def productos(request):
    ensure_initial_data()
    categoria_seleccionada = request.GET.get('categoria', '').strip()
    disponibilidad = request.GET.get('disponibilidad', '').strip()
    orden = request.GET.get('orden', '').strip()
    precio_min = request.GET.get('precio_min', '').strip()
    precio_max = request.GET.get('precio_max', '').strip()

    productos = Producto.objects.all().select_related('categoria')

    if categoria_seleccionada:
        productos = productos.filter(categoria__nombre__iexact=categoria_seleccionada)

    if disponibilidad == 'disponibles':
        productos = productos.filter(stock_disponible__gt=0)
    elif disponibilidad == 'agotados':
        productos = productos.filter(stock_disponible__lte=0)

    if precio_min:
        try:
            productos = productos.filter(precio__gte=precio_min)
        except ValueError:
            pass

    if precio_max:
        try:
            productos = productos.filter(precio__lte=precio_max)
        except ValueError:
            pass

    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'recientes':
        productos = productos.order_by('-fecha_creacion')
    else:
        productos = productos.order_by('nombre')

    categorias = Categoria.objects.filter(activa=True)

    return render(
        request,
        'productos.html',
        {
            'productos': productos,
            'categorias': categorias,
            'categoria_seleccionada': categoria_seleccionada,
            'disponibilidad': disponibilidad,
            'orden': orden,
            'precio_min': precio_min,
            'precio_max': precio_max,
        },
    )

@login_required
def mis_apartados(request):
    apartados = Apartado.objects.filter(usuario=request.user).select_related('producto').order_by('-fecha_apartado')

    estados_activos = ['pendiente', 'confirmado']
    apartados_activos = apartados.filter(estado__in=estados_activos)
    productos_distintos_activos = len(set(apartados_activos.values_list('producto_id', flat=True)))
    total_unidades_activas = sum(apartados_activos.values_list('cantidad', flat=True))

    return render(
        request,
        'mis_apartados.html',
        {
            'apartados': apartados,
            'productos_distintos_activos': productos_distintos_activos,
            'total_unidades_activas': total_unidades_activas,
            'max_productos_distintos': 3,
            'max_unidades_por_producto': 5,
        },
    )


@login_required
def estado_apartados_api(request):
    apartados = (
        Apartado.objects.filter(usuario=request.user)
        .select_related('producto')
        .order_by('-fecha_apartado')[:6]
    )

    data = [
        {
            'id': apartado.id,
            'producto': apartado.producto.nombre,
            'cantidad': apartado.cantidad,
            'estado': apartado.estado,
            'estado_display': apartado.get_estado_display(),
            'fecha_apartado': timezone.localtime(apartado.fecha_apartado).strftime('%d/%m/%Y %H:%M'),
        }
        for apartado in apartados
    ]

    return JsonResponse({'apartados': data})


@login_required
def mi_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'actualizar_perfil':
            perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=usuario)
            password_form = CambioPasswordSemanalForm(usuario)
            eliminar_form = EliminarCuentaForm()

            if perfil_form.is_valid():
                perfil_form.save()
                messages.success(request, 'Tu perfil fue actualizado correctamente.')
                return redirect('mi_perfil')

        elif accion == 'cambiar_password':
            perfil_form = PerfilUsuarioForm(instance=usuario)
            password_form = CambioPasswordSemanalForm(usuario, request.POST)
            eliminar_form = EliminarCuentaForm()

            if password_form.is_valid():
                usuario = password_form.save()
                usuario.ultima_actualizacion_password = timezone.now()
                usuario.save(update_fields=['ultima_actualizacion_password'])
                update_session_auth_hash(request, usuario)
                messages.success(request, 'Tu contraseña se cambió correctamente.')
                return redirect('mi_perfil')

        elif accion == 'eliminar_cuenta':
            perfil_form = PerfilUsuarioForm(instance=usuario)
            password_form = CambioPasswordSemanalForm(usuario)
            eliminar_form = EliminarCuentaForm(request.POST)

            if eliminar_form.is_valid():
                if not usuario.check_password(eliminar_form.cleaned_data['password_actual']):
                    eliminar_form.add_error('password_actual', 'La contraseña actual no es correcta.')
                else:
                    logout(request)
                    usuario.delete()
                    return redirect('landing')
        else:
            perfil_form = PerfilUsuarioForm(instance=usuario)
            password_form = CambioPasswordSemanalForm(usuario)
            eliminar_form = EliminarCuentaForm()
    else:
        perfil_form = PerfilUsuarioForm(instance=usuario)
        password_form = CambioPasswordSemanalForm(usuario)
        eliminar_form = EliminarCuentaForm()

    return render(
        request,
        'mi_perfil.html',
        {
            'perfil_form': perfil_form,
            'password_form': password_form,
            'eliminar_form': eliminar_form,
        },
    )