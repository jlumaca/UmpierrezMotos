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
     # path('generar_compromiso_compra_venta_moto_ingreso/<int:id_cliente>', views.generar_compromiso_compra_venta_moto_ingreso,name="GCCVMI"),
     path('cliente_moto', views.cliente_moto,name="BuscarClienteMoto"),#
     path('alta_moto_usada/<int:id_cliente>', views.alta_moto_usada,name="AltaMotoUsada"),#
     path('reingresar_moto_usada/<int:id_moto>/<int:id_cliente>', views.reingresar_moto_usada,name="ReingresarMotoUsada"),#
     path('alta_moto_nueva', views.alta_moto_nueva,name="AltaMotoNueva"),#
     path('alta_moto_usada_sin_dueno', views.alta_moto_usada_sin_dueno,name="AltaMotoUsadaSinDueno"),#



     path('moto_baja/<int:id_moto>', views.baja_moto,name="MotoBaja"),#
     # path('datos_cliente_moto', views.datos_cliente_venta,name="DatosClienteMoto"),#
     path('moto_modificacion/<int:id_moto>', views.modificacion_moto,name="MotoModificacion"),#
     path('form_cambio_duenio/<int:id_moto>', views.form_cambio_propietario_moto,name="FormCambioDuenio"),
     path('cambio_duenio/<int:id_moto>/<int:id_cliente>', views.cambio_duenio_moto,name="CambioDuenio"),
     
     
     
     

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
     path('busqueda_num_motor', views.busqueda_num_motor,name="BusquedaNumMotor"),
     path('busqueda_num_chasis', views.busqueda_num_chasis,name="BusquedaNumChasis"),

     
     path('accesorios', views.vista_inventario_accesorios,name="Accesorios"),
     path('seleccionar_accesorio/<int:id_accesorio>', views.seleccionar_accesorio,name="SeleccionarAccesorio"),
     path('borrar_seleccion_accesorio/<int:id_accesorio>', views.borrar_seleccion_accesorio,name="BorrarSeleccionAccesorio"),
     path('accesorio_alta', views.alta_accesorio,name="AccesorioAlta"),
     #path('datos_accesorio_modificacion/<int:id_accesorio>', views.datos_a_modificacion_accesorio,name="DatosAccesorioModificacion"),
     path('accesorio_modificacion/<int:id_accesorio>', views.modificacion_accesorio,name="AccesorioModificacion"),
     path('accesorio_baja/<int:id_accesorio>', views.baja_accesorio,name="AccesorioBaja"),
     path('accesorio_detalle/<int:id_accesorio>', views.detalles_accesorio,name="AccesorioDetalle"),
     path('accesorio_venta/<int:id_cliente>', views.venta_accesorio,name="AccesorioVenta"),
     path('cliente_accesorio_venta/<int:mostrar>/<int:vender>', views.cliente_venta_accesorio,name="ClienteAccesorioVenta"),
     path('prueba_cliente_accesorio_venta', views.prueba_varios_accesorios,name="PruebaVariosAccesorios"),


     path('busqueda_marca_modelo_accesorio', views.busqueda_marca_modelo_accesorio,name="BusquedaMarcaModeloAccesorio"),
     path('busqueda_tipo_accesorio', views.busqueda_tipo_accesorio,name="BusquedaTipoAccesorio"),
     path('busqueda_codigo_accesorio', views.busqueda_codigo_accesorio,name="BusquedaCodigoAccesorio"),

     path('clientes', views.vista_clientes,name="Clientes"),
     path('cliente_alta', views.alta_cliente,name="ClienteAlta"),
     path('cliente_modificacion/<int:id_cliente>', views.modificacion_cliente,name="ClienteModificacion"),
     path('empresa_alta', views.alta_empresa,name="EmpresaAlta"),
     path('empresa_modificacion/<int:id_cliente>', views.modificacion_empresa,name="EmpresaModificacion"),
     path('busqueda_documento', views.buscar_por_doc,name="BusquedaDocumento"),
     path('busqueda_nombre_apellido', views.buscar_nom_ape,name="BusquedaNombreApellido"),
     path('busqueda_rut', views.buscar_por_rut,name="BusquedaRUT"),
     path('busqueda_nombre_empresa', views.buscar_nom_emp,name="BusquedaNombreEmpresa"),
     
     path('cargar_certificado/<int:id_cv>', views.cargar_certificado,name="CargarCertificado"),
     path('cargar_libreta/<int:id_cv>', views.cargar_libreta,name="CargarLibreta"),
     path('cargar_factura/<int:id_cv>', views.cargar_factura,name="CargarFactura"),
     path('generar_ccv/<int:id_moto>/<int:id_cliente>', views.generar_compromiso_compra_venta,name="GenerarCCV"),
     path('generar_ccv_ma/<int:id_moto>/<int:id_cliente>', views.generar_compromiso_compra_venta_moto_ingreso,name="GenerarCCVMA"),
     path('cargar_ccv/<int:id_cv>', views.cargar_ccv,name="CargarCCV"),
     path('cargar_ccv_ma/<int:id_cv>/<int:id_moto>', views.cargar_ccv_ma,name="CargarCCVMA"),

     path('borrar_documentacion/<int:id_cv>/<str:tipo>', views.borrar_documentacion,name="BorrarDocumentacion"),

     #generar_compromiso_compra_venta(req,id_moto,id_cliente)


     path('personal', views.vista_personal,name="Personal"),
     path('personal_alta', views.alta_personal,name="PersonalAlta"),
     path('personal_detalle/<int:id_personal>', views.detalles_personal,name="PersonalDetalle"),
     path('personal_baja/<str:donde>/<int:id_personal>', views.baja_personal,name="PersonalBaja"),

     path('reingresar_tienda/<int:id_personal>', views.ingresar_tienda,name="ReingresarTienda"),
     


     path('ventas', views.vista_ventas,name="Ventas"),
     path('venta_cliente', views.buscar_venta_cliente,name="VentasCliente"),
     path('venta_fecha', views.buscar_venta_fecha,name="VentasFecha"),
     path('venta_marca_modelo_moto', views.buscar_venta_marca_modelo_moto,name="VentaMoto"),
     path('venta_x_accesorio', views.buscar_venta_accesorio,name="VentaAccesorio"),
     path('venta_x_num_motor', views.buscar_venta_num_motor_moto,name="VentaNumMotor"),
     path('venta_x_num_chasis', views.buscar_venta_num_chasis_moto,name="VentaNumChasis"),
     # path('alta_cuota/<int:id_cv>', views.alta_cuota,name="AltaCuota"),buscar_venta_marca_modelo_moto
     
     

     path('tienda', views.datos_tienda,name="Tienda"),
     path('precio_dolar', views.modificar_precio_dolar,name="ModificarPrecioDolar"),
     path('modificar_logo', views.modificar_logo_tienda,name="ModificarLogo"),
     path('modificar_logo_cv', views.modificar_logo_cv,name="ModificarLogoCV"),

     path('arqueos', views.arqueos,name="Arqueos"),
     path('apertura', views.buscar_x_fecha_apertura,name="ArqueosFechaApertura"),
     path('cierre', views.buscar_x_fecha_cierre,name="ArqueosFechaCierre"),
     path('abrir_caja', views.abrir_caja,name="AbrirCaja"),
     path('ingresos_caja/<int:id_caja>', views.ingresos_caja,name="IngresosCaja"),
     path('egresos_caja/<int:id_caja>', views.egresos_caja,name="EgresosCaja"),
     path('saldo_caja_final/<int:id_caja>', views.saldo_final_caja,name="SaldoFinalCaja"),
     path('cerrar_caja/<int:id_caja>', views.cerrar_caja,name="CerrarCaja"),
     path('movimientos_caja/<int:id_caja>', views.movimientos_caja,name="MovimientosCaja"),
      path('editar_monto_inicial/<int:id_caja>', views.editar_saldo_inicial,name="EditarMontoInicial"),

     path('movimiento_baja/<int:id_caja>/<int:id_movimiento>', views.baja_movimiento,name="MovimientoBaja"),
     path('detalles_caja_x_fecha/', views.buscar_detalles_movimientos_x_fecha,name="DetallesCajaXFecha"),
     path('detalles_caja_x_fecha_excel/', views.buscar_detalles_movimientos_x_fecha_excel,name="DetallesCajaXFechaExcel"),


     path('detalles_caja_x_mes_anio/', views.buscar_detalles_movimientos_x_mes_anio,name="DetallesCajaXMesAnio"),
     path('detalles_caja_x_mes_anio_excel/', views.buscar_detalles_movimientos_x_mes_anio_excel,name="DetallesCajaXMesAnioExcel"),

     path('nuevo_rubro/<int:id_caja>', views.nuevo_rubro_egreso,name="NuevoRubro"),
     
     
     
     path('notificaciones_administrativo', views.notificaciones_administrativo,name="NotificacionesAdministrativo"),
     path('borrar_notificaciones_administrativo/<int:id_notificacion>', views.borrar_notificacion_tienda,name="BorrarNotificacionesAdministrativo"),     
          
     path('cliente_ficha/<int:id_cliente>', views.ficha_cliente,name="ClienteFicha"),
     path('fondos_cliente/<int:id_cliente>', views.fondos_cliente,name="FondosCliente"),
     path('modificar_moto_vendida/<int:id_moto>/<int:id_cliente>', views.modificar_moto_vendida,name="ModificarMotoVendida"),
     path('modificar_accesorio_vendido/<int:id_accesorio>/<int:id_cliente>', views.modificar_accesorio_vendido,name="ModificarAccesorioVendido"),
     path('baja_accesorio_vendido/<int:codigo_compra>/<int:id_accesorio>', views.borrar_accesorio_vendido,name="BorrarAccesorioVendido"),


      path('calculadora', views.calculadora_pagos,name="Calculadora"),

     path('detalles_compra_accesorio/<int:codigo_compra>', views.pagos_accesorio,name="DetallesCompraAccesorio"),
     path('alta_paga_accesorio/<int:id_venta>', views.alta_paga_accesorio,name="AltaPagoAccesorio"),
     path('baja_paga_accesorio/<int:id_ca>', views.baja_paga_accesorio,name="BajaPagoAccesorio"),

     
     path('servicios_en_gestion', views.servicios_en_gestion,name="ServiciosEnGestion"),
     path('form_alta_servicio', views.form_alta_servicio,name="FormAltaServicio"),
     path('cliente_moto_servicio', views.cliente_moto_servicio,name="ClienteMotoServicio"),
     path('alta_servicio/<int:id_moto>/<int:id_cliente>', views.alta_servicio,name="AltaServicio"),
     path('historial_de_servicios', views.historial_de_servicios,name="HistorialDeServicios"),














     path('baja_pago/<int:id_cm>', views.baja_primeros_pagos,name="BajaPrimerosPagos"),
     path('editar_usuario', views.editar_usuario,name="EditarUsuario"),
     path('editar_pass_usuario', views.editar_password,name="EditarPassUsuario"),
     path('editar_pass_usuario/<int:id_u>', views.resetear_usuario,name="ResetearUsuario"),
     path('moto_venta_form/<int:id_moto>', views.form_venta_moto,name="MotoVentaForm"),#SOLO RENDERIZA FORM Y DATOS
     path('detalles_cuotas/<int:id_cv>', views.detalles_cuotas,name="DetallesCuotas"),
     path('moto_venta/<int:id_moto>/<int:id_cliente>', views.venta_moto,name="MotoVenta"),#
     path('baja_moto_vendida/<int:id_venta>', views.baja_venta_moto,name="BajaMotoVendida"),#
     path('generar_compromiso_compra_venta/<int:id_moto>/<int:id_cliente>', views.generar_compromiso_compra_venta,name="GCCV"),

     
     path('pago_por_ref/', views.buscar_pagos_por_refinanciamiento,name="PagoPorRef"),
     path('reservas', views.reservas,name="Reservas"),
     path('moto_reserva_form/<int:id_moto>', views.form_reservar_moto,name="MotoReservaForm"),
     path('moto_reserva/<int:id_moto>/<int:id_cliente>', views.reservar_moto,name="MotoReserva"),
     path('baja_moto_reserva/<int:id_reserva>', views.baja_reserva_moto,name="BajaReservaMoto"),
     path('alta_pago/<int:id_cv>', views.alta_pago,name="AltaPago"),
     path('baja_pago/<int:id_cm>', views.baja_pago,name="BajaPago"),
     path('refinanciar/<int:id_cv>', views.refinanciar_pagos,name="Refinanciar"),
     path('pago_cuota/<int:id_cv>', views.alta_pago_cuota,name="PagoCuotas"),
     path('baja_financiamiento/<int:id_f>/<int:id_cv>', views.baja_financiamiento,name="BajaFinanciamiento"),


     path('repuestos', views.repuestos,name="Repuestos"),
     path('alta_repuesto', views.alta_repuesto,name="AltaRepuesto"),
     path('buscar_repuesto_alta/', views.buscar_pieza,name="BuscarRepuestoAlta"),
     path('baja_repuesto/<int:id_rp>', views.baja_repuesto,name="BajaRepuesto"),
     path('modificacion_repuesto/<int:id_rp>', views.modificacion_repuesto,name="ModificacionRepuesto"),
     path('detalles_repuesto/<int:id_rp>', views.detalles_repuesto,name="DetallesRepuesto"),
     path('stock_critico', views.stock_critico,name="StockCritico"),
     path('estadisticas_taller', views.estadisticas_taller,name="EstadisticasTaller"),
     path('clientes_taller', views.clientes_taller,name="ClientesTaller"),
     path('busqueda_documento_taller', views.buscar_por_doc_taller,name="BusquedaDocumentoTaller"),
     path('busqueda_nombre_apellido_taller', views.buscar_nom_ape_taller,name="BusquedaNombreApellidoTaller"),
     path('alta_cliente_taller', views.alta_cliente_taller,name="AltaClienteTaller"),
     path('modificacion_cliente_taller/<int:id_cliente>', views.modificacion_cliente_taller,name="ModificacionClienteTaller"),
     path('empresa_alta_taller', views.alta_empresa_taller,name="EmpresaAltaTaller"),
     path('empresa_modificacion_taller/<int:id_cliente>', views.modificacion_empresa_taller,name="EmpresaModificacionTaller"),
     path('detalles_cliente_taller/<int:id_cliente>', views.detalles_cliente_taller,name="DetallesClienteTaller"),
     path('busqueda_rut_taller/', views.buscar_por_rut_taller,name="TallerBusquedaRUT"),
     path('busqueda_nombre_empresa_taller/', views.buscar_nom_emp_taller,name="TallerBusquedaNombreEmpresa"),
     path('servicios_por_moto/<int:id_moto>/<int:id_cliente>', views.servicios_por_moto_de_cliente,name="ServiciosPorMoto"),
     path('detalles_por_servicio/<int:id_s>/<int:id_cliente>', views.detalle_de_cada_servicio_de_moto,name="DetallesPorServicios"),
     path('cerrar_servicio/<int:id_s>', views.cerrar_servicio,name="CerrarServicio"),
     path('form_modificar_servicio/<int:id_s>', views.form_modificar_servicio,name="FormModificarServicio"),
     path('agregar_servicio/<int:id_s>', views.agregar_quitar_servicios,name="AgregarServicio"),
     path('agregar_anotacion_servicio/<int:id_s>', views.agregar_anotacion_servicio,name="AgregarAnotacionServicio"),
     path('borrar_servicio/<int:id_tarea>', views.borrar_servicio,name="BorrarServicio"),
     path('agregar_mecanico_servicio/<int:id_s>', views.agregar_mecanico_servicio,name="AgregarMecanicoServicio"),
     path('borrar_mecanico_servicio/<int:id_s>/<int:id_mecanico>', views.borrar_mecanico_servicio,name="BorrarMecanicoServicio"),
     path('modificar_servicio/<int:id_s>', views.modificar_datos_servicio,name="ModificarServicio"),
     path('agregar_repuesto_pieza_servicio/<int:id_s>', views.agregar_repuesto_pieza_servicio,name="AgregarRepPiezaServ"),
     
     path('borrar_repuesto_pieza_servicio/<int:id_rp>', views.borrar_repuesto_pieza_servicio,name="BorrarRepPiezaServ"),
     
     
     path('detalles_servicio/<int:id_s>', views.detalles_servicios,name="DetallesServicio"),
     path('detalles_servicio_cerrado/<int:id_s>', views.detalles_servicios_cerrados,name="DetallesServicioCerrado"),

     
     
     

     path('pedidos', views.pedidos,name="Pedidos"),
     path('cliente_pedido', views.cliente_pedido,name="ClientePedido"),
     path('alta_pedido/<int:id_cliente>', views.alta_pedido,name="AltaPedido"),
     path('baja_pedido/<int:id_pedido>', views.baja_pedido,name="BajaPedido"),
     path('cerrar_pedido/<int:id_pedido>', views.cerrar_pedido,name="CerrarPedido"),
     path('buscar_pedido_documento', views.busqueda_pedido_por_doc_cliente,name="PedidoPorDocumento"),
     path('buscar_pedido_nombre_apellido', views.busqueda_pedido_por_nombre_apellido_cliente,name="PedidoPorNombreApellido"),

     path('personal_taller', views.personal_taller,name="PersonalTaller"),
     path('alta_personal_taller', views.alta_personal_taller,name="AltaPersonalTaller"),
     path('reingresar_taller/<int:id_personal>', views.ingresar_taller,name="ReingresarTaller"),
     path('personal_taller_detalle/<int:id_personal>', views.detalles_personal_taller,name="PersonalTallerDetalle"),
     path('resetear_usuario_taller/<int:id_u>', views.resetear_usuario_taller,name="ResetearUsuarioTaller"),

     path('notificaciones_taller/', views.notificaciones_taller,name="NotificacionesTaller"),
     path('borrar_notificaciones_taller/<int:id_notificacion>', views.borrar_notificacion_taller,name="BorrarNotificacionesTaller"),     
          

     path('venta_repuesto_form/<int:id_rp>', views.venta_repuesto_form,name="VentaRepuestoPiezaForm"),
     path('venta_repuesto/<int:id_rp>/<int:id_cliente>', views.venta_repuesto,name="VentaRepuestoPieza"),


     path('motos_taller/', views.vista_inventario_motos_taller,name="MotosTaller"),
     path('busqueda_marca_taller', views.busqueda_marca_taller,name="BusquedaMarcaTaller"),
     path('busqueda_modelo_taller', views.busqueda_modelo_taller,name="BusquedaModeloTaller"),
     path('busqueda_matricula_taller', views.busqueda_matricula_taller,name="BusquedaMatriculaTaller"),
     path('busqueda_tipo_taller', views.busqueda_tipo_moto_taller,name="BusquedaTipoMotoTaller"),
     path('busqueda_num_motor_taller', views.busqueda_num_motor_taller,name="BusquedaNumMotorTaller"),
     path('busqueda_num_chasis_taller', views.busqueda_num_chasis_taller,name="BusquedaNumChasisTaller"),

     path('alta_moto_taller/', views.alta_moto_taller,name="AltaMotoTaller"),
     path('modificacion_moto_taller/<int:id_moto>', views.modificacion_moto_taller,name="ModMotoTaller"),
     path('detalles_moto_taller/<int:id_moto>', views.detalles_moto_taller,name="DetallesMotoTaller"),
     path('servicios_moto_taller/<int:id_s>/<int:id_cliente>', views.servicios_de_la_moto,name="ServiciosMoto"),


     path('balance/<str:busqueda>', views.balanceo,name="Balance"),
     path('movimiento_balance_baja/<int:id_movimiento>', views.baja_movimiento_movimiento,name="MovimientoBalanceBaja"),
     path('balance/', views.balanceo,name="Balance"),
     path('movimiento_balance_baja/<int:id_movimiento>', views.baja_movimiento_movimiento,name="MovimientoBalanceBaja"),
     path('detalles_balance_x_fecha/', views.buscar_detalles_balance_movimientos_x_fecha,name="DetallesBalanceCajaXFecha"),
     path('detalles_balance_x_fecha_excel/', views.buscar_detalles_balance_movimientos_x_fecha_excel,name="DetallesBalanceCajaXFechaExcel"),
     path('detalles_balance_x_mes_anio/', views.buscar_detalles_balance_movimientos_x_mes_anio,name="DetallesBalanceCajaXMesAnio"),
     path('detalles_balance_x_mes_anio_excel/', views.buscar_detalles_balance_movimientos_x_mes_anio_excel,name="DetallesBalanceCajaXMesAnioExcel"),
     path('ingresos_balance/', views.ingresos_balance,name="IngresosBalance"),
     path('egresos_balance/', views.egresos_balance,name="EgresosBalance"),
     path('nuevo_rubro_balance/', views.nuevo_rubro_egreso_balance,name="NuevoRubroBalance"),


     path('cambiar_a_perfil_taller/', views.cambiar_a_perfil_taller,name="CambiarAPerfilTaller"),
     path('cambiar_a_perfil_tienda/', views.cambiar_a_perfil_tienda,name="CambiarAPerfilTienda"),

     path('hojas_presupuestales/', views.hojas_presupuestales,name="HojasPresupuestales"),
     path('nuevo_presupuesto/', views.nuevo_presupuesto,name="NuevoPresupuesto"),
     path('cliente_moto_presupuesto/', views.buscar_moto_cliente,name="ClienteMotoPresupuesto"),
     path('baja_presupuesto/<int:id_p>', views.baja_presupuesto,name="BajaPresupuesto"),





     



     






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)