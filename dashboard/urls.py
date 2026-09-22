from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("actividad/", views.activity_log, name="activity"),
    path("usuarios/", views.user_list, name="users"),
    path("usuarios/<int:pk>/toggle/", views.user_toggle_active, name="user_toggle"),
]
