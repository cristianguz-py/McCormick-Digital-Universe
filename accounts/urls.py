from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.McCormickLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.profile_view, name="profile"),
    path("perfil/password/", views.McCormickPasswordChangeView.as_view(), name="password_change"),
]
