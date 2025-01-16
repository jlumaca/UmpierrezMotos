from .models import *
def cantidad_solicitudes_no_leidas(req):
    if req.user.is_authenticated:
        usuario = req.user
        usuario_actual = Personal.objects.filter(usuario=usuario.username).first()
        notificaciones = NotificacionPersonal.objects.filter(personal=usuario_actual,leido=0).count()
    else:
        notificaciones = 0
    
    return {'notificaciones': notificaciones}