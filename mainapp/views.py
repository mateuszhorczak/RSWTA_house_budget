import io

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
import matplotlib.pyplot as plt
import numpy as np
# Create your views here.

from .models import Category, IncomeOperation, ExpanseOperation, Wallet
from .forms import ExpansesForm, IncomesForm, UserRegistrationForm, WalletForm, CategoryForm, DatabaseRecordForm

@login_required()
def plot_view_expanse(request, pk):
    fig, axs = plt.subplots(2, figsize=(6, 10))
    expenses = ExpanseOperation.objects.filter(wallet__pk=pk)
    incomes = IncomeOperation.objects.filter(wallet__pk=pk)

    y1 = []
    y2 = []

    for expense in expenses:
        y1.append(expense.amount)
    for income in incomes:
        y2.append(income.amount)

    x1= np.arange(1,len(y1) + 1)
    x2= np.arange(1,len(y2) + 1)

    axs[0].stem(x1, y1)
    axs[1].stem(x2, y2)
    axs[0].grid()
    axs[1].grid()
    axs[0].set_ylim(0-max(y1)/10, max(y1) + max(y1)/10)
    axs[1].set_ylim(0-max(y2)/10, max(y2) + max(y2)/10)
    axs[0].set_xlabel('Numer operacji')
    axs[1].set_xlabel('Numer operacji')
    axs[0].set_ylabel('Kwota')
    axs[1].set_ylabel('Kwota')
    axs[0].set_xticks(range(min(x1), max(x1) + 1, 1))
    axs[1].set_xticks(range(min(x2), max(x2) + 1, 1))
    for i in range(len(x1)):
        axs[0].annotate(str(y1[i]), xy=(x1[i], y1[i]), xytext=(x1[i], y1[i] + 2), ha='center')
    for i in range(len(x2)):
        axs[1].annotate(str(y2[i]), xy=(x2[i], y2[i]), xytext=(x2[i], y2[i] + 2), ha='center')
    axs[0].set_title('Wydatki')
    axs[1].set_title('Przychody')

    response1 = HttpResponse(content_type='image/png')

    fig.savefig(response1, format='png')

    return response1


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
            wallet.account_balance = 0
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
                wallet=wallet,
                category=category,
                id_user=request.user
            )
            wallet.account_balance -= float(amount)
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
                wallet=wallet,
                id_user=request.user,
            )
            wallet.account_balance += float(amount)
            wallet.save()
            return HttpResponseRedirect(f"/mainapp/wallets/{wallet.name}")
    else:
        form_expanses = ExpansesForm(user=request.user, wallet=wallet.name)
        form_incomes = IncomesForm()

    context = {'wallet_name': wallet_name, 'categories_list': categories_list, 'form_expanses': form_expanses,
               'form_incomes': form_incomes, 'account_balance': wallet.account_balance,
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


@login_required(login_url='home')
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('mainapp:home_view'))
    return render(request, 'registration/login.html')


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:login_view'))


@login_required(login_url='home')
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'registration/password_reset_form.html', {'form': form})


# @login_required(login_url='home')
def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'registration/registration_form.html', context)
