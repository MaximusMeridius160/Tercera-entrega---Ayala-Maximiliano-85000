"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name= "home"),
    path('login/', views.loginformulario, name= "login"),
    path('register/', views.register, name= "register"),
    path('general/', views.general, name= "general"),
    path('ventas_gral/', views.ventas_geral, name= "ventas_geral"),
    path('institucionales/',views.institucionales, name= "institucionales"),
    path('nosotros/',views.nosotros, name= "nosotros"),
    path('pedidosprov/',views.pedidosprov, name= "pedidosprov"),
    path('productos/',views.compra, name= "productos"),
    path('instagram/',views.instagram, name= "instagram"),
    path('stock/',views.producto, name= "stock"),
    path('agregarproveedor/',views.agregarproveedor, name="agregarproveedor"),
    path('user_profile/',views.user_profile, name="user_profile"),
    path('logout/', views.cerrar_sesion, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)