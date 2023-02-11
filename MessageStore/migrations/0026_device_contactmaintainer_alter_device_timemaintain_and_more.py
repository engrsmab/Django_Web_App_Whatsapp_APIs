# Generated by Django 4.0.5 on 2022-09-18 03:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0025_device_active_device_maintainer_device_timeactive_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='contactMaintainer',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='device',
            name='timeMaintain',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='device',
            name='timeStart',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]