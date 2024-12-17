from django.contrib import admin
from django.urls import path
from AppUM import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path('login/', views.acceso_login,name="Login"),
     path('cerrar_sesion', views.cerrar_sesion,name="CerrarSesion"),
     path('seleccion_rol', views.seleccion_rol,name="SeleccionRol"),
     path('cambio_pass', views.cambio_pass,name="CambioPass"),
     
     # path('login_validacion', views.validacion_login,name="LoginValidacion"),
     # path('login_validacion', views.prueba_login,name="LoginValidacion"),

     path('estadisticas', views.estadisticas,name="Estadisticas"),#

     path('motos', views.vista_inventario_motos,name="Motos"),#

     path('moto_alta', views.form_alta_moto,name="MotoAlta"),#
     path('cliente_moto', views.cliente_moto,name="BuscarClienteMoto"),#
     path('alta_moto_usada/<int:id_cliente>', views.alta_moto_usada,name="AltaMotoUsada"),#
     path('reingresar_moto_usada/<int:id_moto>/<int:id_cliente>', views.reingresar_moto_usada,name="ReingresarMotoUsada"),#
     path('alta_moto_nueva', views.alta_moto_nueva,name="AltaMotoNueva"),#



     path('moto_baja/<int:id_moto>', views.baja_moto,name="MotoBaja"),#
     # path('datos_cliente_moto', views.datos_cliente_venta,name="DatosClienteMoto"),#
     path('moto_modificacion/<int:id_moto>', views.modificacion_moto,name="MotoModificacion"),#
     
     
     
     

     path('moto_detalles/<int:id_moto>', views.detalles_moto,name="MotoDetalles"),

     path('busqueda_codigo', views.busqueda_codigo,name="BusquedaCodigo"),
     path('busqueda_marca', views.busqueda_marca,name="BusquedaMarca"),
     path('busqueda_modelo', views.busqueda_modelo,name="BusquedaModelo"),
     path('busqueda_marca_modelo', views.busqueda_marca_modelo,name="BusquedaMarcaModelo"),
     path('busqueda_anio', views.busqueda_anio,name="BusquedaAnio"),
     path('busqueda_kms', views.busqueda_kms,name="BusquedaKms"),
     path('busqueda_precio', views.busqueda_precio,name="BusquedaPrecio"),
     path('busqueda_matricula', views.busqueda_matricula,name="BusquedaMatricula"),
     path('busqueda_tipo', views.busqueda_tipo_moto,name="BusquedaTipoMoto"),

     
     path('accesorios', views.vista_inventario_accesorios,name="Accesorios"),
     path('accesorio_alta', views.alta_accesorio,name="AccesorioAlta"),
     #path('datos_accesorio_modificacion/<int:id_accesorio>', views.datos_a_modificacion_accesorio,name="DatosAccesorioModificacion"),
     path('accesorio_modificacion/<int:id_accesorio>', views.modificacion_accesorio,name="AccesorioModificacion"),
     path('accesorio_baja/<int:id_accesorio>', views.baja_accesorio,name="AccesorioBaja"),
     path('accesorio_detalle/<int:id_accesorio>', views.detalles_accesorio,name="AccesorioDetalle"),
     path('accesorio_venta/<int:id_accesorio>/<int:id_cliente>', views.venta_accesorio,name="AccesorioVenta"),
     path('cliente_accesorio_venta/<int:id_accesorio>', views.cliente_venta_accesorio,name="ClienteAccesorioVenta"),

     path('busqueda_marca_modelo_accesorio', views.busqueda_marca_modelo_accesorio,name="BusquedaMarcaModeloAccesorio"),
     path('busqueda_tipo_accesorio', views.busqueda_tipo_accesorio,name="BusquedaTipoAccesorio"),
     path('busqueda_codigo_accesorio', views.busqueda_codigo_accesorio,name="BusquedaCodigoAccesorio"),

     path('clientes', views.vista_clientes,name="Clientes"),
     path('cliente_alta', views.alta_cliente,name="ClienteAlta"),
     path('cliente_modificacion/<int:id_cliente>', views.modificacion_cliente,name="ClienteModificacion"),
     path('busqueda_documento', views.buscar_por_doc,name="BusquedaDocumento"),
     path('busqueda_nombre_apellido', views.buscar_nom_ape,name="BusquedaNombreApellido"),
     path('cargar_certificado/<int:id_cv>', views.cargar_certificado,name="CargarCertificado"),
     path('cargar_libreta/<int:id_cv>', views.cargar_libreta,name="CargarLibreta"),


     path('personal', views.vista_personal,name="Personal"),
     path('personal_alta', views.alta_personal,name="PersonalAlta"),
     path('personal_detalle/<int:id_personal>', views.detalles_personal,name="PersonalDetalle"),

     path('reingresar_tienda/<int:id_personal>', views.ingresar_tienda,name="ReingresarTienda"),
     


     path('ventas', views.vista_ventas,name="Ventas"),
     # path('alta_cuota/<int:id_cv>', views.alta_cuota,name="AltaCuota"),
     
     

     path('tienda', views.datos_tienda,name="Tienda"),
     path('precio_dolar', views.modificar_precio_dolar,name="ModificarPrecioDolar"),
     path('modificar_logo', views.modificar_logo_tienda,name="ModificarLogo"),
     path('modificar_logo_cv', views.modificar_logo_cv,name="ModificarLogoCV"),

     path('arqueos', views.arqueos,name="Arqueos"),
     path('abrir_caja', views.abrir_caja,name="AbrirCaja"),
     path('ingresos_caja/<int:id_caja>', views.ingresos_caja,name="IngresosCaja"),
     path('egresos_caja/<int:id_caja>', views.egresos_caja,name="EgresosCaja"),
     path('saldo_caja_final/<int:id_caja>', views.saldo_final_caja,name="SaldoFinalCaja"),
     path('cerrar_caja/<int:id_caja>', views.cerrar_caja,name="CerrarCaja"),
     path('movimientos_caja/<int:id_caja>', views.movimientos_caja,name="MovimientosCaja"),
     path('notificaciones_administrativo', views.notificaciones_administrativo,name="NotificacionesAdministrativo"),     
     path('cliente_ficha/<int:id_cliente>', views.ficha_cliente,name="ClienteFicha"),
     path('detalles_compra_accesorio/<int:id_venta>', views.pagos_accesorio,name="DetallesCompraAccesorio"),
     path('alta_paga_accesorio/<int:id_venta>', views.alta_paga_accesorio,name="AltaPagoAccesorio"),
     path('baja_paga_accesorio/<int:id_ca>', views.baja_paga_accesorio,name="BajaPagoAccesorio"),

     
     path('servicios_en_gestion', views.servicios_en_gestion,name="ServiciosEnGestion"),
     path('form_alta_servicio', views.form_alta_servicio,name="FormAltaServicio"),
     path('cliente_moto_servicio', views.cliente_moto_servicio,name="ClienteMotoServicio"),
     path('alta_servicio/<int:id_moto>/<int:id_cliente>', views.alta_servicio,name="AltaServicio"),
     path('historial_de_servicios', views.historial_de_servicios,name="HistorialDeServicios"),















     path('editar_usuario', views.editar_usuario,name="EditarUsuario"),
     path('editar_pass_usuario', views.editar_password,name="EditarPassUsuario"),
     path('moto_venta_form/<int:id_moto>', views.form_venta_moto,name="MotoVentaForm"),#SOLO RENDERIZA FORM Y DATOS
     path('detalles_cuotas/<int:id_cv>', views.detalles_cuotas,name="DetallesCuotas"),
     path('moto_venta/<int:id_moto>/<int:id_cliente>', views.venta_moto,name="MotoVenta"),#
     path('pago_por_ref/', views.buscar_pagos_por_refinanciamiento,name="PagoPorRef"),
     path('reservas', views.reservas,name="Reservas"),
     path('moto_reserva_form/<int:id_moto>', views.form_reservar_moto,name="MotoReservaForm"),
     path('moto_reserva/<int:id_moto>/<int:id_cliente>', views.reservar_moto,name="MotoReserva"),
     path('alta_pago/<int:id_cv>', views.alta_pago,name="AltaPago"),
     path('baja_pago/<int:id_cm>', views.baja_pago,name="BajaPago"),
     path('refinanciar/<int:id_cv>', views.refinanciar_pagos,name="Refinanciar"),
     path('pago_cuota/<int:id_cv>', views.alta_pago_cuota,name="PagoCuotas"),
     path('baja_financiamiento/<int:id_f>/<int:id_cv>', views.baja_financiamiento,name="BajaFinanciamiento"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)