# Generated by Django 4.0.5 on 2022-09-27 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0034_device_timeactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='smavSetting',
            field=models.CharField(default='SMAV Setting', max_length=30),
        ),
    ]
