"""
accounts/decorators.py
Protección real de rutas por rol (no ocultamiento visual: si el usuario
no tiene el rol requerido, recibe un 403 real).
"""
from functools import wraps
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """Uso: @role_required('super_admin')"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role not in roles:
                raise PermissionDenied("No tienes permiso para acceder a esta sección.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
