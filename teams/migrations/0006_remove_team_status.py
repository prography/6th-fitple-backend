# Generated by Django 3.0.6 on 2020-06-19 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20200619_0705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='status',
        ),
    ]
