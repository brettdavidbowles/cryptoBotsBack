# Generated by Django 3.2 on 2022-01-30 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_sale',
            field=models.BooleanField(default=False),
        ),
    ]
