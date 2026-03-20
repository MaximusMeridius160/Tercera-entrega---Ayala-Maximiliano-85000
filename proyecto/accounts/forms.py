from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Producto, Compra

class LoginFormulario(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistroUsuarioForm(UserCreationForm):    
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NuevoProductoFrom(forms.Form):
    producto = forms.CharField(required=True)
    cantidad = forms.IntegerField(required=True)

class NuevaVentaForm(forms.Form):
    fecha = forms.DateField(required=True)
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(min_value=1,required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()

class NuevoCompraForm(forms.Form):
    fecha = forms.DateField(required=True)
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(required=True)

    
