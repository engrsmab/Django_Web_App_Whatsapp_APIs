# Generated by Django 4.0.5 on 2022-06-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0017_data_voltagebattery_language_voltagebattery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='machineStatus',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='data',
            name='voltage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='data',
            name='voltageBattery',
            field=models.FloatField(default=0),
        ),
    ]
