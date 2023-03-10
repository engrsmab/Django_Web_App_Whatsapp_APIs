# Generated by Django 4.0.5 on 2022-10-03 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0037_data_mode_data_signal_data_volsolar_language_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='volBat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='language',
            name='volBat',
            field=models.CharField(default='Voltage Solar', max_length=30),
        ),
        migrations.AddField(
            model_name='language',
            name='volBatMenu',
            field=models.CharField(default='Voltage Battery', max_length=24),
        ),
        migrations.AlterField(
            model_name='language',
            name='volSolar',
            field=models.CharField(default='Voltage Battery', max_length=30),
        ),
    ]
