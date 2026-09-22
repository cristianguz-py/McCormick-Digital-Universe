"""
analytics/services.py
Punto único para registrar eventos y para calcular estadísticas reales
(nunca inventadas) que consumen los dashboards.
"""
from django.utils import timezone
from datetime import timedelta

from .models import AnalyticsEvent


def log_event(event_type, request=None, user=None, page="", metadata=None):
    AnalyticsEvent.objects.create(
        event_type=event_type,
        page=page,
        user=user if getattr(user, "is_authenticated", False) else None,
        metadata=metadata or {},
    )


def summary_for_scope(scope=None, days=30):
    """
    scope: 'maco' | 'cmc' | 'melanie' | None (None = global, sólo Cristian).
    Devuelve conteos reales por tipo de evento en la ventana de días dada.
    Si no hay eventos, los conteos son 0 (nunca se inventa un número).
    """
    since = timezone.now() - timedelta(days=days)
    qs = AnalyticsEvent.objects.filter(created_at__gte=since)
    if scope:
        qs = qs.filter(page=scope)

    counts = {}
    for value, _label in AnalyticsEvent._meta.get_field("event_type").choices:
        counts[value] = qs.filter(event_type=value).count()
    counts["total"] = qs.count()
    return counts


def monthly_series(scope=None, event_type="page_view", months=6):
    """
    Serie mensual real (conteo por mes) para graficar. Si no hay datos,
    los meses aparecen con 0 — nunca se rellenan con cifras ficticias.
    """
    today = timezone.now()
    series = []
    for i in range(months - 1, -1, -1):
        month_date = (today.replace(day=1) - timedelta(days=1)) if i else today
        # Cálculo simple de mes/año hacia atrás sin dependencias externas
        month = today.month - i
        year = today.year
        while month <= 0:
            month += 12
            year -= 1
        qs = AnalyticsEvent.objects.filter(
            event_type=event_type, created_at__year=year, created_at__month=month,
        )
        if scope:
            qs = qs.filter(page=scope)
        series.append({"year": year, "month": month, "count": qs.count()})
    return series
