# Generated by Django 4.0.5 on 2022-09-21 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MessageStore', '0031_alter_language_maintainer_alter_language_timeactive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='timeActive',
            field=models.CharField(default='0', editable=False, max_length=20),
        ),
    ]