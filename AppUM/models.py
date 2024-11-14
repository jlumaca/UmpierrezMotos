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

class Administrativo(Personal):
    activo = models.BooleanField(default=True)

class Mecanico(Personal):
    jefe = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

class Moto(models.Model):
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    anio = models.IntegerField()
    motor = models.IntegerField()
    estado = models.CharField(max_length=10)
    kilometros = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=20)   
    num_motor = models.CharField(max_length=40, unique=True)
    num_chasis = models.CharField(max_length=40, unique=True)
    foto = models.ImageField(null=True, blank=True, upload_to="motos/fotos/")
    pertenece_tienda = models.BooleanField()
    pertenece_taller = models.BooleanField()
    identificacion_pdf = models.FileField(upload_to='motos/pdfs/', null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

class Matriculas(models.Model):
    moto = models.ForeignKey(Moto, related_name='moto', on_delete=models.CASCADE, null=True)
    matricula = models.CharField(max_length=20, unique=True)
    activo = models.BooleanField()


class Accesorio(models.Model):
    tipo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(null=True, blank=True, upload_to="accesorios/")
    activo = models.BooleanField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

class Logos(models.Model):
    logo_UM = models.ImageField(null=True, blank=True, upload_to="logos/")
    logo_DM = models.ImageField(null=True, blank=True, upload_to="logos/")

class Cliente(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=20)
    apellido  = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    ciudad = models.CharField(max_length=40)
    calle = models.CharField(max_length=40)
    numero = models.IntegerField()
    num_apartamento = models.IntegerField()


class ClienteCorreo(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_correo', on_delete=models.CASCADE, null=True)
    correo = models.CharField(max_length=100, unique=True)
    principal = models.BooleanField(default=True)
    

class ClienteTelefono(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='cliente_telefono', on_delete=models.CASCADE, null=True)
    telefono = models.CharField(max_length=10,unique=True)
    principal = models.BooleanField(default=True)
   


class ComprasVentas(models.Model):
    moto = models.ForeignKey(Moto, related_name='moto_cliente', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, related_name='cliente_moto', on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    padron = models.IntegerField(unique=True)
    fotocopia_libreta = models.ImageField(null=True, blank=True, upload_to="documentacion/libretas/")
    compra_venta = models.FileField(null=True, blank=True, upload_to="documentacion/compra_venta/")
    certificado_venta = models.FileField(null=True, blank=True, upload_to="documentacion/certificado_venta/")
    tipo = models.CharField(max_length=20)
    cantidad_cuotas = models.IntegerField()
    cuotas_pagas = models.IntegerField()
    valor_cuota = models.IntegerField()

    class Meta:
        pass
#tipo = V --->>> PARA CUANDO UN CLIENTE COMPRA UNA MOTO
#tipo = CV --->>> PARA CUANDO UN CLIENTE VENDE UNA MOTO USADA

class ClienteAccesorio(models.Model):
    accesorio = models.ForeignKey(Accesorio, related_name='accesorio_cliente', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, related_name='cliente_cliente', on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    factura = models.IntegerField(null=True)
    factura_rut = models.IntegerField(null=True)
    factura_documento = models.FileField(null=True, blank=True, upload_to="documentacion/facturas_accesorios/")

