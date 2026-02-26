from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Producto, Apartado
from .forms import RegistroForm


def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def apartar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad > 5:
        return redirect('home')

    if producto.stock_disponible >= cantidad:
        Apartado.objects.create(
            usuario=request.user,
            producto=producto,
            cantidad=cantidad,
            fecha_expiracion=timezone.now() + timezone.timedelta(hours=24)
        )

        producto.stock_disponible -= cantidad
        producto.save()

    return redirect('home')