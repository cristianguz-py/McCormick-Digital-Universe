"""
suggestions/models.py
Sistema real de sugerencias: cada sugerencia queda asociada a quien la
envió, con historial de cambios de estado y comentarios de respuesta.
"""
from django.conf import settings
from django.db import models


def suggestion_attachment_path(instance, filename):
    return f"suggestions/{instance.user_id}/{filename}"


class Suggestion(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Baja"
        MEDIUM = "medium", "Media"
        HIGH = "high", "Alta"

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        REVIEW = "review", "En revisión"
        IN_PROGRESS = "in_progress", "En progreso"
        COMPLETED = "completed", "Completada"
        REJECTED = "rejected", "Rechazada"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="suggestions",
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    section = models.CharField(max_length=100, blank=True, help_text="Ej: Hero, Galería, C&MC")
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    attachment = models.FileField(upload_to=suggestion_attachment_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sugerencia"
        verbose_name_plural = "Sugerencias"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class SuggestionComment(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class SuggestionHistory(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Historial de sugerencia"
        verbose_name_plural = "Historial de sugerencias"
