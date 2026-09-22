from django.contrib import admin
from .models import AnalyticsEvent


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "event_type", "page", "user")
    list_filter = ("event_type", "page")
    date_hierarchy = "created_at"
