from django import forms


class ExpansesForm(forms.Form):
    title = forms.CharField(label='Tytul operacji', max_length=100)
    description = forms.CharField(label='Opis', max_length=100)
    amount = forms.FloatField(label='Kwota')


class IncomesForm(forms.Form):
    title = forms.CharField(label='Tytul operacji', max_length=100)
    description = forms.CharField(label='Opis', max_length=100)
    amount = forms.FloatField(label='Kwota')
