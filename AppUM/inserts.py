from .models import *
from datetime import date
from datetime import datetime
def insert_moto(marca,modelo,anio,estado,cc_motor,kilometros,moneda,precio,color,num_motor,num_chasis,num_cilindros,num_pasajeros,pert_tienda,pert_taller,observaciones,foto,tipo_moto):
    nueva_moto = Moto(marca = marca,
                    modelo = modelo,
                    anio = anio,
                    estado = estado,
                    motor = cc_motor,
                    kilometros = kilometros,
                    moneda_precio = moneda,
                    precio = precio,
                    color = color,
                    num_motor = num_motor,
                    num_chasis = num_chasis,
                    num_cilindros = num_cilindros,
                    cantidad_pasajeros = num_pasajeros,
                    pertenece_tienda = pert_tienda,
                    pertenece_taller = pert_taller,
                    fecha_ingreso = datetime.now(),
                    observaciones = observaciones,
                    foto = foto,
                    tipo = tipo_moto
                    )
    nueva_moto.save()

    return nueva_moto

def insert_compras_ventas(tipo,libreta_propiedad,id_cliente,id_moto,compra_venta,certificado_venta,forma_de_pago):
    cliente_moto = ComprasVentas(
                fecha_compra = datetime.now(),
                compra_venta = compra_venta,
                certificado_venta = certificado_venta,
                tipo = tipo,
                fotocopia_libreta = libreta_propiedad,
                cliente_id = id_cliente,
                moto_id = id_moto,
                forma_de_pago = forma_de_pago
            )
    cliente_moto.save()

    return cliente_moto.id

def insert_matriculas(matricula,padron,id_moto):
    nueva_matricula = Matriculas(
                matricula = matricula,
                padron = padron,
                moto_id = id_moto
            )
    nueva_matricula.save()

def insert_cliente_telefono(telefono,principal,id_cliente):
    telefono_cliente = ClienteTelefono(
                    telefono = telefono,
                    principal = principal,
                    
                    cliente_id = id_cliente
                )
    telefono_cliente.save()

def insert_cliente_correo(correo,principal,id_cliente):
    correo_cliente = ClienteCorreo(
                        correo = correo,
                        principal = principal,
                        
                        cliente_id = id_cliente
                    )
    correo_cliente.save()

def insert_movimientos_caja(movimiento_descripcion,tipo,monto,id_caja,id_personal):
    movimiento = Movimientos(
        fecha = datetime.now(),
        movimiento = movimiento_descripcion,
        tipo = tipo,
        monto = monto,
        caja_id = id_caja,
        usuario_id = id_personal
    )
    movimiento.save()

def insert_cuotas_moto(fecha_prox_pago,id_cv,resto_dolares,resto_pesos,moneda,precio_dolar,entrega_dolares,entrega_pesos,observaciones):
    nueva_cuota = CuotasMoto(
                fecha_pago = datetime.now(),
                fecha_prox_pago = fecha_prox_pago,
                venta_id = id_cv,
                cant_restante_dolares = resto_dolares,
                cant_restante_pesos = resto_pesos,
                moneda = moneda,
                precio_dolar = precio_dolar,
                valor_pago_dolares = entrega_dolares,
                valor_pago_pesos = entrega_pesos,
                observaciones = observaciones
            )
    nueva_cuota.save()

def movimiento_caja_por_pago(req,entrega,id_cv,moneda):
    #movimiento_caja_por_pago(entrega,id_cv,moneda)
    cv = ComprasVentas.objects.get(id=id_cv)
    caja = Caja.objects.filter(estado = "Abierto").first()
    usuario = req.user
    personal = Personal.objects.filter(usuario=usuario.username).first()
    cliente = Cliente.objects.get(id=cv.cliente_id)
    dolar = PrecioDolar.objects.get(id=1)
    precio_dolar = dolar.precio_dolar_tienda
    
    if moneda == "Pesos":
        nuevo_ingreso = caja.depositos + int(entrega)
    else:
        nuevo_ingreso = caja.depositos + (int(entrega) * precio_dolar)
    
    caja.depositos = nuevo_ingreso
    caja.save()  
    cliente_nombre_apellido = cliente.nombre + " " + cliente.apellido
    movimiento_descripcion = "Pago de moto, cliente: " + cliente_nombre_apellido + " Moneda: " + moneda
    insert_movimientos_caja(movimiento_descripcion,"Ingreso",entrega,caja.id,personal.id)

def movimiento_caja_por_pago_accesorio(req,entrega,id_ca,moneda):
    #movimiento_caja_por_pago(entrega,id_cv,moneda)
    cv = ClienteAccesorio.objects.get(id=id_ca)
    caja = Caja.objects.filter(estado = "Abierto").first()
    usuario = req.user
    personal = Personal.objects.filter(usuario=usuario.username).first()
    cliente = Cliente.objects.get(id=cv.cliente_id)
    dolar = PrecioDolar.objects.get(id=1)
    precio_dolar = dolar.precio_dolar_tienda
    
    if moneda == "Pesos":
        nuevo_ingreso = caja.depositos + int(entrega)
    else:
        nuevo_ingreso = caja.depositos + (int(entrega) * precio_dolar)
    
    caja.depositos = nuevo_ingreso
    caja.save()  
    cliente_nombre_apellido = cliente.nombre + " " + cliente.apellido
    movimiento_descripcion = "Pago de accesorio, cliente: " + cliente_nombre_apellido + " Moneda: " + moneda
    insert_movimientos_caja(movimiento_descripcion,"Ingreso",entrega,caja.id,personal.id)

def alta_cuota_funcion(req,fecha_prox_pago,id_cv,resto_dolares,resto_pesos,moneda,observaciones_pago,precio_dolar,entrega_dolares,entrega_pesos,comprobante,forma_pago):
    nueva_cuota = CuotasMoto(
                    fecha_pago = datetime.now(),
                    fecha_prox_pago = fecha_prox_pago,
                    venta_id = id_cv,
                    cant_restante_dolares = resto_dolares,
                    cant_restante_pesos = resto_pesos,
                    moneda = moneda,
                    observaciones = observaciones_pago,
                    precio_dolar = precio_dolar,
                    valor_pago_dolares = entrega_dolares,
                    valor_pago_pesos = entrega_pesos,
                    comprobante_pago = comprobante,
                    metodo_pago = forma_pago,
                )
    nueva_cuota.save()
    if nueva_cuota.comprobante_pago:
            comprobante_url = nueva_cuota.comprobante_pago.url
    else:
            comprobante_url = None
    
    return comprobante_url

def alta_cuota_accesorio(req,fecha_prox_pago,id_cv,resto_dolares,resto_pesos,moneda,observaciones_pago,precio_dolar,entrega_dolares,entrega_pesos,comprobante,forma_pago,recargo):
    nueva_cuota = CuotasAccesorios(
                    fecha_pago = datetime.now(),
                    fecha_prox_pago = fecha_prox_pago,
                    venta_id = id_cv,
                    cant_restante_dolares = resto_dolares,
                    cant_restante_pesos = resto_pesos,
                    moneda = moneda,
                    observaciones = observaciones_pago,
                    precio_dolar = precio_dolar,
                    valor_pago_dolares = entrega_dolares,
                    valor_pago_pesos = entrega_pesos,
                    comprobante_pago = comprobante,
                    metodo_pago = forma_pago,
                    recargo = recargo
                )
    nueva_cuota.save()
    if nueva_cuota.comprobante_pago:
            comprobante_url = nueva_cuota.comprobante_pago.url
    else:
            comprobante_url = None
    
    return comprobante_url