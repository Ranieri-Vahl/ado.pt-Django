from django import forms
from utils.forms_validators import msgrequired


class LoginForm(forms.Form):
    name = forms.CharField(
        error_messages=msgrequired,
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your name',
            'class': 'form-control',
        }),
    )

    password = forms.CharField(
        error_messages=msgrequired,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password',
            'class': 'form-control',
        }),
    )
