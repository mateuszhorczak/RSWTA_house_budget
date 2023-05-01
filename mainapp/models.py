from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


# Create your models here.

class Wallet(models.Model):
    name = models.TextField()


class Category(models.Model):
    name = models.TextField()
    id_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)


class Finance(models.Model):
    name = models.TextField()
    description = models.TextField()
    cost = models.FloatField()
    id_user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
