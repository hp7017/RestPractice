# Generated by Django 2.2.12 on 2020-05-19 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0005_auto_20191110_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=20)),
                ('msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EnvirementVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=10)),
                ('desktop_version', models.CharField(max_length=10)),
                ('mobile_maintainence', models.BooleanField()),
                ('desktop_maintainence', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Msg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=20)),
                ('msg', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='App',
        ),
        migrations.AddField(
            model_name='cuser',
            name='platform',
            field=models.CharField(choices=[('Mobile', 'Mobile'), ('Desktop', 'Desktop')], default='Mobile', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuser',
            name='status',
            field=models.CharField(choices=[(0, 'OFF'), (1, 'ON')], max_length=10),
        ),
        migrations.AddField(
            model_name='adminmsg',
            name='envirement_variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adminMsgs', to='LibGen.EnvirementVariable'),
        ),
        migrations.AddField(
            model_name='cuser',
            name='msg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='msgs', to='LibGen.Msg'),
        ),
    ]
