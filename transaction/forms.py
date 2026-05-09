# forms.py
from django import forms
from django import forms
from django.contrib.auth.hashers import check_password

from .models import Deposit, LocalTransfer, InternationalTransfer
from customer.models import UserBankAccount


class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit

        fields = [
            "method",
            "amount",
            "proof"
        ]

        widgets = {

            "method": forms.Select(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control my-input",
                    "placeholder": "Enter amount"
                }
            ),

            "proof": forms.FileInput(
                attrs={
                    "class": "form-control my-input"
                }
            )
        }

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount <= 0:
            raise forms.ValidationError(
                "Amount must be greater than zero."
            )

        return amount
    

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
                "placeholder": "Transfer PIN"
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
                    "class": "form-control my-input"
                }
            ),

            "beneficiary_number": forms.TextInput(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "bank_name": forms.TextInput(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "bank_address": forms.Textarea(
                attrs={
                    "class": "form-control my-input",
                    "rows": 3
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "swift_code": forms.TextInput(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "iban_number": forms.TextInput(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control my-input"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control my-input",
                    "rows": 3
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
            account.transfer_pin
        ):

            raise forms.ValidationError(
                "Invalid transfer PIN."
            )

        return cleaned_data