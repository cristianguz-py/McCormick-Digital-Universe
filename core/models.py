"""
core/models.py
ActivityLog: bitácora administrativa global (login, sugerencias, ingresos,
contrataciones, cambios de estado, etc.). Es de solo lectura desde el
dashboard; se escribe mediante core.utils.log_activity desde cada app.
"""
from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="activity_logs",
    )
    action = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Registro de actividad"
        verbose_name_plural = "Actividad"

    def __str__(self):
        who = self.user.display_name if self.user else "Sistema"
        return f"{self.created_at:%Y-%m-%d %H:%M} — {who} — {self.action}"
