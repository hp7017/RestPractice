# Generated by Django 2.0 on 2020-06-29 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0042_sponsoredbook_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsoredbook',
            name='status',
            field=models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline')], default=False, max_length=100),
        ),
    ]
