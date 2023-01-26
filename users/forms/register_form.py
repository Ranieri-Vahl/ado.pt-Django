from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.forms_validators import (email_validation, msgrequired,
                                    strong_password)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        error_messages=msgrequired,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password',
            'class': 'form-control',
        }),
        validators=[strong_password]
        )

    password2 = forms.CharField(
        error_messages=msgrequired,
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'class': 'form-control',
        })
        )

    username = forms.CharField(
        error_messages=msgrequired,
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your Name',
            'class': 'form-control',
        }),
        )

    email = forms.EmailField(
        error_messages=msgrequired,
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Type your E-mail',
            'class': 'form-control',
        }),
        validators={email_validation},
        )

    class Meta:
        
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        password2 = cleaned.get('password2')
        if password != password2:
            raise ValidationError({
                'password': 'The passwords must be equal!',
                'password2': 'The passwords must be equal!'
            })
        return cleaned