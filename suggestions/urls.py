from django.urls import path
from . import views

app_name = "suggestions"

urlpatterns = [
    path("", views.suggestion_list, name="list"),
    path("nueva/", views.suggestion_create, name="create"),
    path("<int:pk>/", views.suggestion_detail, name="detail"),
]
