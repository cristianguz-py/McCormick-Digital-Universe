"""
dashboard/views.py
Una sola vista de overview que adapta su contenido según el rol
(requisito #38: no cuatro dashboards idénticos, sino una estructura
común con datos filtrados por permiso).
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from accounts.models import User
from analytics.services import summary_for_scope, monthly_series
from core.models import ActivityLog
from core.utils import log_activity
from finance.models import Income, Contract
from suggestions.models import Suggestion


@login_required
def overview(request):
    user = request.user
    scope = None if user.is_super_admin else user.project_scope

    analytics_summary = summary_for_scope(scope=scope, days=30)
    monthly_pageviews = monthly_series(scope=scope, event_type="page_view")

    suggestions_qs = Suggestion.objects.all() if user.is_super_admin else Suggestion.objects.filter(user=user)
    pending_suggestions = suggestions_qs.filter(status=Suggestion.Status.PENDING).count()

    context = {
        "active_tab": "overview",
        "analytics_summary": analytics_summary,
        "monthly_pageviews": monthly_pageviews,
        "pending_suggestions": pending_suggestions,
        "recent_suggestions": suggestions_qs[:5],
    }

    if user.is_super_admin:
        context.update({
            "income_total": Income.objects.filter(status=Income.Status.PAID).count(),
            "contracts_total": Contract.objects.count(),
            "users_total": User.objects.count(),
            "recent_activity": ActivityLog.objects.select_related("user")[:8],
        })

    return render(request, "dashboard/overview.html", context)


@login_required
@role_required("super_admin")
def activity_log(request):
    logs = ActivityLog.objects.select_related("user")[:200]
    return render(request, "dashboard/activity.html", {"logs": logs, "active_tab": "actividad"})


@login_required
@role_required("super_admin")
def user_list(request):
    users = User.objects.all().order_by("username")
    return render(request, "dashboard/users.html", {"users": users, "active_tab": "usuarios"})


@login_required
@role_required("super_admin")
def user_toggle_active(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target == request.user:
        messages.error(request, "No puedes desactivar tu propia cuenta.")
        return redirect("dashboard:users")
    target.is_active = not target.is_active
    target.save(update_fields=["is_active"])
    log_activity(request.user, "user_toggled", {"user_id": target.id, "is_active": target.is_active})
    messages.success(request, f"Usuario {target.username} {'activado' if target.is_active else 'desactivado'}.")
    return redirect("dashboard:users")
