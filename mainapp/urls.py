from django.urls import path


from . import views

urlpatterns = [
    path("<str:wallet_name>/", views.wallets),
]
