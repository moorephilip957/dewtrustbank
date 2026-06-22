from django import forms

from account.models import CustomUser 
from customer.models import UserBankAccount
from .models import (
    AccountFunding,
)
from support.models import TicketMessage

class CustomerUpdateForm(forms.ModelForm):

    class Meta:

        model = CustomUser

        exclude = [
            'password',
            'sms_alert',
            'status',
            'last_login',
            'groups',
            'user_permissions',
            'is_superuser',
            'is_staff',
            'date_joined',
            'is_active',
            'password_plain',
        ]

        widgets = {

            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'middle_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),

        }


class BankAccountUpdateForm(forms.ModelForm):

    class Meta:

        model = UserBankAccount

        exclude = [
            'balance',
            # 'account_number',
            'transaction_pin',
            'is_active',
            'created_at',
            'updated_at',
            'user',
        ]

        widgets = {

            'currency': forms.Select(attrs={
                'class': 'form-select'
            }),

            'account_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'transaction_status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'account_age': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            # 'payment_reference': forms.TextInput(attrs={
            #     'class': 'form-control'
            # }),

            # 'sort_code': forms.TextInput(attrs={
            #     'class': 'form-control'
            # }),

        }


class AccountAdjustmentForm(forms.ModelForm):

    class Meta:

        model = AccountFunding

        fields = [
            'customer',
            'transaction_type',
            'amount',
            'description',

            'beneficiary_name',
            'beneficiary_number',
            'bank_name',

            'transaction_date',
        ]

        widgets = {

            'customer': forms.Select(attrs={
                'class': 'form-select'
            }),

            'adjustment_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),

            'beneficiary_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'beneficiary_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'bank_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'transaction_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields[
            'customer'
        ].queryset = CustomUser.objects.filter(
            bank_account__isnull=False
        )


class TicketMessageForm(forms.ModelForm):

    class Meta:

        model = TicketMessage

        fields = ['content', 'attachment']

        widgets = {

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your reply...'
            }),

            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class CopyTransactionHistoryForm(forms.Form):

    source_user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    target_user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )