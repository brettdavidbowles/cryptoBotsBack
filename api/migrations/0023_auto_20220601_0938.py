# Generated by Django 3.2 on 2022-06-01 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20220528_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactioncalculations',
            name='cumulative_expense',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='transactioncalculations',
            name='transaction_expense',
            field=models.FloatField(null=True),
        ),
    ]
