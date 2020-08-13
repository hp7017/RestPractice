# Generated by Django 2.0 on 2020-07-25 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LibGen', '0065_book_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('reference_id', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=500)),
                ('payment_mode', models.CharField(max_length=500)),
                ('tx_msg', models.CharField(max_length=500)),
                ('tx_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-tx_time'],
            },
        ),
    ]