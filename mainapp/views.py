from django.shortcuts import render

# Create your views here.

from . models import Category, Expense, Wallet


def wallets(request, wallet_name):
    wallets_list = Wallet.objects.filter(name=wallet_name)
    context = {'wallet_name': wallet_name, 'wallets_list': wallets_list}
    return render(request, "wallet.html", context)
