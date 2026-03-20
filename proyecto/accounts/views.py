from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Venta, Producto, Compra
from .forms import LoginFormulario, RegistroUsuarioForm, NuevaVentaForm, NuevoCompraForm, NuevoProductoFrom


# Create your views here.

def home(request):
    return render(request, "accounts/home.html")


def loginformulario(request):

    if request.method == "POST":
        form = LoginFormulario(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, "accounts/login.html", {
                    "form": form,
                    "error": "Usuario no encontrado"
                })

            user = authenticate(request, username=user.username, password=password)

            
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)

                # 👇 REDIRECCIÓN SI TODO ES CORRECTO
            return redirect("general")

        else:
            return render(request, "accounts/login.html", {
                "form": form,
                "error": "Contraseña incorrecta"
            })

    else:
        form = LoginFormulario()

    return render(request, "accounts/login.html", {"form": form})

def register(request):

    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = RegistroUsuarioForm()

    return render(request, "accounts/register.html", {"form": form})
        
def general(request):
    return render(request, "accounts/general.html")


def ventas_geral(request):
    return render(request, "accounts/ventas_geral.html")


def institucionales(request):
    return render(request, "accounts/institucionales.html")

def instagram(request):
    return render(request, "accounts/instagram.html")

def nosotros(request):
    return render(request,"accounts/nosotros.html")

def pedidosprov(request):
    return render(request,"accounts/pedidosprov.html")

def producto(request):
    mensaje_error = None

    if request.method == "POST":
        form = NuevoProductoFrom(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']

            # 🔥 BUSCAR SI EXISTE
            producto_obj, creado = Producto.objects.get_or_create(
                producto=nombre,
                defaults={'cantidad': cantidad}
            )

            if not creado:
                # 🔥 SI YA EXISTE → SUMA STOCK
                producto_obj.cantidad += cantidad
                producto_obj.save()

            return redirect('stock')
    else:
        form = NuevoProductoFrom()

    productos = Producto.objects.all()

    return render(request, "accounts/stock.html", {
        "form": form,
        "productos": productos,
        "error": mensaje_error
    })

def compra(request):
    if request.method == "POST":
        form = NuevoCompraForm(request.POST)
        if form.is_valid():
            producto_obj = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            fecha = form.cleaned_data['fecha']
                
            Compra.objects.create(
                producto=producto_obj,
                cantidad=cantidad,
                fecha=fecha
            )

            # 🔥 SUMA STOCK
            producto_obj.cantidad += cantidad
            producto_obj.save()

            return redirect('productos')
    else:
        form = NuevoCompraForm()

    compras = Compra.objects.all()

    return render(request, "accounts/productos.html", {
        "form": form,
        "compras": compras
    })

def ventas_geral(request):
    mensaje_error = None

    if request.method == "POST":
        form = NuevaVentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            fecha = form.cleaned_data['fecha']

            # 🔥 VALIDACIÓN DE STOCK
            if producto.cantidad >= cantidad:
                Venta.objects.create(
                    producto=producto,
                    cantidad=cantidad,
                    fecha = fecha,
                )

                # 🔥 DESCUENTA STOCK
                producto.cantidad -= cantidad
                producto.save()

            return redirect('ventas_geral')
        else:
                mensaje_error = "No hay suficiente stock"
    else:
        form = NuevaVentaForm()

    ventas = Venta.objects.all()

    return render(request, "accounts/ventas_geral.html", {
        "form": form,
        "ventas": ventas,
        "error": mensaje_error
    })
