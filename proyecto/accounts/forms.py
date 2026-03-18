from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class LoginFormulario(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistroUsuarioForm(UserCreationForm):    
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NuevaVentaForm(forms.Form):
    producto = forms.CharField()
    cantidad = forms.IntegerField()


class NuevoProductoForm(forms.Form):
    fechacompra = forms.DateField(required=True)
    producto = forms.CharField(required=True)
    cantidad = forms.IntegerField(required=True)