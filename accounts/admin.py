from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class McCormickUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "name", "role", "is_active", "is_staff", "created_at")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("McCormick", {"fields": ("name", "role")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("McCormick", {"fields": ("name", "role")}),
    )
