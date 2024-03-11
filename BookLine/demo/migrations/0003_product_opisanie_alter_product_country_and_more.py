# Generated by Django 4.2.4 on 2024-02-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_iteminorder_order_iteminorder_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='opisanie',
            field=models.CharField(blank=True, max_length=254, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='country',
            field=models.CharField(blank=True, max_length=254, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.IntegerField(blank=True, verbose_name='Год издания'),
        ),
    ]
