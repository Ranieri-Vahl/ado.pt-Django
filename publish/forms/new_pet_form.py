from django import forms

from publish.models import Pet
from utils.forms_validators import msgrequired


class NewPetForm(forms.ModelForm):        

    name = forms.CharField(
        error_messages=msgrequired,
        label='Name:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type the pet name...',
            'class': 'form-control',
        }),
        )

    description = forms.CharField(
        error_messages=msgrequired,
        label='Description:',
        widget=forms.Textarea(attrs={
            'placeholder': 'Description of the pet...',
            'class': 'form-control',
        }),
        )

    state = forms.CharField(
        error_messages=msgrequired,
        label='State:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type the pet state...',
            'class': 'form-control',
        }),
        )

    city = forms.CharField(
        error_messages=msgrequired,
        label='City:',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type the pet city...',
            'class': 'form-control',
        }),
        )

    phone_number = forms.CharField(
        max_length=11,
        min_length=8,
        error_messages=msgrequired,
        label='Phone Number:',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Type your phone number...',
            'class': 'form-control',
        }),
        )

    class Meta:
        model = Pet
        fields = 'picture', 'name', 'description', 'state', 'city', 
        'phone_number' 
        widgets = {
            'picture': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }       
