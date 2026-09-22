from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("", views.income_list, name="income_list"),
    path("<int:pk>/editar/", views.income_edit, name="income_edit"),
    path("contrataciones/", views.contract_list, name="contract_list"),
    path("contrataciones/<int:pk>/editar/", views.contract_edit, name="contract_edit"),
]
