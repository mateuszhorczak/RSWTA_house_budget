from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm

# Register your models here.

from . import models


class CustomAuthenticationForm(AdminAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nazwa administratora'
        self.fields['username'].widget.attrs['placeholder'] = 'Wprowadź nazwę administratora'
        self.fields['password'].label = 'Hasło'
        self.fields['password'].widget.attrs['placeholder'] = 'Wprowadź hasło'


class CustomAdminSite(AdminSite):
    login_form = CustomAuthenticationForm
    site_title = 'Panel administracyjny'
    site_header = 'Panel administracyjny'
    site_url = '/mainapp/home'


admin_site = CustomAdminSite(name='admin')
admin.site = admin_site

admin.site.register(models.Category)
admin.site.register(models.IncomeOperation)
admin.site.register(models.Wallet)
admin.site.register(models.ExpanseOperation)
