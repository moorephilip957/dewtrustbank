# forms.py

from django import forms
from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):

    class Meta:
        model = LoanApplication

        fields = [
            'loan_type',
            'amount',
            'duration_months',
            'purpose',
            'monthly_net_income',
        ]

        widgets = {

            'loan_type': forms.Select(attrs={
                'class': 'form-select custom_css'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control custom_css',
                'placeholder': 'Enter loan amount',
                'min': '0',
                'step': '0.01'
            }),

            'duration_months': forms.Select(
                choices=[
                    (6, '6 Months'),
                    (12, '12 Months'),
                    (24, '24 Months'),
                    (36, '36 Months'),
                    (48, '48 Months'),
                    (60, '60 Months'),
                ],
                attrs={
                    'class': 'form-select custom_css'
                }
            ),

            'purpose': forms.Textarea(attrs={
                'class': 'form-control custom_css',
                'placeholder': 'Please describe the purpose of this loan...',
                'rows': 5
            }),

            'monthly_net_income': forms.Select(attrs={
                'class': 'form-select custom_css'
            }),
        }

        labels = {
            'amount': 'Loan Amount',
            'duration_months': 'Duration (Months)',
            'loan_type': 'Credit Facility',
            'purpose': 'Purpose of Loan',
            'monthly_net_income': 'Monthly Net Income',
        }