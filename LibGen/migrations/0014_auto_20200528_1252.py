# Generated by Django 2.2.12 on 2020-05-28 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0013_msg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuser',
            name='status',
            field=models.CharField(choices=[('OFF', 'OFF'), ('ON', 'ON')], max_length=10),
        ),
    ]