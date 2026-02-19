from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, Apartado
from .forms import RegistroForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})


@login_required
def apartar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.estado == 'disponible':
        Apartado.objects.create(
            usuario=request.user,
            producto=producto
        )
        producto.estado = 'reservado'
        producto.save()

    return redirect('home')
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

