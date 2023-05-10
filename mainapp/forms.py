from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import FinanceOperation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ExpansesForm(forms.Form):
    title = forms.CharField(label='Tytul operacji', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wprowadz tytul'}))
    amount = forms.DecimalField(label='Kwota', decimal_places=2,
                                widget=forms.TextInput(attrs={'placeholder': 'Wprowadz kwote'}))
    description = forms.CharField(label='Opis', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wprowadz opis'}))


class IncomesForm(forms.Form):
    title = forms.CharField(label='Tytul operacji', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wprowadz tytul'}))
    amount = forms.DecimalField(label='Kwota', decimal_places=2,
                                widget=forms.TextInput(attrs={'placeholder': 'Wprowadz kwote'}))
    description = forms.CharField(label='Opis', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wprowadz opis'}))


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='email', max_length=100, widget=forms.EmailInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


