from django.contrib import admin
from django.urls import path
from AppUM import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path('login', views.vista_login,name="Login"),
     path('login_validacion', views.validacion_login,name="LoginValidacion"),

     path('motos', views.vista_inventario_motos,name="Motos"),
     path('moto_alta', views.form_alta_moto,name="MotoAlta"),
     path('moto_baja/<int:id_moto>', views.baja_moto,name="MotoBaja"),
     path('accesorios', views.vista_inventario_accesorios,name="Accesorios"),


     

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)