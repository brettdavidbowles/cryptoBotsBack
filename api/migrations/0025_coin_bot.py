# Generated by Django 3.2 on 2022-07-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20220603_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='bot',
            field=models.ManyToManyField(to='api.Bot'),
        ),
    ]
