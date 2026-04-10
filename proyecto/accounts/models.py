from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username
    
class edit_users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Producto(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    
    class Unidad(models.TextChoices):
        UNIDAD = "unidad", "Unidad"
        CAJA = "caja", "Caja"
        METRO = "metro", "Metro"

    unidad = models.CharField(max_length=20, choices=Unidad.choices)

    def __str__(self):
        return self.producto

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.producto}"

class Venta(models.Model):
    fecha = models.DateField(default=timezone.now)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto}"   
    
class PedidosProv(models.Model):
    fecha_pedido = models.DateField(default=timezone.now)
    producto_pedido_new = models.CharField(null=True, blank=True)
    producto_pedido_existente = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad_pedida = models.IntegerField()
    email = models.EmailField()
    tipo= models.CharField(max_length=20)

class NuevosProveedores(models.Model):
    nombre = models.CharField()
    email = models.EmailField()
    telefono = models.IntegerField()

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatares', null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.image}"