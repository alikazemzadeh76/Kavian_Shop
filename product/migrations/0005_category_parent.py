# Generated by Django 4.2 on 2023-05-08 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ManyToManyField(related_name='category', to='product.category', verbose_name='زیر مجموعه'),
        ),
    ]
