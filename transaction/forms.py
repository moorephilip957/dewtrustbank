# forms.py
from django import forms
from django.contrib.auth.hashers import check_password

from .models import Deposit, LocalTransfer, InternationalTransfer, TransactionHistory
from customer.models import UserBankAccount


class DepositCreateForm(forms.ModelForm):

    class Meta:
        model = Deposit

        fields = [
            "method",
            "amount"
        ]

        widgets = {

            # HIDDEN FIELD
            "method": forms.HiddenInput(),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "100",
                    "max": "5000000",
                    "step": "0.01",
                    "placeholder": "0.00"
                }
            )
        }

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        if amount < 100:
            raise forms.ValidationError(
                "Minimum deposit is $100"
            )

        if amount > 5000000:
            raise forms.ValidationError(
                "Maximum deposit is $5,000,000"
            )

        return amount


class DepositProofForm(forms.ModelForm):

    class Meta:
        model = Deposit
        fields = ["proof"]

        widgets = {
            "proof": forms.FileInput(
                attrs={
                    "hidden": True,
                    "id": "fileInput",
                    "accept": "image/*,.pdf",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["proof"].required = True
    

class LocalTransferForm(forms.ModelForm):

    transfer_pin = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control-custom",
                "placeholder": "Enter your transfer PIN",
                "autocomplete": "off",
            }
        )
    )

    class Meta:

        model = LocalTransfer

        fields = [
            "beneficiary_name",
            "beneficiary_number",
            "bank_name",
            "transfer_type",
            "amount",
            "description"
        ]

        widgets = {

            "beneficiary_name": forms.TextInput(
                attrs={
                    "class": "form-control-custom",
                    "placeholder": "Enter beneficiary's full name"
                }
            ),

            "beneficiary_number": forms.TextInput(
                attrs={
                    "class": "form-control-custom",
                    "placeholder": "Enter account number"
                }
            ),

            "bank_name": forms.TextInput(
                attrs={
                    "class": "form-control-custom",
                    "placeholder": "Enter bank name"
                }
            ),

            "transfer_type": forms.Select(
                attrs={
                    "class": "form-select-custom"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control-custom amount-input",
                    "min": "1",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control-custom",
                    "rows": 3,
                    "placeholder": "Enter transaction description or purpose of payment",
                    "style": "padding-top: 0.875rem; padding-bottom: 0.875rem; min-height: 100px; resize: vertical;"
                }
            )
        }

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        amount = cleaned_data.get("amount")
        pin = cleaned_data.get("transfer_pin")
        account_number = cleaned_data.get(
            "beneficiary_account_number"
        )

        try:
            account = UserBankAccount.objects.get(user=self.user)

        except UserBankAccount.DoesNotExist:

            raise forms.ValidationError(
                "Account not found."
            )

        # CHECK BALANCE
        if amount and amount > account.balance:

            raise forms.ValidationError(
                "Insufficient balance."
            )

        # CHECK PIN
        if pin and not check_password(
            pin,
            account.transaction_pin
        ):

            raise forms.ValidationError(
                "Invalid transfer PIN."
            )

        # VALIDATE ACCOUNT NUMBER
        if account_number and len(account_number) < 10:

            raise forms.ValidationError(
                "Invalid account number."
            )

        return cleaned_data
    

class InternationalTransferForm(forms.ModelForm):

    transfer_pin = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control my-input",
                "placeholder": "Enter 6-10 digit PIN",
                "minlength": "4",
                "maxlength": "10"
            }
        )
    )

    class Meta:

        model = InternationalTransfer

        fields = [
            "beneficiary_name",
            "beneficiary_number",
            "bank_name",
            "bank_address",
            "country",
            "swift_code",
            "iban_number",
            "amount",
            "description"
        ]

        widgets = {

            "beneficiary_name": forms.TextInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "Enter beneficiary's full name"
                }
            ),

            "beneficiary_number": forms.TextInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "Enter account number"
                }
            ),

            "bank_name": forms.TextInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "Enter bank name"
                }
            ),

            "bank_address": forms.Textarea(
                attrs={
                    "class": "form-control my-input",
                    "rows": 1,
                    "placeholder": "Enter bank address"
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "Enter beneficiary country"
                }
            ),

            "swift_code": forms.TextInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "SWIFT/BIC"
                }
            ),

            "iban_number": forms.TextInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "Enter IBAN number"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control border-start-0 ps-0 fw-bold",
                    "placeholder": "0.00",
                    "min": "1",
                    "step": "0.01",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control my-input",
                    "rows": 3,
                    "placeholder": "Optional payment description"
                }
            )
        }

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):

        cleaned_data = super().clean()

        amount = cleaned_data.get("amount")
        pin = cleaned_data.get("transfer_pin")

        account = UserBankAccount.objects.get(user=self.user)

        if amount and amount > account.balance:

            raise forms.ValidationError(
                "Insufficient balance."
            )

        if pin and not check_password(
            pin,
            account.transaction_pin
        ):

            raise forms.ValidationError(
                "Invalid transfer PIN."
            )

        return cleaned_data
    

class TransactionHistoryForm(forms.ModelForm):

    class Meta:
        model = TransactionHistory

        fields = [
            'transaction_type',
            'amount',
            'status',
            'direction',
            'description',
            'beneficiary_name',
            'beneficiary_number',
            'bank_name',
            'created_at',   
        ]

        widgets = {
            'transaction_type': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'status': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'direction': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'balance_before': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'balance_after': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'beneficiary_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'beneficiary_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'bank_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'created_at': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                },
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # format datetime for datetime-local input
        if self.instance and self.instance.created_at:
            self.initial['created_at'] = (
                self.instance.created_at.strftime('%Y-%m-%dT%H:%M')
            )