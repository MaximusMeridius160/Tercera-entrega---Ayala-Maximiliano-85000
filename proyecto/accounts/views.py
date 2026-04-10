from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Venta, Producto, Compra, PedidosProv, NuevosProveedores
from .forms import *
from .graph import *


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
    return render(request, "accounts/general.html",{"grafico": grafico_pedidos(),"grafico2":grafico_ventas})


def ventas_geral(request):
    return render(request, "accounts/ventas_geral.html")


def institucionales(request):
    return render(request, "accounts/institucionales.html")

def instagram(request):
    return render(request, "accounts/instagram.html")

def nosotros(request):
    return render(request,"accounts/nosotros.html")

def agregarproveedor(request):
    mensaje_error = None

    if request.method == "POST":
        form = NuevoProveedor(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']

            NuevosProveedores.objects.create(
                nombre = nombre,
                email = email,
                telefono = telefono
            )

            return redirect ('agregarproveedor')

    else:
        form = NuevoProveedor()
    
    proveedores = NuevosProveedores.objects.all()

    return render(request,"accounts/agregarproveedor.html", {
        "form": form,
        "proveedores": proveedores,
        "error": mensaje_error
    })

def pedidosprov(request):
    mensaje_error = None
    tipo = None

    if request.method == "POST":
        tipo = request.POST.get("tipo")

        if tipo == "nuevo":
            form = PedidoNuevoForm(request.POST)
        elif tipo == "existente":
            form = PedidoExistenteForm(request.POST)
        else:
            form = PedidoNuevoForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            PedidosProv.objects.create(
                fecha_pedido=data.get("fecha_pedido"),
                producto_pedido_new=data.get("producto_pedido_new"),
                producto_pedido_existente=data.get("producto_pedido_existente"),
                cantidad_pedida=data.get("cantidad_pedida"),
                email=data.get("email"),
                tipo=tipo
            )

            return redirect('pedidosprov')
    
    form_nuevo = PedidoNuevoForm()
    form_existente = PedidoExistenteForm()
        

    pedidos_nuevos = PedidosProv.objects.filter(tipo="nuevo")
    pedidos_existentes = PedidosProv.objects.filter(tipo="existente")

    return render(request, "accounts/pedidosprov.html", {
        "form_nuevo": form_nuevo,
        "form_existente": form_existente,
        "pedidos_nuevos": pedidos_nuevos,
        "pedidos_existentes": pedidos_existentes,
        "tipo": tipo,
        "error": mensaje_error
    })


def producto(request):
    mensaje_error = None

    if request.method == "POST":
        form = NuevoProductoFrom(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            unidad = form.cleaned_data['unidad']

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

@login_required
def user_profile(request):

    avatar, creado = Avatar.objects.get_or_create(user=request.user)

    if request.method == 'POST':

        # 👉 FORM USUARIO
        if 'guardar_usuario' in request.POST:
            form_user = EditProfileForm(request.POST, instance=request.user)
            form_avatar = AvatarForm(instance=avatar)

            if form_user.is_valid():
                form_user.save()
                return redirect('user_profile')

        # 👉 FORM AVATAR
        elif 'guardar_avatar' in request.POST:
            form_user = EditProfileForm(instance=request.user)
            form_avatar = AvatarForm(request.POST, request.FILES, instance=avatar)

            if form_avatar.is_valid():
                form_avatar.save()
                return redirect('user_profile')

        else:
            form_user = EditProfileForm(instance=request.user)
            form_avatar = AvatarForm(instance=avatar)

    else:
        form_user = EditProfileForm(instance=request.user)
        form_avatar = AvatarForm(instance=avatar)

    return render(request, "accounts/user_profile.html", {
        'form_user': form_user,
        'form_avatar': form_avatar
    })

def cerrar_sesion(request):
    logout(request)
    return redirect('login')  # o donde quieras redirigir