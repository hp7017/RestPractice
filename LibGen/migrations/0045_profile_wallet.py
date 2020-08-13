# Generated by Django 2.0 on 2020-06-30 13:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0044_auto_20200629_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wallet',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]