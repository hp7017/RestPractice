# Generated by Django 2.0 on 2020-07-04 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0052_auto_20200704_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsoredbook',
            name='wallet_size',
        ),
    ]
