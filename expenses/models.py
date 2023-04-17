from django.db import models


# Create your models here.

class Expense(models.Model):
    name = models.TextField()
    description = models.TextField()
    cost = models.TextField()
