from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "subject",
            "priority",
            "message",
        ]

        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "form-control-custom",
                "id": "subject",
                "placeholder": "Briefly describe your issue",
                "autocomplete": "off"
            }),

            "priority": forms.Select(attrs={
                "class": "form-select-custom",
                "id": "selectPriority",
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control-custom preserveLines",
                "id": "message",
                "placeholder": "Please provide all relevant details about your issue so we can help you better",
                "autocomplete": "off",
                "rows": 2
            }),
        }