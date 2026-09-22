"""
core/views.py
Páginas públicas (no requieren login). Cada vista registra un evento
page_view real en AnalyticsEvent — nada de estadísticas inventadas.
"""
from django.shortcuts import render
from django.views.generic import TemplateView

from analytics.services import log_event


class PublicPageView(TemplateView):
    """Vista base pública que registra el evento page_view automáticamente."""
    page_name = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = self.page_name
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        log_event("page_view", request=request, page=self.page_name)
        return response


class HomeView(PublicPageView):
    template_name = "public/home.html"
    page_name = "home"


class MacoView(PublicPageView):
    template_name = "public/maco.html"
    page_name = "maco"


class CmcView(PublicPageView):
    template_name = "public/cmc.html"
    page_name = "cmc"


class MelanieView(PublicPageView):
    template_name = "public/melanie.html"
    page_name = "melanie"


# ---------------------------------------------------------------------------
# Páginas de error — nunca se muestra un traceback técnico al usuario.
# ---------------------------------------------------------------------------
def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def error_500(request):
    return render(request, "errors/500.html", status=500)
