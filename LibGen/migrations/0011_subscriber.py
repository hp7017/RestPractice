# Generated by Django 2.2.12 on 2020-05-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0010_auto_20200528_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]