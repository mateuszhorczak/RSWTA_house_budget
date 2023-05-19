from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse

# Create your views here.

from .models import Category, IncomeOperation, ExpanseOperation, Wallet
from .forms import ExpansesForm, IncomesForm, UserRegistrationForm, WalletForm, CategoryForm


@login_required()
def home_view(request):
    username = request.user.username
    return render(request, 'home.html', {'username': username})


@login_required()
def wallets_view(request):
    if request.method == 'POST':
        form_wallet = WalletForm(request.POST)
        if form_wallet.is_valid():
            wallet = form_wallet.save(commit=False)
            wallet.id_user = request.user
            wallet.save()
            return HttpResponseRedirect("/mainapp/wallets")
    else:
        form_wallet = WalletForm()
    wallets_list = Wallet.objects.all()
    context = {'wallets_list': wallets_list, 'form_wallet': form_wallet}
    return render(request, 'wallets.html', context)


@login_required()
def wallet_view(request, wallet_name):
    wallet = Wallet.objects.get(name=wallet_name)
    categories_list = wallet.categories.all()
    context = {'wallet_name': wallet_name, 'categories_list': categories_list}
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
    categories_list = Category.objects.all()
    context = {'categories_list': categories_list, 'form_category': form_category}
    return render(request, 'categories.html', context)


@login_required()
def finances_view(request):
    if request.method == 'POST':
        form_expanses = ExpansesForm(request.POST)
        form_incomes = IncomesForm(request.POST)
        if form_expanses.is_valid():
            title = form_expanses.cleaned_data['title']
            amount = form_expanses.cleaned_data['amount']
            description = form_expanses.cleaned_data['description']
            wallet = form_expanses.cleaned_data['wallet']
            category = form_expanses.cleaned_data['category']
            expanse_operation = ExpanseOperation.objects.create(
                title=title,
                description=description,
                amount=amount,
                wallet=wallet,
                category=category
            )
            return HttpResponseRedirect("/mainapp/finances/")
        if form_incomes.is_valid():
            title = form_incomes.cleaned_data['title']
            amount = form_incomes.cleaned_data['amount']
            description = form_incomes.cleaned_data['description']
            wallet = form_incomes.cleaned_data['wallet']
            income_operation = IncomeOperation.objects.create(
                title=title,
                description=description,
                amount=amount,
                wallet=wallet,
            )
            return HttpResponseRedirect("/mainapp/finances/")
    else:
        form_expanses = ExpansesForm()
        form_incomes = IncomesForm()

    context = {'form_expanses': form_expanses, 'form_incomes': form_incomes}
    return render(request, 'finances.html', context)


@login_required()
def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    categories_list = Category.objects.filter(name=category_name)
    context = {'category_name': category_name, 'wallets_list': categories_list}
    return render(request, 'category.html', context)


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
