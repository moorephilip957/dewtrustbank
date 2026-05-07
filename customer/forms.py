from django import forms
from django.core.exceptions import ValidationError
from .models import UserBankAccount

from django import forms
from django.core.exceptions import ValidationError
from .models import UserBankAccount


class UserBankAccountForm(forms.ModelForm):

    transaction_pin = forms.CharField(
        label='Transaction PIN',
        max_length=6,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-custom',
            'placeholder': '••••',
            'pattern': '[0-9]{4,6}',
            'title': 'Enter 4-6 digit numeric PIN',
            'inputmode': 'numeric',
            'autocomplete': 'new-password'
        }),
        help_text='4-6 digit numeric PIN for authorizing transactions',
        required=True
    )

    class Meta:
        model = UserBankAccount
        fields = ['account_type', 'currency', 'transaction_pin']

        widgets = {
            'account_type': forms.Select(),
            'currency': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Apply same classes to ALL fields automatically
        for field_name, field in self.fields.items():

            field.widget.attrs.update({
                'class': 'form-control form-control-custom'
            })

            # Optional UX improvements per field
            if field_name == 'transaction_pin':
                field.widget.attrs.update({
                    'placeholder': '••••',
                })

    def clean_transaction_pin(self):
        pin = self.cleaned_data.get('transaction_pin')

        if pin and not (pin.isdigit() and 4 <= len(pin) <= 6):
            raise ValidationError('PIN must be 4-6 numeric digits only.')

        return pin

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        if user and not instance.pk:
            instance.user = user

        raw_pin = self.cleaned_data.get('transaction_pin')
        if raw_pin:
            instance.set_transaction_pin(raw_pin)

        if commit:
            instance.save()

        return instance