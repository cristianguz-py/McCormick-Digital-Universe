"""
core/context_processors.py
Centraliza CONTACT_PHONE (y otros valores globales) para que ningún
template ni archivo JS lo repita por su cuenta (requisito #37/#90 del spec).
"""
import datetime
import re
from django.conf import settings


def site_context(request):
    phone = settings.CONTACT_PHONE
    phone_ready = not re.search(r"x", phone, re.IGNORECASE)
    return {
        "SITE_NAME": settings.SITE_NAME,
        "CONTACT_PHONE": phone,
        "CONTACT_PHONE_READY": phone_ready,
        "CONTACT_PHONE_DIGITS": re.sub(r"\D", "", phone),
        "CURRENT_YEAR": datetime.date.today().year,
    }
