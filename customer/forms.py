from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import UserBankAccount, DebitCardApplication 


class UserBankAccountForm(forms.ModelForm):

    transaction_pin = forms.CharField(
        label='Transaction PIN',
        max_length=6,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-custom',
            'placeholder': '••••••',
            'pattern': '[0-9]{5-6}',
            "maxlength":"6",
            'title': 'Enter 6 digit numeric PIN',
            'inputmode': 'numeric',
            'autocomplete': 'new-password'
        }),
        help_text='6 digit numeric PIN for authorizing transactions',
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
                    'placeholder': '••••••',
                })

    def clean_transaction_pin(self):
        pin = self.cleaned_data.get('transaction_pin')
        if pin and not (pin.isdigit() and len(pin) == 6):
            raise ValidationError('PIN must be exactly 6 numeric digits.')
        # if pin and not (pin.isdigit() and 4 <= len(pin) <= 6):
        #     raise ValidationError('PIN must be 4-6 numeric digits only.')

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


class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(
        label='Current Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'current_password',
                'name': 'current_password',
                'class': 'form-control-custom',
                'placeholder': 'Enter your current password',
                'autocomplete': 'current-password',
            }
        )
    )

    password = forms.CharField(
        label='New Password',
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'name': 'password',
                'class': 'form-control-custom',
                'placeholder': 'Enter your new password',
                'autocomplete': 'new-password',
                'minlength': '8',
                'pattern': '(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}',
            }
        ),
        help_text=(
            'Password must contain at least one uppercase letter, '
            'one lowercase letter, and one number.'
        )
    )

    password_confirmation = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'password_confirmation',
                'name': 'password_confirmation',
                'class': 'form-control-custom',
                'placeholder': 'Confirm your new password',
                'autocomplete': 'new-password',
            }
        )
    )

    def __init__(self, user, *args, **kwargs):

        self.user = user

        super().__init__(*args, **kwargs)

    def clean_current_password(self):

        current_password = self.cleaned_data.get(
            'current_password'
        )

        if not self.user.check_password(
            current_password
        ):

            raise forms.ValidationError(
                'Current password is incorrect.'
            )

        return current_password

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        password_confirmation = cleaned_data.get(
            'password_confirmation'
        )

        # Check passwords match
        if password and password_confirmation:

            if password != password_confirmation:

                raise forms.ValidationError(
                    'Passwords do not match.'
                )

            # Django password validation
            validate_password(
                password,
                self.user
            )

        return cleaned_data