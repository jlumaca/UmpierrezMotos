from django.db import models

# Create your models here.
class Personal(models.Model):
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=20)
    apellido  = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    usuario = models.CharField(max_length=10,unique=True)
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


class accesorio(models.Model):
    tipo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    foto = models.ImageField(null=True, blank=True, upload_to="accesorios/")
    activo = models.BooleanField()

class Logos(models.Model):
    logo_UM = models.ImageField(null=True, blank=True, upload_to="logos/")
    logo_DM = models.ImageField(null=True, blank=True, upload_to="logos/")

