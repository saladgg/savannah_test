# Generated by Django 3.1.5 on 2021-03-03 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_auto_20210303_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='code',
            field=models.CharField(default='NEWCUSTOMER', max_length=100),
        ),
    ]
