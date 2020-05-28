# Generated by Django 2.2.12 on 2020-05-28 07:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0014_auto_20200528_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='user',
        ),
        migrations.AddField(
            model_name='subscriber',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AdminMsg',
        ),
        migrations.DeleteModel(
            name='CUser',
        ),
        migrations.DeleteModel(
            name='EnvirementVariable',
        ),
    ]
