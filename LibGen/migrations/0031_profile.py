# Generated by Django 2.0 on 2020-06-18 13:32

import LibGen.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LibGen', '0030_auto_20200615_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveIntegerField()),
                ('width', models.PositiveIntegerField()),
                ('pic', models.ImageField(height_field='height', upload_to=LibGen.models.Profile.user_directory_path, validators=[LibGen.models.Profile.validate_image], width_field='width')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]