from django.shortcuts import render
from .models import *

# Create your views here.

def vista_login(req):
    return render(req,"login/login.html",{})

def validacion_login(req):

    #if req.METHOD == 'GET':
    usuario = req.GET['usuario_login']
    passw = req.GET['pass_login']

    usuario_consulta = Personal.objects.filter(usuario=usuario,contrasena=passw).first()
    

    if usuario_consulta:
        mecanico = Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id).first()
        if mecanico:
            if mecanico.activo == 1:
                existe_mecanico = 1
                if mecanico.jefe == 1:
                    mecanico_jefe = 1
                else:
                    mecanico_jefe = 0
            else:
                existe_mecanico = 0
        else:
            existe_mecanico = 0
        administrativo = Administrativo.objects.filter(personal_ptr_id=usuario_consulta.id).first()
        if administrativo:
            if administrativo.activo == 1:
                existe_administrativo = 1
            else:
                existe_administrativo = 0
        else:
            existe_administrativo = 0
        
        if existe_mecanico == 1 and mecanico_jefe == 1 and existe_administrativo == 1:
            contexto = "Administrativo y Mecanico Jefe"
        elif existe_mecanico == 1 and mecanico_jefe == 0 and existe_administrativo == 1:
            contexto = "Administrativo y Mecanico Empleado"
        elif existe_administrativo == 1 and existe_mecanico == 0:
            contexto = "Solo Administrativo"
        elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 1:
            contexto = "Solo Mecanico Jefe"
        elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 0:
            contexto = "Solo Mecanico Empleado" 
        else:
            contexto = "Este usuario fue dado de baja, contactese con el administrador del sistema."
           
    else:
        contexto = "Error de usuario y/o contraseña"
        
    return render(req,"login/login.html",{"resultado":contexto})
