# Generated by Django 3.1.5 on 2021-02-23 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_auto_20210223_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='code',
            field=models.CharField(default='5WNJ5Q146', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
