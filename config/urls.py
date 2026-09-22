"""
config/urls.py
Enrutador raíz. Une las URLs públicas (core), autenticación (accounts),
panel privado (dashboard) y sus módulos (suggestions, analytics, finance).
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

handler404 = "core.views.error_404"
handler403 = "core.views.error_403"
handler500 = "core.views.error_500"

urlpatterns = [
    path("admin/", admin.site.urls),

    # Público
    path("", include("core.urls")),

    # Autenticación real (Django auth, no localStorage)
    path("", include("accounts.urls")),

    # Panel privado
    path("dashboard/", include("dashboard.urls")),
    path("dashboard/sugerencias/", include("suggestions.urls")),
    path("dashboard/ingresos/", include("finance.urls")),

    # Endpoint AJAX de analytics (usado por static/js/analytics.js)
    path("analytics/", include("analytics.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
