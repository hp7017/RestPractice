# Generated by Django 2.0 on 2020-06-18 13:49

import LibGen.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0032_auto_20200618_1905'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='width',
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(upload_to=LibGen.models.Profile.user_directory_path, validators=[LibGen.models.Profile.validate_image]),
        ),
    ]