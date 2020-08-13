# Generated by Django 2.2.8 on 2020-06-14 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0027_auto_20200613_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('link', models.URLField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='LibGen.Book')),
            ],
        ),
    ]