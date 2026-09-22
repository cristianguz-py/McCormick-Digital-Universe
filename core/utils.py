"""
core/utils.py
Punto único para registrar actividad administrativa. Evita duplicar la
lógica de "quién hizo qué" en cada app (sugerencias, ingresos, etc.).
"""
from .models import ActivityLog


def log_activity(user, action, metadata=None):
    """
    user puede ser None para acciones del sistema (p. ej. un job).
    metadata es un dict JSON-serializable con detalles breves, nunca
    contraseñas ni datos sensibles.
    """
    ActivityLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        metadata=metadata or {},
    )
