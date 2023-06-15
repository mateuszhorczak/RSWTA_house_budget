# Generated by Django 4.2.1 on 2023-06-15 23:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_expanseoperation_operation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expanseoperation',
            name='amount_wallet_after',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='incomeoperation',
            name='amount_wallet_after',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expanseoperation',
            name='operation_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='incomeoperation',
            name='operation_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='account_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
