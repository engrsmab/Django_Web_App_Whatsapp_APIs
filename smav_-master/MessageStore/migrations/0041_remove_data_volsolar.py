# Generated by Django 4.0.5 on 2022-10-06 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0040_alter_data_signal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='volSolar',
        ),
    ]