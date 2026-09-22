"""
python manage.py seed

Crea los usuarios iniciales de McCormick Digital Universe usando el
hashing seguro nativo de Django (set_password). Las contraseñas se leen
de variables de entorno cuando existen, para no depender de valores fijos
en el código. Es seguro ejecutarlo varias veces (usa update_or_create).
"""
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import User, Role


SEED_USERS = [
    {
        "username": "maco.admin",
        "name": "Jonathan McCormick (Maco)",
        "role": Role.ARTIST,
        "password_env": "SEED_PASSWORD_MACO",
        "default_password": "Maco2026!",
    },
    {
        "username": "ian.admin",
        "name": "Ian McCormick",
        "role": Role.MARKETING,
        "password_env": "SEED_PASSWORD_IAN",
        "default_password": "Ian2026!",
    },
    {
        "username": "melanie.admin",
        "name": "Melanie McCormick",
        "role": Role.ARTIST,
        "password_env": "SEED_PASSWORD_MELANIE",
        "default_password": "Melanie2026!",
    },
    {
        "username": "cristian.admin",
        "name": "Cristian Guzmán",
        "role": Role.SUPER_ADMIN,
        "password_env": "SEED_PASSWORD_CRISTIAN",
        "default_password": "CmcAdmin2026!",
        "is_staff": True,
        "is_superuser": True,
    },
]


class Command(BaseCommand):
    help = "Crea/actualiza los usuarios iniciales de McCormick Digital Universe."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in SEED_USERS:
            password = os.environ.get(data["password_env"], data["default_password"])
            user, created = User.objects.update_or_create(
                username=data["username"],
                defaults={
                    "name": data["name"],
                    "role": data["role"],
                    "is_staff": data.get("is_staff", False),
                    "is_superuser": data.get("is_superuser", False),
                    "is_active": True,
                },
            )
            user.set_password(password)  # hashing seguro de Django
            user.save()
            estado = "creado" if created else "actualizado"
            self.stdout.write(self.style.SUCCESS(f"Usuario {estado}: {user.username} ({user.role})"))

        self.stdout.write(self.style.WARNING(
            "\nRecuerda: estas contraseñas son de desarrollo. Cámbialas en "
            "producción usando SEED_PASSWORD_* en tu .env o desde el perfil "
            "de cada usuario."
        ))
