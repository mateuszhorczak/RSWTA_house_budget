from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import io
# Create your views here.

from .models import Category, IncomeOperation, ExpanseOperation, Wallet
from .forms import ExpansesForm, IncomesForm, UserRegistrationForm, WalletForm, CategoryForm, DatabaseRecordForm, \
    CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm


@login_required()
def expanse_plot_view(request, pk):
    fig, ax = plt.subplots(figsize=(12, 6))
    expenses = ExpanseOperation.objects.filter(wallet__pk=pk)
    y = []

    for expense in expenses:
        y.append(expense.amount)
    x = np.arange(1, len(y) + 1)

    ax.stem(x, y)
    ax.grid()
    ax.set_ylim(0 - max(y) / 10, max(y) + max(y) / 10)
    ax.set_xlabel('Numer operacji')
    ax.set_ylabel('Kwota')
    ax.set_xticks(range(min(x), max(x) + 1, 1))
    for i in range(len(x)):
        ax.annotate(str(y[i]), xy=(x[i], y[i]), xytext=(x[i], y[i] + 2), ha='center')

    ax.set_title('Wydatki')

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    response = HttpResponse(content_type='image/png')

    fig.savefig(response, format='png')

    return response


@login_required()
def income_plot_view(request, pk):
    fig, ax = plt.subplots(figsize=(12, 6))
    incomes = IncomeOperation.objects.filter(wallet__pk=pk)
    y = []
    for income in incomes:
        y.append(income.amount)

    x = np.arange(1, len(y) + 1)

    ax.stem(x, y)
    ax.grid()
    ax.set_ylim(0 - max(y) / 10, max(y) + max(y) / 10)
    ax.set_xlabel('Numer operacji')
    ax.set_ylabel('Kwota')
    ax.set_xticks(range(min(x), max(x) + 1, 1))
    for i in range(len(x)):
        ax.annotate(str(y[i]), xy=(x[i], y[i]), xytext=(x[i], y[i] + 2), ha='center')
    ax.set_title('Przychody')

    response = HttpResponse(content_type='image/png')

    fig.savefig(response, format='png')

    return response


def balance_plot_view(request, pk):
    fig, ax = plt.subplots(figsize=(12, 6))
    incomes = IncomeOperation.objects.filter(wallet__pk=pk)
    expanses = ExpanseOperation.objects.filter(wallet__pk=pk)

    data = {}

    for income in incomes:
        data[income.operation_date] = income.amount_wallet_after

    for expanse in expanses:
        data[expanse.operation_date] = expanse.amount_wallet_after

    sorted_keys = sorted(data.keys())
    print(sorted_keys)
    new_data = {}
    for key in sorted_keys:
        key_start = key
        key = key.strftime('%y-%m-%d\n%H:%M:%S')
        new_data[key] = data[key_start]

    keys = list(new_data.keys())
    values = list(new_data.values())

    ax.stem(keys, values)
    ax.grid()
    ax.set_xlabel('Data')
    ax.set_ylabel('Saldo')
    for i in range(len(keys)):
        ax.annotate(str(values[i]), xy=(keys[i], values[i]), xytext=(keys[i], values[i] + 2), ha='center')
    ax.set_title('Ostatnie Stany Salda Portfela')

    response = HttpResponse(content_type='image/png')

    fig.savefig(response, format='png')

    return response


@login_required()
def home_view(request):
    username = request.user.username
    if request.method == 'POST':
        form_database_record = DatabaseRecordForm(request.POST, user=request.user)
        if form_database_record.is_valid():
            expense_operations, income_operations = form_database_record.search(request.user)
            operations = list(expense_operations) + list(income_operations)
            context = {'username': username, 'form_database_record': form_database_record, 'operations': operations}
            return render(request, 'home.html', context)
    else:
        form_database_record = DatabaseRecordForm(user=request.user)

    context = {'username': username, 'form_database_record': form_database_record}
    return render(request, 'home.html', context)


@login_required()
def wallets_view(request):
    if request.method == 'POST':
        form_wallet = WalletForm(request.POST, user=request.user)
        if form_wallet.is_valid():
            wallet = form_wallet.save(commit=False)
            wallet.id_user = request.user
            wallet.save()
            form_wallet.instance.categories.set(form_wallet.cleaned_data['categories'])
            return HttpResponseRedirect("/mainapp/wallets")
    else:
        form_wallet = WalletForm()
    form_wallet.fields['categories'].queryset = Category.objects.filter(id_user=request.user)
    wallets_list = Wallet.objects.filter(id_user=request.user)
    context = {'wallets_list': wallets_list, 'form_wallet': form_wallet}
    return render(request, 'wallets.html', context)


@login_required()
def wallet_view(request, wallet_name):
    wallet = Wallet.objects.get(name=wallet_name)
    account_balance = wallet.get_account_balance()
    categories_list = wallet.categories.filter(id_user=request.user)

    if request.method == 'POST':
        form_expanses = ExpansesForm(request.POST, user=request.user, wallet=wallet.name)
        form_incomes = IncomesForm(request.POST)
        if form_expanses.is_valid():
            title = form_expanses.cleaned_data['title']
            amount = form_expanses.cleaned_data['amount']
            description = form_expanses.cleaned_data['description']
            category = form_expanses.cleaned_data['category']
            expanse_operation = ExpanseOperation.objects.create(
                title=title,
                description=description,
                amount=amount,
                amount_wallet_after=account_balance - amount,
                wallet=wallet,
                category=category,
                id_user=request.user
            )
            wallet.save()
            return HttpResponseRedirect(f"/mainapp/wallets/{wallet.name}")
        if form_incomes.is_valid():
            title = form_incomes.cleaned_data['title']
            amount = form_incomes.cleaned_data['amount']
            description = form_incomes.cleaned_data['description']

            income_operation = IncomeOperation.objects.create(
                title=title,
                description=description,
                amount=amount,
                amount_wallet_after=account_balance + amount,
                wallet=wallet,
                id_user=request.user,
            )
            wallet.save()
            return HttpResponseRedirect(f"/mainapp/wallets/{wallet.name}")
    else:
        form_expanses = ExpansesForm(user=request.user, wallet=wallet.name)
        form_incomes = IncomesForm()

    context = {'wallet_name': wallet_name, 'categories_list': categories_list, 'form_expanses': form_expanses,
               'form_incomes': form_incomes, 'account_balance': wallet.get_account_balance(),
               'wallet_id': wallet.pk}
    return render(request, 'wallet.html', context)


@login_required()
def categories_view(request):
    if request.method == 'POST':
        form_category = CategoryForm(request.POST)
        if form_category.is_valid():
            category = form_category.save(commit=False)
            category.id_user = request.user
            category.save()
            return HttpResponseRedirect('/mainapp/categories')
    else:
        form_category = CategoryForm()
    categories_list = Category.objects.filter(id_user=request.user)
    context = {'categories_list': categories_list, 'form_category': form_category}
    return render(request, 'categories.html', context)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login')
        else:
            return HttpResponseRedirect('/accounts/register')
    else:
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'registration/registration_form.html', context)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'registration/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
