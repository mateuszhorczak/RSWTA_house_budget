from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse

# Create your views here.

from .models import Category, FinanceOperation, Wallet
from .forms import ExpansesForm, IncomesForm


@login_required()
def home_view(request):
    return render(request, 'home.html')


@login_required()
def wallets_view(request):
    wallets_list = Wallet.objects.all()
    context = {'wallets_list': wallets_list}
    return render(request, 'wallets.html', context)


@login_required()
def wallet_view(request, wallet_name):
    wallet = get_object_or_404(Wallet, name=wallet_name)
    wallets_list = Wallet.objects.filter(name=wallet_name)
    context = {'wallet_name': wallet_name, 'wallets_list': wallets_list}
    return render(request, 'wallet.html', context)


@login_required()
def categories_view(request):
    categories_list = Category.objects.all()
    context = {'categories_list': categories_list}
    return render(request, 'categories.html', context)


@login_required()
def finances_view(request):
    if request.method == 'POST':
        form_expanses = ExpansesForm(request.POST)
        form_incomes = IncomesForm(request.POST)
        if form_expanses.is_valid():
            return HttpResponseRedirect("/thanks/")
        elif form_incomes.is_valid():
            return HttpResponseRedirect("/not_thanks/")

    context = {'form_expanses': ExpansesForm(), 'form_incomes': IncomesForm()}
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/registration_form.html', context)
