"""
suggestions/forms.py
Validación real en backend (no sólo frontend), incluida la del archivo
adjunto (extensión y tamaño), según settings.ALLOWED_UPLOAD_EXTENSIONS.
"""
import os
from django import forms
from django.conf import settings
from .models import Suggestion, SuggestionComment


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ["title", "description", "section", "priority", "attachment"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "field-input", "placeholder": "Título"}),
            "description": forms.Textarea(attrs={"class": "field-input", "rows": 5, "placeholder": "Describe tu idea o solicitud"}),
            "section": forms.TextInput(attrs={"class": "field-input", "placeholder": "Sección (ej. Hero, Galería)"}),
            "priority": forms.Select(attrs={"class": "field-input"}),
        }

    def clean_attachment(self):
        file = self.cleaned_data.get("attachment")
        if not file:
            return file
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            raise forms.ValidationError(
                f"Extensión no permitida. Usa: {', '.join(settings.ALLOWED_UPLOAD_EXTENSIONS)}"
            )
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file.size > max_bytes:
            raise forms.ValidationError(f"El archivo supera {settings.MAX_UPLOAD_SIZE_MB}MB.")
        return file


class SuggestionCommentForm(forms.ModelForm):
    class Meta:
        model = SuggestionComment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"class": "field-input", "rows": 3, "placeholder": "Escribe una respuesta..."}),
        }
