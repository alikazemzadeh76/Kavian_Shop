# Generated by Django 4.2 on 2023-05-11 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_cart_cartshop'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diccount',
            options={'verbose_name': 'کد تخفیف', 'verbose_name_plural': 'کد های تخفیف'},
        ),
    ]