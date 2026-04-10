from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginFormulario(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistroUsuarioForm(UserCreationForm):    
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        help_texts = {
            'username': '',
        }
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['image']

class NuevoProductoFrom(forms.Form):
    producto = forms.CharField(required=True)
    cantidad = forms.IntegerField(required=True)
    unidad = forms.ChoiceField(required=True, choices=Producto.Unidad.choices)

class NuevaVentaForm(forms.Form):
    fecha = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(min_value=1,required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()

class NuevoCompraForm(forms.Form):
    fecha = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(required=True)


class NuevoProveedor(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    telefono = forms.IntegerField()

class PedidoExistenteForm(forms.Form):
    fecha_pedido = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    producto_pedido_existente = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad_pedida = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad'}))
    email = forms.EmailField()


class PedidoNuevoForm(forms.Form):
    fecha_pedido = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    producto_pedido_new = forms.CharField()
    cantidad_pedida = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese la cantidad'}))
    email = forms.EmailField() 
