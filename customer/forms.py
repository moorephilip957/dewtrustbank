from django import forms
from django.core.exceptions import ValidationError
from .models import UserBankAccount

from django import forms
from django.core.exceptions import ValidationError
from .models import UserBankAccount, DebitCardApplication

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
    

class DebitCardApplicationForm(forms.ModelForm):

    class Meta:
        model = DebitCardApplication

        fields = [
            'full_name',
            'email',
            'phone',
            'address',
            'card_type',
            'currency',
            'spending_limit',
            'issuance_fee',
            'delivery_method',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control form-control-custom',
                'placeholder': 'Enter your full name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-custom',
                'placeholder': 'Enter your email'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-custom',
                'placeholder': 'Enter your phone number'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control form-control-custom',
                'rows': 3,
                'placeholder': 'Enter your address'
            }),

            'card_type': forms.Select(attrs={
                'class': 'form-select-custom'
            }),

            'currency': forms.Select(attrs={
                'class': 'form-select-custom'
            }),

            'spending_limit': forms.NumberInput(attrs={
                'class': 'form-control form-control-custom',
                'placeholder': 'Enter spending limit'
            }),

            'issuance_fee': forms.Select(attrs={
                'class': 'form-select-custom'
            }),

            'delivery_method': forms.Select(attrs={
                'class': 'form-select-custom'
            }),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields['full_name'].initial = user.get_full_name()
            self.fields['email'].initial = user.email

            # optional read-only fields
            self.fields['full_name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True