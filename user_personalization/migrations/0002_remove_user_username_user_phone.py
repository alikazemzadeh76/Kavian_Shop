# Generated by Django 4.2 on 2023-04-23 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_personalization', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default=1, max_length=50, unique=True, verbose_name='شماره تلفن'),
            preserve_default=False,
        ),
    ]