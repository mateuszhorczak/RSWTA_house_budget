from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


# Create your models here.

class Wallet(models.Model):
    name = models.TextField()
    id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category')
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name

class FinanceOperation(models.Model):
    title = models.TextField()
    amount = models.FloatField()
    description = models.TextField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    # id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    # id_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
