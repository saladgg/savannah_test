# Generated by Django 3.1.5 on 2021-02-23 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20210222_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='code',
            field=models.CharField(default='F05TA74B5', max_length=200),
        ),
    ]
