from django.db import models

# Create your models here.
class Personal(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=20)
    apellido  = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    usuario = models.CharField(max_length=100,unique=True)
    contrasena = models.CharField(max_length=20)
    correo = models.CharField(max_length=40,unique=True)
    telefono = models.CharField(max_length=10,unique=True) 
    primera_sesion = models.BooleanField(default=False)

class Administrativo(Personal):
    activo = models.BooleanField(default=True)

class Mecanico(Personal):
    jefe = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

class Moto(models.Model):
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    anio = models.IntegerField(null=True, blank=True)
    motor = models.IntegerField()
    estado = models.CharField(max_length=10)
    kilometros = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    color = models.CharField(max_length=20,null=True, blank=True)   
    num_motor = models.CharField(max_length=40, unique=True)
    num_chasis = models.CharField(max_length=40, unique=True)
    num_cilindros = models.IntegerField(default=1)
    cantidad_pasajeros = models.IntegerField(default=2,null=True, blank=True)
    foto = models.ImageField(null=True, blank=True, upload_to="motos/fotos/")
    pertenece_tienda = models.BooleanField()
    pertenece_taller = models.BooleanField()
    identificacion_pdf = models.FileField(upload_to='motos/pdfs/', null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    moneda_precio = models.CharField(max_length=10,default=True,null=True)
    tipo = models.CharField(max_length=20,blank=True)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2,default=0,null=True, blank=True)
    contiene_num_motor = models.BooleanField(default=1)
    contiene_num_chasis = models.BooleanField(default=1)

class Matriculas(models.Model):
    moto = models.ForeignKey(Moto, related_name='moto', on_delete=models.CASCADE, null=True)
    matricula = models.CharField(max_length=20, unique=True)
    padron = models.IntegerField(null=True, blank=True)



class Accesorio(models.Model):
    tipo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(null=True, blank=True, upload_to="accesorios/")
    activo = models.BooleanField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    moneda_precio = models.CharField(max_length=10,default=True,null=True)
    talle = models.CharField(max_length=20,null=True)
    seleccionado = models.BooleanField(default=0)

class Logos(models.Model):
    logo_UM = models.ImageField(null=True, blank=True, upload_to="logos/")
    logo_DM = models.ImageField(null=True, blank=True, upload_to="logos/")

class Cliente(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    apellido  = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    # ciudad = models.CharField(max_length=40)
    # calle = models.CharField(max_length=40)
    # numero = models.IntegerField()
    # num_apartamento = models.IntegerField()
    domicilio = models.CharField(max_length=500,blank=True) 
    tipo = models.CharField(max_length=500,default="Cliente")


class ClienteCorreo(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_correo', on_delete=models.CASCADE, null=True)
    correo = models.CharField(max_length=100)
    principal = models.BooleanField(default=True)
    

class ClienteTelefono(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_telefono', on_delete=models.CASCADE, null=True)
    telefono = models.CharField(max_length=10)
    principal = models.BooleanField(default=True)
   


class ComprasVentas(models.Model):
    moto = models.ForeignKey(Moto, related_name='moto_cliente', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, related_name='cliente_moto', on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    fotocopia_libreta = models.ImageField(null=True, blank=True, upload_to="documentacion/libretas/")
    compra_venta = models.FileField(null=True, blank=True, upload_to="documentacion/compra_venta/")
    certificado_venta = models.FileField(null=True, blank=True, upload_to="documentacion/certificado_venta/")
    tipo = models.CharField(max_length=20)
    forma_de_pago = models.TextField(null=True, blank=True)
    facturas = models.FileField(null=True, blank=True, upload_to="documentacion/facturas_motos/")

    class Meta:
        pass
#tipo = V --->>> PARA CUANDO UN CLIENTE COMPRA UNA MOTO
#tipo = CV --->>> PARA CUANDO UN CLIENTE VENDE UNA MOTO USADA
#tipo = R --->>> PARA CUANDO UNA MOTO ESTA RESERVADA

class ClienteAccesorio(models.Model):
    accesorio = models.ForeignKey(Accesorio, related_name='accesorio_cliente', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, related_name='cliente_cliente', on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    factura = models.IntegerField(null=True)
    factura_rut = models.IntegerField(null=True)
    factura_documento = models.FileField(null=True, blank=True, upload_to="documentacion/facturas_accesorios/")
    codigo_compra = models.IntegerField(null=True,default=0)
    forma_de_pago = models.TextField(null=True, blank=True)

class PrecioDolar(models.Model):
    precio_dolar_tienda = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    precio_dolar_taller = models.DecimalField(max_digits=10, decimal_places=2,default=0)

class Notificaciones(models.Model):
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)
    url = models.CharField(max_length=20,null=True,blank=True)

class NotificacionPersonal(models.Model):
    personal = models.ForeignKey(Personal, related_name='personal_notificacion', on_delete=models.CASCADE)
    notificacion = models.ForeignKey(Notificaciones, related_name='notificacion_personal', on_delete=models.CASCADE)
    leido = models.BooleanField(default=0)

class Caja(models.Model):
    apertura = models.DateTimeField()
    cierre = models.DateTimeField(null=True,blank=True)
    moneda = models.CharField(max_length=10)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    depositos = models.DecimalField(max_digits=10, decimal_places=2)
    egresos = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_caja = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_sistema = models.DecimalField(max_digits=10, decimal_places=2)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10)
    usuario = models.ForeignKey(Personal, related_name='usuario_caja', on_delete=models.CASCADE)

class Movimientos(models.Model):
    fecha = models.DateTimeField()
    movimiento = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=10)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    caja = models.ForeignKey(Caja, related_name='movimiento_caja', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Personal, related_name='usuario_movimiento', on_delete=models.CASCADE)
    moneda = models.CharField(max_length=10,null=True,blank=True)
    rubro = models.TextField(null=True, blank=True)
    metodo = models.CharField(max_length=30,null=True,blank=True)
    es_moto = models.BooleanField(default=0)
    es_accesorio = models.BooleanField(default=0)

class CuotasAccesorios(models.Model):
    fecha_pago = models.DateField()
    moneda = models.CharField(max_length=10,default=True,null=True)
    valor_pago_pesos = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    valor_pago_dolares = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cant_restante_pesos = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cant_restante_dolares = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    precio_dolar = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    venta = models.ForeignKey(ClienteAccesorio, related_name='cliente_accesorio', on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)
    comprobante_pago = models.FileField(upload_to='documentacion/facturas_accesorios/', null=True, blank=True)
    metodo_pago = models.CharField(max_length=20, blank=True)
    recargo = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    mostrar_reporte = models.BooleanField(default=1)
    fecha_prox_pago = models.DateField(null=True)

class Servicios(models.Model):
    fecha_ingreso = models.DateField()
    descripcion_ingreso = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, blank=True)
    prioridad = models.CharField(max_length=20, blank=True)
    fecha_estimada_cierre = models.DateField(null=True)
    fecha_prox_servicio = models.DateField(null=True)
    km_prox_servicio = models.IntegerField(null=True)
    moto = models.ForeignKey(Moto, related_name='moto_servicio', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, related_name='cliente_servicio', on_delete=models.CASCADE)
    dias = models.IntegerField(default=0)
    titulo = models.CharField(max_length=20, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2,default=0)

class MecanicosServicios(models.Model):
    mecanico = models.ForeignKey(Mecanico, related_name='mecanicos_servicios', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicios, related_name='servicios_mecanicos', on_delete=models.CASCADE)

class TareasServicios(models.Model):
    servicio = models.ForeignKey(Servicios, related_name='tareas_servicios', on_delete=models.CASCADE)
    tarea = models.TextField(null=True, blank=True)
    realizado = models.BooleanField(default=0)

class Financiamientos(models.Model):
    fecha = models.DateField()
    recargo = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cantidad_cuotas = models.IntegerField(default=1)
    valor_cuota = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    moneda_cuota = models.CharField(max_length=20, blank=True)
    actual = models.BooleanField(default=True)
    venta = models.ForeignKey(ComprasVentas, related_name='financiamientos_venta', on_delete=models.CASCADE)
    inicial = models.BooleanField(default=False)
    precio_moto_actual = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quincena = models.BooleanField(default=False)
    semanal = models.BooleanField(default=False)

class CuotasMoto(models.Model):
    fecha_pago = models.DateField()
    fecha_prox_pago = models.DateField(null=True)
    moneda = models.CharField(max_length=10,default=True,null=True)
    valor_pago_pesos = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    valor_pago_dolares = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cant_restante_pesos = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    cant_restante_dolares = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    precio_dolar = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    venta = models.ForeignKey(ComprasVentas, related_name='cuotas_venta', on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)
    comprobante_pago = models.FileField(upload_to='documentacion/comprobantes/', null=True, blank=True)
    metodo_pago = models.CharField(max_length=20, blank=True,null=True)
    tipo_pago = models.CharField(max_length=20, blank=True)

class CuotasFinanciacion(models.Model):
    cuota = models.ForeignKey(CuotasMoto, related_name='cuota_financiamiento', on_delete=models.CASCADE)
    financiamiento = models.ForeignKey(Financiamientos, related_name='financiamiento_cuota', on_delete=models.CASCADE)

class RepuestosPiezas(models.Model):
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    stock = models.IntegerField(null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    foto = models.ImageField(null=True, blank=True, upload_to="repuestos_piezas/")
    stock_critico = models.IntegerField(null=True)
    

class Pedidos(models.Model):
    detalle = models.CharField(max_length=200)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, related_name='pedido_cliente', on_delete=models.CASCADE)

class AnotacionesServicio(models.Model):
    anotaciones = models.TextField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    mecanico = models.ForeignKey(Mecanico, related_name='anotacion_mecanicos', on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicios, related_name='anotacion_servicio', on_delete=models.CASCADE)

class RepuestosPiezasServicios(models.Model):
    servicio = models.ForeignKey(Servicios, related_name='servicio_rp', on_delete=models.CASCADE)
    repuestopieza = models.ForeignKey(RepuestosPiezas, related_name='rp_servicios', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)

class ClienteFondos(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_fondos', on_delete=models.CASCADE, null=True)
    moneda = models.CharField(max_length=10,default=True,null=True)
    ingreso_pesos = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_pesos = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    fecha = models.DateField()
    ingreso_dolares = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    total_dolares = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    tipo = models.CharField(max_length=10,default=True,null=True)
    metodo = models.CharField(max_length=20, blank=True)
    comprobante = models.FileField(upload_to='documentacion/comprobantes/', null=True, blank=True)

class ClienteRepuestosPiezas(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_rp', on_delete=models.CASCADE, null=True)
    repuestospiezas = models.ForeignKey(RepuestosPiezas, related_name='rp_cliente', on_delete=models.CASCADE, null=True)
    cantidad = models.IntegerField(default=0)
    fecha_compra = models.DateField(null=True) 


class Rubros(models.Model):
    rubro = models.TextField(null=True, blank=True)
    habilitado = models.BooleanField(default=True)
    cantidad_usos = models.IntegerField(default=0)

class MovimientoPagoMoto(models.Model):
    pago = models.ForeignKey(CuotasMoto, related_name='pago_moto_movimiento', on_delete=models.CASCADE)
    movimiento= models.ForeignKey(Movimientos, related_name='movimiento_pago_moto', on_delete=models.CASCADE)

class MovimientoPagoAccesorio(models.Model):
    pago = models.ForeignKey(CuotasAccesorios, related_name='pago_accesorio_movimiento', on_delete=models.CASCADE)
    movimiento = models.ForeignKey(Movimientos, related_name='movimiento_pago_accesorio', on_delete=models.CASCADE)

class Presupuestos(models.Model):
    titulo = models.CharField(max_length=300)
    texto = models.TextField(null=True, blank=True,default=True)
    moneda = models.CharField(max_length=10,default=True,null=True)
    mano_de_obra = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    precio_dolar = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    fuente_precios = models.CharField(max_length=200,default=True)
    fecha = models.DateField()
    archivo = models.FileField(upload_to='presupuestos/', null=True, blank=True)
    usuario = models.ForeignKey(Personal, related_name='personal_presupuesto', on_delete=models.CASCADE)
    marca = models.CharField(max_length=20,default=True)
    modelo = models.CharField(max_length=20,default=True)
    anio = models.IntegerField(null=True, blank=True,default=True)
    matricula = models.CharField(max_length=20, default=True)
    padron = models.IntegerField(null=True, blank=True,default=True)
    num_motor = models.CharField(max_length=40, default=True)
    num_chasis = models.CharField(max_length=40, default=True)
    documento = models.CharField(max_length=20, default=True)
    nombre = models.CharField(max_length=200,default=True)
    apellido = models.CharField(max_length=200,default=True)
    tipo_doc = models.CharField(max_length=10,default=True,null=True)

class PiezasPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuestos, related_name='piezas_presupuesto', on_delete=models.CASCADE)
    piezas = models.CharField(max_length=200)
    cantidad = models.IntegerField(null=True, blank=True)
    moneda = models.CharField(max_length=10,default=True,null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

class NotasPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuestos, related_name='notas_presupuesto', on_delete=models.CASCADE)
    notas = models.CharField(max_length=200)


class HojasMembretadas(models.Model):
    titulo = models.CharField(max_length=300)
    texto = models.TextField(null=True, blank=True,default=True)
    usuario = models.ForeignKey(Personal, related_name='personal_hoja_membretada', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='hojas_membretadas/', null=True, blank=True)
    fecha = models.DateField()

    


    


    

