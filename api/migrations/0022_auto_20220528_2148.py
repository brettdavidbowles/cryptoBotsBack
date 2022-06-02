# Generated by Django 3.2 on 2022-05-28 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_transactioncalculations_market_profit_margin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactioncalculations',
            name='cumulative_profit',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transactioncalculations',
            name='cumulative_profit_margin',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transactioncalculations',
            name='market_profit_margin',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transactioncalculations',
            name='transaction_profit',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='transactioncalculations',
            name='transaction_profit_margin',
            field=models.FloatField(null=True),
        ),
    ]