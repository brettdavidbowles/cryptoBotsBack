# Generated by Django 3.2 on 2022-05-28 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20220528_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactioncalculations',
            name='market_profit_margin',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
