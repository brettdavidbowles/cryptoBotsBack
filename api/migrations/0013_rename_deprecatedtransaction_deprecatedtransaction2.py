# Generated by Django 3.2 on 2022-04-20 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_rename_deprecatedtransaction2_deprecatedtransaction'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeprecatedTransaction',
            new_name='DeprecatedTransaction2',
        ),
    ]
