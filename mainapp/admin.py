from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Category)
admin.site.register(models.Finance)
admin.site.register(models.Wallet)
