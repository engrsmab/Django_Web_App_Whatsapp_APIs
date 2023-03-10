# Generated by Django 4.0.5 on 2022-09-20 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0026_device_contactmaintainer_alter_device_timemaintain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='maintainer',
            field=models.CharField(default='Maintainer', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='timeActive',
            field=models.CharField(default='Time Active', max_length=30),
        ),
        migrations.AlterField(
            model_name='device',
            name='timeActive',
            field=models.CharField(default='', editable=False, max_length=20),
        ),
    ]
