# Generated by Django 4.2 on 2023-05-25 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='عنوان صفحه'),
        ),
    ]