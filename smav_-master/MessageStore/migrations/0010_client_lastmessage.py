# Generated by Django 4.0.5 on 2022-06-22 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0009_alter_client_alertstatus_alter_client_machinevoltage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='lastmessage',
            field=models.IntegerField(default=0),
        ),
    ]