# Generated by Django 3.1.5 on 2021-02-19 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20210218_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='code',
            field=models.CharField(default='S836G7E2J', max_length=200),
        ),
        migrations.CreateModel(
            name='UserTokenizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=100, unique=True)),
                ('refresh_token', models.CharField(max_length=100, unique=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
