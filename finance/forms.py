from django import forms
from .models import Income, Contract

_INPUT = {"class": "field-input"}


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["project", "client", "concept", "amount", "date", "status", "notes"]
        widgets = {
            "project": forms.TextInput(attrs=_INPUT),
            "client": forms.TextInput(attrs=_INPUT),
            "concept": forms.TextInput(attrs=_INPUT),
            "amount": forms.NumberInput(attrs=_INPUT),
            "date": forms.DateInput(attrs={**_INPUT, "type": "date"}),
            "status": forms.Select(attrs=_INPUT),
            "notes": forms.Textarea(attrs={**_INPUT, "rows": 3}),
        }


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ["project", "client", "service", "date", "amount", "status", "notes"]
        widgets = {
            "project": forms.TextInput(attrs=_INPUT),
            "client": forms.TextInput(attrs=_INPUT),
            "service": forms.TextInput(attrs=_INPUT),
            "date": forms.DateInput(attrs={**_INPUT, "type": "date"}),
            "amount": forms.NumberInput(attrs=_INPUT),
            "status": forms.Select(attrs=_INPUT),
            "notes": forms.Textarea(attrs={**_INPUT, "rows": 3}),
        }
