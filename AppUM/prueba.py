from datetime import date
import os
import sys
import django

# Agregar la ruta del proyecto Django al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Directorio actual
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Directorio del proyecto

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProyectoUM.settings")  # Asegúrate de que el nombre sea correcto
django.setup()

from AppUM.models import *  # Importación absoluta
# import pywhatkit

# contact = '+59892344264'

# hour = 13

# minute = 2

# message = 'prueba'
# pywhatkit.sendwhatmsg(contact, message, hour, minute)

# print(date.today())

# hoy = date.today()
# pagos_atrasados = CuotasMoto.objects.all()

# for pagos in pagos_atrasados:
#     venta = ComprasVentas.objects.get(id=pagos.venta_id)
#     ult_pago = CuotasMoto.objects.filter(venta=venta).latest('id')
#     if pagos.fecha_prox_pago and (pagos.fecha_prox_pago.day, pagos.fecha_prox_pago.month) == (hoy.day, hoy.month) and pagos.id == ult_pago.id:
#         cliente = Cliente.objects.get(id=venta.cliente_id)
#         moto = Moto.objects.get(id=venta.moto_id)
#         tipo = "Atraso en cuota"
#         descripcion = f"El cliente {cliente.nombre} {cliente.apellido} se encuentra atrasado en el pago de su {moto.marca} {moto.modelo}"
#         print(descripcion)

compras = ClienteAccesorio.objects.all()
codigo_compra = 0

# while compras:


#ASIGNAR CODIGO DE VENTA A LAS COMPRAS DE LOS CLIENTES
# i = 0
# j = 0
# for compra in compras:
#     cantidad_compras_dia = ClienteAccesorio.objects.filter(fecha_compra=compra.fecha_compra).count()
    
#     if cantidad_compras_dia == 1:
#         codigo_compra = codigo_compra + 1
#     else:
#         #MAS DE UNA COMPRA
#         cliente = ClienteAccesorio.objects.filter(cliente=compra.cliente,fecha_compra=compra.fecha_compra).count()
#         i = compra.cliente_id
#         if cliente == 1 or i != j:
#             codigo_compra = codigo_compra + 1
#             j = i
#         # j = compra.cliente_id


#     compra.codigo_compra = codigo_compra
#     compra.save()


#LIMPIAR BASE DE DATOS
CuotasAccesorios.objects.all().delete()
ClienteCorreo.objects.all().delete()
ClienteTelefono.objects.all().delete()
ClienteFondos.objects.all().delete()
AnotacionesServicio.objects.all().delete()
ClienteAccesorio.objects.all().delete()
ClienteRepuestosPiezas.objects.all().delete()
CuotasFinanciacion.objects.all().delete()
Financiamientos.objects.all().delete()
MovimientoPagoAccesorio.objects.all().delete()
MovimientoPagoMoto.objects.all().delete()
CuotasMoto.objects.all().delete()
Accesorio.objects.all().delete()
ComprasVentas.objects.all().delete()
Movimientos.objects.all().delete()
Caja.objects.all().delete()
Matriculas.objects.all().delete()
MecanicosServicios.objects.all().delete()
NotificacionPersonal.objects.all().delete()
Notificaciones.objects.all().delete()
Pedidos.objects.all().delete()
RepuestosPiezasServicios.objects.all().delete()
Rubros.objects.all().delete()
RepuestosPiezas.objects.all().delete()
TareasServicios.objects.all().delete()
Servicios.objects.all().delete()
Moto.objects.all().delete()
Cliente.objects.all().delete()



















#     for cliente in compra_dia:
#             codigo_compra = codigo_compra + 1
#             compra.codigo_compra = codigo_compra
#             compra.save()
        # if (cliente.fecha_compra == compra.fecha_compra) and (cliente.cliente == compra.cliente):
        #     #mismo codigo compra
        #     compra.codigo_compra = codigo_compra
        #     compra.save()
        # else:
        #     codigo_compra = codigo_compra + 1
        #     compra.codigo_compra = codigo_compra
        #     compra.save()
            # compra.codigo_compra = codigo_compra
            # compra.save()
            # codigo_compra = codigo_compra + 1
            # if cliente.cliente == compra.cliente:
            #       #     #mismo codigo compra
            #     compra.codigo_compra = codigo_compra
            #     compra.save()
            # else:
            #     codigo_compra = codigo_compra + 1
            #     compra.codigo_compra = codigo_compra
            #     compra.save()
                 
                  
    # compra.codigo_compra = codigo_compra
    # compra.save()