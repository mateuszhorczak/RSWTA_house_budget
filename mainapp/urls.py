from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('wallets/', views.wallets_view, name='wallets'),
    path('categories/', views.categories_view, name='categories'),
    path('wallets/<str:wallet_name>/', views.wallet_view, name='wallet'),
    path('plot_view_expanse/<int:pk>', views.expanse_plot_view, name='plot_view_expanse'),
    path('plot_view_income/<int:pk>', views.income_plot_view, name='plot_view_income'),
    path('plot_view_balance/<int:pk>', views.balance_plot_view, name='plot_view_balance'),
]
