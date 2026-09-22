"""
python manage.py seed_demo

Crea datos DEMO explícitamente marcados como tales, para poder mostrar
los dashboards con contenido antes de tener datos reales. Es independiente
de `seed` (usuarios reales) y fácil de omitir en producción: simplemente
no se ejecuta este comando.

Nunca ejecutar en producción si no quieres datos ficticios visibles.
"""
from datetime import date, timedelta
from django.core.management.base import BaseCommand

from accounts.models import User
from analytics.models import AnalyticsEvent, EventType
from finance.models import Income, Contract
from suggestions.models import Suggestion, SuggestionHistory


class Command(BaseCommand):
    help = "Crea datos DEMO (claramente marcados) para probar los dashboards."

    def handle(self, *args, **options):
        try:
            maco = User.objects.get(username="maco.admin")
            cristian = User.objects.get(username="cristian.admin")
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                "Ejecuta primero `python manage.py seed` para crear los usuarios."
            ))
            return

        # Analítica demo
        today = date.today()
        for i in range(10):
            AnalyticsEvent.objects.create(
                event_type=EventType.PAGE_VIEW, page="maco",
                metadata={"demo": True},
                created_at=today - timedelta(days=i),
            )

        # Sugerencia demo
        suggestion, created = Suggestion.objects.get_or_create(
            user=maco, title="[DATOS DEMO] Cambiar foto del Hero",
            defaults={"description": "Ejemplo de sugerencia de demostración.", "section": "Hero"},
        )
        if created:
            SuggestionHistory.objects.create(
                suggestion=suggestion, user=maco, description="[DATOS DEMO] Sugerencia creada",
            )

        # Ingreso y contratación demo
        Income.objects.get_or_create(
            project="Maco", client="[DEMO] Cliente de ejemplo", concept="[DATOS DEMO] Presentación en vivo",
            defaults={"amount": 500000, "date": today, "status": Income.Status.PAID},
        )
        Contract.objects.get_or_create(
            project="Maco", client="[DEMO] Cliente de ejemplo", service="[DATOS DEMO] Show privado",
            defaults={"amount": 800000, "date": today, "status": Contract.Status.CONFIRMED},
        )

        self.stdout.write(self.style.SUCCESS(
            "Datos DEMO creados. Están marcados con '[DATOS DEMO]' / '[DEMO]' — "
            "bórralos antes de pasar a producción."
        ))
