from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .models import Personal, Administrativo, Mecanico

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        # Verificar si el usuario está autenticado y si es un administrativo
        if user.is_authenticated:
            usuario_consulta = Personal.objects.filter(usuario=user.username).first()
            if usuario_consulta:
                if Administrativo.objects.filter(personal_ptr_id=usuario_consulta.id,activo=1).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return view_func(request, *args, **kwargs)
        else:
            return redirect('Login')  # Redirigir al login si no está autenticado
    return _wrapped_view

def mecanico_jefe_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        # Verificar si el usuario está autenticado y si es un mecánico jefe
        if user.is_authenticated:
            usuario_consulta = Personal.objects.filter(usuario=user.username).first()
            if usuario_consulta:
                if Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id, activo=True, jefe=True).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return view_func(request, *args, **kwargs)
        else:
            return redirect('Login')  # Redirigir al login si no está autenticado
    return _wrapped_view

def mecanico_empleado_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        # Verificar si el usuario está autenticado y si es un mecánico empleado
        if user.is_authenticated:
            usuario_consulta = Personal.objects.filter(usuario=user.username).first()
            if usuario_consulta:
                if Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id, activo=True, jefe=False).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return view_func(request, *args, **kwargs)
        else:
            return redirect('Login')  # Redirigir al login si no está autenticado
    return _wrapped_view
