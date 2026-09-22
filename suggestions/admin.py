from django.contrib import admin
from .models import Suggestion, SuggestionComment, SuggestionHistory


class CommentInline(admin.TabularInline):
    model = SuggestionComment
    extra = 0
    readonly_fields = ("user", "comment", "created_at")


class HistoryInline(admin.TabularInline):
    model = SuggestionHistory
    extra = 0
    readonly_fields = ("user", "description", "created_at")


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "section", "priority", "status", "created_at")
    list_filter = ("status", "priority", "section")
    search_fields = ("title", "description", "user__username")
    inlines = [CommentInline, HistoryInline]
