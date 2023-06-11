from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import IncomeOperation, Wallet, Category, ExpanseOperation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm


class ExpansesForm(forms.Form):
    style = 'w-full p-2 mb-2 border-2 border-black'
    title = forms.CharField(label='Tytul operacji', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wprowadz tytul', 'class': style}))
    amount = forms.DecimalField(label='Kwota', decimal_places=2,
                                widget=forms.TextInput(attrs={'placeholder': 'Wprowadz kwote', 'class': style}))
    description = forms.CharField(label='Opis', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wprowadz opis', 'class': style}))
    category = forms.ModelChoiceField(label='Kategoria', queryset=Category.objects.none(),
                                      widget=forms.Select(attrs={'placeholder': 'Wybierz kategorię', 'class': style, }),
                                      to_field_name='name')

    def __init__(self, *args, user=None, wallet=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Wallet.objects.filter(name=wallet, id_user=user).first().categories


class IncomesForm(forms.Form):
    style = 'w-full p-2 mb-2 border-2 border-black'
    title = forms.CharField(label='Tytul operacji', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wprowadz tytul', 'class': style}))
    amount = forms.DecimalField(label='Kwota', decimal_places=2,
                                widget=forms.TextInput(attrs={'placeholder': 'Wprowadz kwote', 'class': style}))
    description = forms.CharField(label='Opis', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wprowadz opis', 'class': style}))


class WalletForm(forms.ModelForm):
    name = forms.CharField(label='Nazwa portfela', max_length=100,
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Wprowadz nazwe portfela',
                                      'class': 'border-black border-2 mb-2 p-2 w-full'}))
    categories = forms.ModelMultipleChoiceField(label='Kategorie', queryset=Category.objects.none(),
                                                widget=forms.SelectMultiple(
                                                    attrs={'class': 'border-black border-2 mb-2 w-full'}),
                                                to_field_name='name')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(id_user=user)

    class Meta:
        model = Wallet
        fields = ['name', 'categories']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Nazwa kategorii', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'Wprowadz nazwe kategorii',
                                                         'class': 'w-full p-2 mb-2 border-2 border-black'}))

    class Meta:
        model = Category
        fields = ['name']


class DatabaseRecordForm(forms.Form):
    style = 'w-full p-2 mb-2 border-2 border-black'

    title = forms.CharField(label='Tytuł operacji', max_length=100,
                            widget=forms.TextInput(attrs={'placeholder': 'Wprowadź tytuł', 'class': style}),
                            required=False)
    amount = forms.DecimalField(label='Kwota', decimal_places=2,
                                widget=forms.TextInput(attrs={'placeholder': 'Wprowadź kwotę', 'class': style}),
                                required=False)
    description = forms.CharField(label='Opis', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Wprowadź opis', 'class': style}),
                                  required=False)
    categories = forms.ModelChoiceField(label='Kategoria', queryset=Category.objects.none(),
                                        widget=forms.Select(
                                            attrs={'placeholder': 'Wybierz kategorie', 'class': style}),
                                        to_field_name='name', required=False)
    wallets = forms.ModelChoiceField(label='Portfel', queryset=Wallet.objects.none(),
                                     widget=forms.Select(attrs={'placeholder': 'Wybierz portfel', 'class': style}),
                                     to_field_name='name', required=False)
    operation_type = forms.ChoiceField(label='Typ operacji', choices=[('expense', 'Wydatek'), ('income', 'Dochód'),
                                                                      ('both', 'Oba')],
                                       widget=forms.Select(attrs={'class': style}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(id_user=user)
        self.fields['wallets'].queryset = Wallet.objects.filter(id_user=user)

    def search(self, user):
        operation_type = self.cleaned_data['operation_type']
        categories = self.cleaned_data['categories']
        wallets = self.cleaned_data['wallets']
        title = self.cleaned_data['title']
        amount = self.cleaned_data['amount']
        description = self.cleaned_data['description']

        queryset_income = IncomeOperation.objects.all().filter(id_user=user)
        queryset_expense = ExpanseOperation.objects.all().filter(id_user=user)
        if operation_type == 'expense':
            if title:
                queryset_expense = queryset_expense.filter(title__icontains=title)
            if description:
                queryset_expense = queryset_expense.filter(description__icontains=description)
            if amount:
                queryset_expense = queryset_expense.filter(amount=amount)
            if categories:
                queryset_expense = queryset_expense.filter(category__pk=categories.pk)
            if wallets:
                queryset_expense = queryset_expense.filter(wallet__pk=wallets.pk)
            return queryset_expense, []

        elif operation_type == 'income':
            if title:
                queryset_income = queryset_income.filter(title__icontains=title)
            if description:
                queryset_income = queryset_income.filter(description__icontains=description)
            if amount:
                queryset_income = queryset_income.filter(amount=amount)
            if wallets:
                queryset_income = queryset_income.filter(wallet__pk=wallets.pk)
            return [], queryset_income

        elif operation_type == 'both':

            if title:
                queryset_expense = queryset_expense.filter(title__icontains=title)
            if description:
                queryset_expense = queryset_expense.filter(description__icontains=description)
            if amount:
                queryset_expense = queryset_expense.filter(amount=amount)
            if categories:
                queryset_expense = queryset_expense.filter(category__pk=categories.pk)
            if wallets:
                queryset_expense = queryset_expense.filter(wallet__pk=wallets.pk)

            if title:
                queryset_income = queryset_income.filter(title__icontains=title)
            if description:
                queryset_income = queryset_income.filter(description__icontains=description)
            if amount:
                queryset_income = queryset_income.filter(amount=amount)
            if wallets:
                queryset_income = queryset_income.filter(wallet__pk=wallets.pk)
            return queryset_expense, queryset_income


class UserRegistrationForm(UserCreationForm):
    style = 'w-full p-2 mb-2 ml-2 border-2 border-black'
    email = forms.EmailField(label='email', max_length=100,
                             widget=forms.EmailInput(attrs={'placeholder': 'Adres email', 'class': style}))
    username = forms.CharField(help_text='',
                               widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika', 'class': style}))
    password1 = forms.CharField(help_text='',
                                widget=forms.PasswordInput(
                                    attrs={'type': 'password', 'placeholder': 'Hasło', 'class': style}))
    password2 = forms.CharField(help_text='',
                                widget=forms.PasswordInput(
                                    attrs={'type': 'password', 'placeholder': 'Powtórz hasło', 'class': style}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style = 'w-full p-2 mb-2 ml-2 border-black border-2'
        self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
        self.fields['username'].widget.attrs['class'] = style
        self.fields['password'].widget.attrs['placeholder'] = 'Hasło'
        self.fields['password'].widget.attrs['class'] = style


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Adres email'
        self.fields['email'].widget.attrs['class'] = 'w-full p-2 ml-2 border-black border-2'
