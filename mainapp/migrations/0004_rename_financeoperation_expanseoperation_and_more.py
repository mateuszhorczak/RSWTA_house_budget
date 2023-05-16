# Generated by Django 4.1.9 on 2023-05-16 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_remove_financeoperation_id_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FinanceOperation',
            new_name='ExpanseOperation',
        ),
        migrations.CreateModel(
            name='IncomeOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('amount', models.FloatField()),
                ('description', models.TextField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.category')),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.wallet')),
            ],
        ),
    ]
