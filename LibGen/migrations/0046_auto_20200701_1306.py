# Generated by Django 2.0 on 2020-07-01 07:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0045_profile_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsoredbook',
            name='wallet_size',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.1)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sponsoredbook',
            name='verified',
            field=models.BooleanField(default=True),
        ),
    ]