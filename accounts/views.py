"""
accounts/views.py
Autenticación real basada en django.contrib.auth. El "Recordarme" controla
la expiración de la sesión (si no se marca, la sesión expira al cerrar el
navegador). Cada acción relevante queda registrada en ActivityLog.
"""
from django.contrib.auth import views as auth_views, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import StyledLoginForm, StyledPasswordChangeForm
from core.utils import log_activity
from analytics.services import log_event


class McCormickLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)  # expira al cerrar el navegador
        log_activity(self.request.user, "login", metadata={"via": "formulario"})
        log_event("login", request=self.request, user=self.request.user)
        return response


@login_required
def logout_view(request):
    log_activity(request.user, "logout")
    log_event("logout", request=request, user=request.user)
    django_logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("core:home")


@login_required
def profile_view(request):
    return render(request, "dashboard/profile.html", {"active_tab": "perfil"})


class McCormickPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "dashboard/profile_password.html"
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        log_activity(self.request.user, "password_changed")
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return response
