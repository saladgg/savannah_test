# Generated by Django 3.1.5 on 2021-03-01 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_auto_20210223_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useraccessgroup',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='customer',
            name='code',
            field=models.CharField(default='0U5P5G146', max_length=200),
        ),
    ]