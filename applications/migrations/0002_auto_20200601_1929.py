# Generated by Django 3.0.6 on 2020-06-01 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamapplication',
            name='job',
            field=models.CharField(choices=[('Developer', 'Developer'), ('Planner', 'Planner'), ('Designer', 'Designer')], default='Developer', max_length=10),
        ),
        migrations.AlterField(
            model_name='teamapplication',
            name='join_status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Canceled', 'Canceled'), ('Waiting', 'Waiting')], default='Waiting', max_length=10),
        ),
    ]
