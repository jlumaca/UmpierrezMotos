from django.contrib import admin
from django.urls import path
from AppUM import views

urlpatterns = [
     path('login', views.vista_login,name="Login"),
     path('login_validacion', views.validacion_login,name="LoginValidacion"),

     path('motos', views.vista_inventario_motos,name="Motos"),
     path('moto_alta', views.form_alta_moto,name="MotoAlta"),
     path('accesorios', views.vista_inventario_accesorios,name="Accesorios"),
]