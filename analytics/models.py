"""
analytics/models.py
Un evento real por fila. Sin contraseñas ni datos personales innecesarios.
"""
from django.conf import settings
from django.db import models


class EventType(models.TextChoices):
    PAGE_VIEW = "page_view", "Vista de página"
    SOCIAL_CLICK = "social_click", "Click en red social"
    CONTACT_CLICK = "contact_click", "Click en contacto"
    GALLERY_OPEN = "gallery_open", "Apertura de galería"
    CTA_CLICK = "cta_click", "Click en CTA"
    LOGIN = "login", "Inicio de sesión"
    LOGOUT = "logout", "Cierre de sesión"
    SUGGESTION_CREATED = "suggestion_created", "Sugerencia creada"
    SUGGESTION_UPDATED = "suggestion_updated", "Sugerencia actualizada"


class AnalyticsEvent(models.Model):
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    page = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="analytics_events",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "page", "created_at"]),
        ]
        verbose_name = "Evento de analítica"
        verbose_name_plural = "Eventos de analítica"

    def __str__(self):
        return f"{self.event_type} — {self.page} — {self.created_at:%Y-%m-%d %H:%M}"
