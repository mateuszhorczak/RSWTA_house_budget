from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Category, Finance, Wallet


def home_view(request):
    return render(request, 'home.html')


def wallets_view(request):
    wallets_list = Wallet.objects.all()
    context = {'wallets_list': wallets_list}
    return render(request, 'wallets.html', context)


def wallet_view(request, wallet_name):
    wallet = get_object_or_404(Wallet, name=wallet_name)
    wallets_list = Wallet.objects.filter(name=wallet_name)
    context = {'wallet_name': wallet_name, 'wallets_list': wallets_list}
    return render(request, 'wallet.html', context)


def categories_view(request):
    categories_list = Category.objects.all()
    context = {'categories_list': categories_list}
    return render(request, 'categories.html', context)


def finances_view(request):
    return render(request, 'finances.html')


def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    categories_list = Category.objects.filter(name=category_name)
    context = {'category_name': category_name, 'wallets_list': categories_list}
    return render(request, 'category.html', context)
