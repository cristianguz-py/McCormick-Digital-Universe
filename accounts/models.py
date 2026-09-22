"""
accounts/models.py
Usuario real de McCormick Digital Universe, con roles.
Usa el sistema de autenticación nativo de Django (hashing seguro,
sesiones reales) — nada de localStorage ni contraseñas en JS.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    SUPER_ADMIN = "super_admin", "Super Admin"
    ARTIST = "artist", "Artista"
    MARKETING = "marketing", "Marketing"


class User(AbstractUser):
    """
    Extiende AbstractUser (username, password hasheado, is_active, etc.)
    y agrega el rol que determina permisos y contenido del dashboard.
    """
    name = models.CharField(
        "Nombre para mostrar", max_length=150, blank=True,
        help_text="Nombre visible en el dashboard (si se deja vacío, se usa el username).",
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ARTIST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.name or self.username

    @property
    def display_name(self):
        return self.name or self.username

    @property
    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN

    @property
    def project_scope(self):
        """
        Determina a qué 'universo' pertenecen las sugerencias/analíticas
        de este usuario cuando no es super_admin. Usado para filtrar
        datos en dashboards de Maco / C&MC / Melanie.
        """
        mapping = {
            "maco.admin": "maco",
            "melanie.admin": "melanie",
            "ian.admin": "cmc",
        }
        return mapping.get(self.username)
