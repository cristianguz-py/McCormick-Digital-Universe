from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("maco/", views.MacoView.as_view(), name="maco"),
    path("cmc/", views.CmcView.as_view(), name="cmc"),
    path("melanie/", views.MelanieView.as_view(), name="melanie"),
]
