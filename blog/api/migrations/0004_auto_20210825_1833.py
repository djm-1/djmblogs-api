# Generated by Django 3.0.6 on 2021-08-25 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_subscribers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='subscribers',
            new_name='subscriber',
        ),
    ]
