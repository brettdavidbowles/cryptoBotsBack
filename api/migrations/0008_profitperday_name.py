# Generated by Django 3.2 on 2022-04-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_profitperday'),
    ]

    operations = [
        migrations.AddField(
            model_name='profitperday',
            name='name',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
