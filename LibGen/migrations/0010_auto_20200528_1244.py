# Generated by Django 2.2.12 on 2020-05-28 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0009_auto_20200522_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF')], max_length=10),
        ),
    ]
