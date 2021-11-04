# Generated by Django 3.2.9 on 2021-11-03 20:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.CharField(default='Anonymous User', max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.CharField(default='img/events/default_event.jpg', max_length=200),
        ),
    ]