from django import forms
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
