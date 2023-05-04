from django import forms
from .models import FinanceOperation


class ExpansesForm(forms.Form):
    title = forms.CharField(label='Tytul operacji', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Wprowadz tytul'}))
    description = forms.CharField(label='Opis', max_length=100)
    amount = forms.DecimalField(label='Kwota', decimal_places=2)


class IncomesForm(forms.Form):
    title = forms.CharField(label='Tytul operacji', max_length=100)
    description = forms.CharField(label='Opis', max_length=100)
    amount = forms.DecimalField(label='Kwota')


class NameForm(forms.Form):
    your_name = forms.CharField(label="your name", max_length=100)
