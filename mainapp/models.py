from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser

user_model = get_user_model()


# Create your models here.

class Wallet(models.Model):
    name = models.TextField()
    id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField()
    id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ExpanseOperation(models.Model):
    title = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)


class IncomeOperation(models.Model):
    title = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)
