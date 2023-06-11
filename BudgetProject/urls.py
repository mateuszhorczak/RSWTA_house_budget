"""
URL configuration for BudgetProject project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView

from mainapp.views import registration_view, CustomLoginView, CustomPasswordResetView, CustomPasswordResetDoneView, \
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', RedirectView.as_view(url='accounts/login/')),

    re_path(r'^favicon\.ico$', RedirectView.as_view(url='mainapp/home')),
    # nie wiem po co to, ale nie krzyczy przegladarka
    path("accounts/register/", registration_view, name='registration'),
    path("accounts/login/", CustomLoginView.as_view(), name='login'),
    path("accounts/password_reset/", CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),
    path('accounts/reset/done', CustomPasswordResetCompleteView.as_view(), name='custom_password_reset_complete'),
    path('mainapp/', include('mainapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
