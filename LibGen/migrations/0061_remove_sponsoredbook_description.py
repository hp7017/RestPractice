# Generated by Django 2.0 on 2020-07-06 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0060_auto_20200706_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsoredbook',
            name='description',
        ),
    ]
