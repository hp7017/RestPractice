# Generated by Django 2.0 on 2020-08-05 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibGen', '0076_auto_20200805_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replyto',
            name='email',
        ),
        migrations.AddField(
            model_name='email',
            name='reply_to',
            field=models.EmailField(choices=[('support@librarygenesis.in', 'Support')], default='support@librarygenesis.in', max_length=254),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ReplyTo',
        ),
    ]