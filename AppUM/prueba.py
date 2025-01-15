from datetime import date
from .models import *
# import pywhatkit

# contact = '+59892344264'

# hour = 13

# minute = 2

# message = 'prueba'
# pywhatkit.sendwhatmsg(contact, message, hour, minute)

# print(date.today())

hoy = date.today()
pagos_atrasados = CuotasMoto.objects.all()

for pagos in pagos_atrasados:
    venta = ComprasVentas.objects.get(id=pagos.venta_id)
    ult_pago = CuotasMoto.objects.filter(venta=venta).latest('id')
    if pagos.fecha_prox_pago and (pagos.fecha_prox_pago.day, pagos.fecha_prox_pago.month) == (hoy.day, hoy.month) and pagos.id == ult_pago.id:
        cliente = Cliente.objects.get(id=venta.cliente_id)
        moto = Moto.objects.get(id=venta.moto_id)
        tipo = "Atraso en cuota"
        descripcion = f"El cliente {cliente.nombre} {cliente.apellido} se encuentra atrasado en el pago de su {moto.marca} {moto.modelo}"
        print(descripcion)