from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Compra, Producto, Venta, PedidosProv,NuevosProveedores


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = "Perfil"
    fk_name = "user"  # 🔥 importante


class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioInline,)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'telefono'),
        }),
    )

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "get_telefono",
    )

    def get_telefono(self, obj):
        if hasattr(obj, 'usuario'):
            return obj.usuario.telefono
        return "-"
    get_telefono.short_description = "Teléfono"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Compra)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("fecha", "producto", "cantidad")

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad")

@admin.register(Venta)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("fecha", "producto", "cantidad")


@admin.register(PedidosProv)
class PedidosAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_pedido",
        "producto_pedido_new",
        "producto_pedido_existente",
        "cantidad_pedida",
        "tipo",
        "email"
    )
    
@admin.register(NuevosProveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "telefono",
        "email"
    )