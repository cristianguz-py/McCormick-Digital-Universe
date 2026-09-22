"""
finance/models.py
Ingresos y contrataciones. Gestión exclusiva del super_admin (Cristian),
protegida en las vistas con @role_required('super_admin').
"""
from django.db import models


class Income(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PAID = "paid", "Pagado"
        CANCELLED = "cancelled", "Cancelado"

    project = models.CharField("Persona/Proyecto", max_length=100)
    client = models.CharField("Cliente", max_length=150)
    concept = models.CharField("Concepto", max_length=200)
    amount = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    date = models.DateField("Fecha")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField("Notas", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return f"{self.project} — {self.concept} — ${self.amount}"


class Contract(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        CONFIRMED = "confirmed", "Confirmada"
        DONE = "done", "Realizada"
        CANCELLED = "cancelled", "Cancelada"

    project = models.CharField("Persona/Proyecto", max_length=100)
    client = models.CharField("Cliente", max_length=150)
    service = models.CharField("Servicio/Evento", max_length=200)
    date = models.DateField("Fecha")
    amount = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField("Notas", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Contratación"
        verbose_name_plural = "Contrataciones"

    def __str__(self):
        return f"{self.project} — {self.service}"
