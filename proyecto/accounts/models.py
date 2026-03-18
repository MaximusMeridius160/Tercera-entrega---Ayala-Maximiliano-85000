from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def crear_usuario(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_usuario(sender, instance, **kwargs):
    if hasattr(instance, 'usuario'):
        instance.usuario.save()

class Producto(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return self.producto
    

class Venta(models.Model):
    fecha = models.DateField(default=timezone.now)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto} - {self.cantidad}"