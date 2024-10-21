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

