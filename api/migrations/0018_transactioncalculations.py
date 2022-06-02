# Generated by Django 3.2 on 2022-05-25 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20220421_0140'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionCalculations',
            fields=[
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.transaction')),
                ('transaction_profit', models.FloatField()),
            ],
        ),
    ]