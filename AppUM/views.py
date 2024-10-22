from django.shortcuts import render
from .models import *

# Create your views here.

def vista_login(req):
    return render(req,"login/login.html",{})

def validacion_login(req):

    #if req.METHOD == 'GET':
    usuario = req.GET['usuario_login']
    passw = req.GET['pass_login']

    usuario = Personal.objects.get(usuario=usuario,contrasena=passw)

    if usuario:
        #contexto = "EXITO"
        print(usuario.values())
        mecanico = Mecanico.objects.get(id=usuario)
        if mecanico:
            contexto = "MECANICO"
        else:
            contexto = "NO MECANICO"
    else:
        contexto = "Error de usuario y/o contraseña"

    
    return render(req,"login/login.html",{"resultado":contexto})
