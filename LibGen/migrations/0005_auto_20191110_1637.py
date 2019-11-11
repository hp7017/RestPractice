# Generated by Django 2.2.3 on 2019-11-10 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0004_auto_20191110_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='update',
        ),
        migrations.AddField(
            model_name='app',
            name='version',
            field=models.CharField(default='1.0', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='cuser',
            name='status',
            field=models.CharField(choices=[(1, 'ON'), (0, 'OFF')], max_length=10),
        ),
    ]
