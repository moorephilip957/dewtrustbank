from django import forms
from .models import KYCVerification


class KYCVerificationForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = KYCVerification

        fields = '__all__'

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+15167658976'
            }),

            'title': forms.Select(attrs={
                'class': 'form-select'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            'zipcode': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'ssn': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'account_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'employment_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'annual_income_range': forms.Select(attrs={
                'class': 'form-select'
            }),

            'address_line': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'state': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'value': 'United States of America'
            }),

            'beneficiary_legal_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'next_of_kin_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'relationship': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'document_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'upload_front_side': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'upload_back_side': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'passport_photograph': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }