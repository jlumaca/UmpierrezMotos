from .models import *
def cantidad_solicitudes_no_leidas(req):
    if req.user.is_authenticated:
        usuario = req.user
        usuario_actual = Personal.objects.filter(usuario=usuario.username).first()
        notificaciones = NotificacionPersonal.objects.filter(personal=usuario_actual,leido=0).count()
    else:
        notificaciones = 0
    
    return {'notificaciones': notificaciones}

def perfiles_usuario_actual_administrativo(req):
    if req.user.is_authenticated:
        usuario = req.user
        usuario_actual = Personal.objects.filter(usuario=usuario.username).first()
        obtener_administrativo = Administrativo.objects.filter(personal_ptr_id=usuario_actual.id).first()
        obtener_mecanico = Mecanico.objects.filter(personal_ptr_id=usuario_actual.id).first()

        administrativo = obtener_administrativo.activo
        mecanico_jefe = obtener_mecanico.activo and obtener_mecanico.jefe
        mecanico_empleado = obtener_mecanico.activo and not obtener_mecanico.jefe
        if administrativo and (mecanico_jefe or mecanico_empleado):
            permisos = True
        else:
            permisos = False
    else:
        permisos = None
    
    return {'administrativo_taller': permisos,'taller_administrativo':permisos}