"""
suggestions/views.py
Reglas de permisos:
- artist/marketing: ven y crean sólo SUS sugerencias.
- super_admin (Cristian): ve todas, puede comentar y cambiar el estado.
Toda acción relevante queda en SuggestionHistory y en ActivityLog.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SuggestionForm, SuggestionCommentForm
from .models import Suggestion, SuggestionHistory
from core.utils import log_activity
from analytics.services import log_event


def _visible_suggestions(user):
    if user.is_super_admin:
        return Suggestion.objects.all()
    return Suggestion.objects.filter(user=user)


@login_required
def suggestion_list(request):
    suggestions = _visible_suggestions(request.user).select_related("user")
    return render(request, "dashboard/suggestions.html", {
        "suggestions": suggestions,
        "active_tab": "sugerencias",
    })


@login_required
def suggestion_create(request):
    if request.method == "POST":
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
            SuggestionHistory.objects.create(
                suggestion=suggestion, user=request.user,
                description=f"{request.user.display_name} creó la sugerencia",
            )
            log_activity(request.user, "suggestion_created", {"suggestion_id": suggestion.id})
            log_event("suggestion_created", request=request, user=request.user)
            messages.success(request, "Sugerencia enviada correctamente.")
            return redirect("suggestions:list")
    else:
        form = SuggestionForm()
    return render(request, "dashboard/new_suggestion.html", {
        "form": form, "active_tab": "sugerencias",
    })


@login_required
def suggestion_detail(request, pk):
    suggestion = get_object_or_404(_visible_suggestions(request.user), pk=pk)

    if request.method == "POST":
        if "submit_comment" in request.POST:
            comment_form = SuggestionCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.suggestion = suggestion
                comment.user = request.user
                comment.save()
                SuggestionHistory.objects.create(
                    suggestion=suggestion, user=request.user,
                    description=f"{request.user.display_name} respondió",
                )
                log_activity(request.user, "suggestion_comment_added", {"suggestion_id": suggestion.id})
                messages.success(request, "Comentario agregado.")
        elif "status" in request.POST:
            if not request.user.is_super_admin:
                return HttpResponseForbidden("Sólo el administrador puede cambiar el estado.")
            new_status = request.POST["status"]
            if new_status in Suggestion.Status.values:
                suggestion.status = new_status
                suggestion.save(update_fields=["status", "updated_at"])
                SuggestionHistory.objects.create(
                    suggestion=suggestion, user=request.user,
                    description=f"{request.user.display_name} cambió el estado a {suggestion.get_status_display()}",
                )
                log_activity(request.user, "suggestion_status_changed", {
                    "suggestion_id": suggestion.id, "status": new_status,
                })
                log_event("suggestion_updated", request=request, user=request.user)
                messages.success(request, "Estado actualizado.")
        return redirect("suggestions:detail", pk=pk)

    return render(request, "dashboard/suggestion_detail.html", {
        "suggestion": suggestion,
        "comment_form": SuggestionCommentForm(),
        "active_tab": "sugerencias",
        "statuses": Suggestion.Status.choices,
    })
