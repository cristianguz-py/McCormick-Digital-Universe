"""
analytics/views.py
Endpoint mínimo necesario para que el JavaScript vanilla del frontend
registre eventos reales (social_click, contact_click, gallery_open,
cta_click). No se crea una API REST completa: sólo este endpoint.
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import EventType
from .services import log_event

ALLOWED_CLIENT_EVENTS = {
    EventType.SOCIAL_CLICK, EventType.CONTACT_CLICK,
    EventType.GALLERY_OPEN, EventType.CTA_CLICK,
}


@require_POST
def track_event(request):
    """
    POST /analytics/track/  body: {"event_type": "...", "page": "...", "metadata": {...}}
    Protegido por CSRF (el JS envía el token, ver static/js/analytics.js).
    Sólo acepta los tipos de evento pensados para el frontend público.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "payload inválido"}, status=400)

    event_type = data.get("event_type")
    if event_type not in ALLOWED_CLIENT_EVENTS:
        return JsonResponse({"ok": False, "error": "evento no permitido"}, status=400)

    log_event(
        event_type,
        user=request.user if request.user.is_authenticated else None,
        page=str(data.get("page", ""))[:50],
        metadata={"note": str(data.get("metadata", ""))[:200]},
    )
    return JsonResponse({"ok": True})
