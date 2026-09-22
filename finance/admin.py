from django.contrib import admin
from .models import Income, Contract


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("project", "client", "concept", "amount", "date", "status")
    list_filter = ("status", "project")
    search_fields = ("client", "concept")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("project", "client", "service", "amount", "date", "status")
    list_filter = ("status", "project")
    search_fields = ("client", "service")
