# Generated by Django 3.2.9 on 2021-11-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='gender',
            field=models.CharField(default='not disclose', max_length=50),
        ),
    ]