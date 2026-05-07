from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CustomUserRegistrationForm(UserCreationForm):
    # Reorder and explicitly define fields for precise control
    first_name = forms.CharField(max_length=150, required=True)
    middle_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=True)
    username = forms.CharField(
        max_length=150,
        required=True,
        # help_text="3-20 characters: letters, numbers, underscores"
    )
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    country = CountryField().formfield(
                required=False,
                initial='US',
                widget=CountrySelectWidget(attrs={
                    'class': 'form-control form-control-custom'
                })
            )
    password1 = forms.CharField(
                widget=forms.PasswordInput(attrs={
                    'id': 'password'
                })
            )
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'middle_name', 'last_name', 'username',
            'email', 'phone_number', 'country', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply your exact CSS classes and structure to every field
        for field_name, field in self.fields.items():
            if field_name in ['password1', 'password2']:
                field.widget.attrs.update({
                    'class': 'form-control form-control-custom',
                    'placeholder': '••••••••',
                    'minlength': '8',
                    'required': 'required'
                })
            elif field_name == 'phone_number':
                field.widget.attrs.update({
                    'class': 'form-control form-control-custom',
                    'type': 'tel',
                    'placeholder': '+1 (555) 123-4567'
                })
            elif field_name == 'email':
                field.widget.attrs.update({
                    'class': 'form-control form-control-custom',
                    'placeholder': 'jane@example.com',
                    'required': 'required'
                })
            elif field_name == 'username':
                field.widget.attrs.update({
                    'class': 'form-control form-control-custom',
                    'placeholder': 'jane_doe',
                    'pattern': '[a-zA-Z0-9_]{3,20}',
                    # 'title': '3-20 characters: letters, numbers, underscores',
                    'required': 'required'
                })
            else:
                # Default text inputs (first_name, middle_name, last_name)
                field.widget.attrs.update({
                    'class': 'form-control form-control-custom',
                    'placeholder': field_name.replace('_', ' ').title(),
                    'required': 'required' if field_name != 'middle_name' else ''
                })