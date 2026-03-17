from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


# Inline para el perfil
class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = "Perfil"


# Extender el admin de User (IMPORTANTE usar UserAdmin)
class CustomUserAdmin(UserAdmin):
    inlines = (UsuarioInline,)

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "get_telefono",
    )

    def get_telefono(self, obj):
        return obj.usuario.telefono if hasattr(obj, 'usuario') else ""
    get_telefono.short_description = "Teléfono"


# Reemplazar el admin original
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)