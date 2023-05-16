from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path("accounts/login/", auth_views.LoginView.as_view()),
    # path("accounts/logout/", auth_views.LogoutView.as_view()),

    path("home/", views.home_view, name='home'),
    path("wallets/", views.wallets_view, name='wallets'),
    path("categories/", views.categories_view, name='categories'),
    path("finances/", views.finances_view, name='finances'),
    path("wallets/<str:wallet_name>/", views.wallet_view, name='wallet'),
    path("categories/<str:category_name>/", views.category_view, name='category'),
]
