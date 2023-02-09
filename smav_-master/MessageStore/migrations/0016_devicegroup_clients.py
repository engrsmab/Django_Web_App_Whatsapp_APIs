# Generated by Django 4.0.5 on 2022-06-26 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0015_client_country_alter_device_imei_alter_device_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicegroup',
            name='clients',
            field=models.ManyToManyField(blank=True, to='MessageStore.client', verbose_name='Telegram User'),
        ),
    ]
