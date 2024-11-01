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
     #path('datos_moto_modificacion/<int:id_moto>', views.datos_a_modificacion_moto,name="DatosMotoModificacion"),
     path('moto_modificacion/<int:id_moto>', views.modificacion_moto,name="MotoModificacion"),

     path('moto_detalles/<int:id_moto>', views.detalles_moto,name="MotoDetalles"),

     path('busqueda_codigo', views.busqueda_codigo,name="BusquedaCodigo"),
     path('busqueda_marca', views.busqueda_marca,name="BusquedaMarca"),
     path('busqueda_modelo', views.busqueda_modelo,name="BusquedaModelo"),
     path('busqueda_marca_modelo', views.busqueda_marca_modelo,name="BusquedaMarcaModelo"),
     path('busqueda_anio', views.busqueda_anio,name="BusquedaAnio"),
     path('busqueda_kms', views.busqueda_kms,name="BusquedaKms"),
     path('busqueda_precio', views.busqueda_precio,name="BusquedaPrecio"),

     
     path('accesorios', views.vista_inventario_accesorios,name="Accesorios"),
     path('accesorio_alta', views.alta_accesorio,name="AccesorioAlta"),
     #path('datos_accesorio_modificacion/<int:id_accesorio>', views.datos_a_modificacion_accesorio,name="DatosAccesorioModificacion"),
     path('accesorio_modificacion/<int:id_accesorio>', views.modificacion_accesorio,name="AccesorioModificacion"),
     path('accesorio_baja/<int:id_accesorio>', views.baja_accesorio,name="AccesorioBaja"),
     path('accesorio_detalle/<int:id_accesorio>', views.detalles_accesorio,name="AccesorioDetalle"),

     

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)