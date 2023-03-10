# Generated by Django 4.0.5 on 2022-06-22 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0007_device_whatsapps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='alarm',
        ),
        migrations.RemoveField(
            model_name='data',
            name='alarmStatus',
        ),
        migrations.RemoveField(
            model_name='language',
            name='alarm',
        ),
        migrations.AddField(
            model_name='client',
            name='alertStatus',
            field=models.IntegerField(default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='client',
            name='machineVoltage',
            field=models.IntegerField(default=12, max_length=2),
        ),
        migrations.AddField(
            model_name='client',
            name='temperatureAlert',
            field=models.IntegerField(default=1, max_length=2),
        ),
        migrations.AddField(
            model_name='language',
            name='machineErorr',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='machineStart',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='machineStop',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='machineWarning',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='client',
            name='language',
            field=models.CharField(default='English', max_length=15),
        ),
        migrations.AlterField(
            model_name='data',
            name='machineStatus',
            field=models.IntegerField(default=0, max_length=2),
        ),
        migrations.AlterField(
            model_name='data',
            name='voltage',
            field=models.IntegerField(default=0, max_length=2),
        ),
        migrations.AlterField(
            model_name='language',
            name='alarmStatus',
            field=models.CharField(default='Alarm', max_length=30),
        ),
    ]
