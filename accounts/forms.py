"""
accounts/forms.py
Reutiliza los formularios seguros nativos de Django (AuthenticationForm,
PasswordChangeForm) y sólo les agrega clases CSS para el look McCormick.
No se reimplementa la validación de credenciales: eso lo hace Django.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class StyledLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=True, label="Recordarme")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "field-input", "placeholder": "Usuario", "autofocus": True,
        })
        self.fields["password"].widget.attrs.update({
            "class": "field-input", "placeholder": "Contraseña",
        })
        self.error_messages["invalid_login"] = (
            "Usuario o contraseña incorrectos."
        )


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "field-input"})
