from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Producto, Venta
from .forms import LoginFormulario, RegistroUsuarioForm, NuevaVentaForm, NuevoProductoForm


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

def nosotros(request):
    return render(request,"accounts/nosotros.html")

def pedidosprov(request):
    return render(request,"accounts/pedidosprov.html")

def productos(request):
    if request.method == "POST":
        form = NuevoProductoForm(request.POST)
        if form.is_valid():
            Producto.objects.create(
                producto=form.cleaned_data['producto'],
                cantidad=form.cleaned_data['cantidad']
            )
            return redirect('productos')  # recarga la página
    else:
        form = NuevoProductoForm()

    lista_productos = Producto.objects.all()

    return render(request, "accounts/productos.html", {
        "form": form,
        "productos": lista_productos
    })

def ventas(request):
    mensaje_error = None

    if request.method == "POST":
        form = NuevaVentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']

            # 🔥 VALIDACIÓN DE STOCK
            if producto.stock >= cantidad:
                Venta.objects.create(
                    producto=producto,
                    cantidad=cantidad
                )

                # 🔥 DESCUENTA STOCK
                producto.stock -= cantidad
                producto.save()

            return redirect('ventas')
        else:
                mensaje_error = "No hay suficiente stock"
    else:
        form = NuevaVentaForm()

    ventas = Venta.objects.all()

    return render(request, "ventas_geral.html", {
        "form": form,
        "ventas": ventas,
        "error": mensaje_error
    })