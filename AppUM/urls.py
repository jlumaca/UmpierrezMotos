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
     path('datos_cliente_moto', views.datos_cliente_venta,name="DatosClienteMoto"),
     path('moto_modificacion/<int:id_moto>', views.modificacion_moto,name="MotoModificacion"),

     path('moto_detalles/<int:id_moto>', views.detalles_moto,name="MotoDetalles"),

     path('busqueda_codigo', views.busqueda_codigo,name="BusquedaCodigo"),
     path('busqueda_marca', views.busqueda_marca,name="BusquedaMarca"),
     path('busqueda_modelo', views.busqueda_modelo,name="BusquedaModelo"),
     path('busqueda_marca_modelo', views.busqueda_marca_modelo,name="BusquedaMarcaModelo"),
     path('busqueda_anio', views.busqueda_anio,name="BusquedaAnio"),
     path('busqueda_kms', views.busqueda_kms,name="BusquedaKms"),
     path('busqueda_precio', views.busqueda_precio,name="BusquedaPrecio"),
     path('busqueda_matricula', views.busqueda_matricula,name="BusquedaMatricula"),

     
     path('accesorios', views.vista_inventario_accesorios,name="Accesorios"),
     path('accesorio_alta', views.alta_accesorio,name="AccesorioAlta"),
     #path('datos_accesorio_modificacion/<int:id_accesorio>', views.datos_a_modificacion_accesorio,name="DatosAccesorioModificacion"),
     path('accesorio_modificacion/<int:id_accesorio>', views.modificacion_accesorio,name="AccesorioModificacion"),
     path('accesorio_baja/<int:id_accesorio>', views.baja_accesorio,name="AccesorioBaja"),
     path('accesorio_detalle/<int:id_accesorio>', views.detalles_accesorio,name="AccesorioDetalle"),

     path('busqueda_marca_modelo_accesorio', views.busqueda_marca_modelo_accesorio,name="BusquedaMarcaModeloAccesorio"),
     path('busqueda_tipo_accesorio', views.busqueda_tipo_accesorio,name="BusquedaTipoAccesorio"),

     path('clientes', views.vista_clientes,name="Clientes"),
     path('cliente_alta', views.alta_cliente,name="ClienteAlta"),
     path('cliente_modificacion/<int:id_cliente>', views.modificacion_cliente,name="ClienteModificacion"),
     path('busqueda_documento', views.buscar_por_doc,name="BusquedaDocumento"),
     path('busqueda_nombre_apellido', views.buscar_nom_ape,name="BusquedaNombreApellido"),
     path('cliente_ficha/<int:id_cliente>', views.ficha_cliente,name="ClienteFicha"),


     path('personal', views.vista_personal,name="Personal"),
     path('personal_alta', views.alta_personal,name="PersonalAlta"),
     path('personal_detalle/<int:id_personal>', views.detalles_personal,name="PersonalDetalle"),
     

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)