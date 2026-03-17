from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Usuario
from .forms import LoginFormulario, RegistroUsuarioForm


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