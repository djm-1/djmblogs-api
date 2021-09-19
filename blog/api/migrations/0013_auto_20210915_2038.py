# Generated by Django 3.0.6 on 2021-09-15 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210915_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_time',
            field=models.DateTimeField(default='September 15,2021, 08:38 PM'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customUser'),
        ),
    ]
