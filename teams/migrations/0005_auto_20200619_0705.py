# Generated by Django 3.0.6 on 2020-06-18 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20200528_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='active_status',
            field=models.CharField(choices=[('모집진행중', '모집진행중'), ('모집마감', '모집마감'), ('활동중', '활동중'), ('활동종료', '활동종료')], default='모집진행중', max_length=15),
        ),
        migrations.AddField(
            model_name='team',
            name='recruitment_deadline',
            field=models.CharField(default='0000-00-00', max_length=15),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
