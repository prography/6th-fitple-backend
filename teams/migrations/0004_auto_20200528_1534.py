# Generated by Django 3.0.6 on 2020-05-28 06:34

import config.storage_backends
import config.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20200527_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='personnel',
        ),
        migrations.AddField(
            model_name='team',
            name='designer',
            field=models.PositiveIntegerField(default=0, verbose_name='디자이너'),
        ),
        migrations.AddField(
            model_name='team',
            name='developer',
            field=models.PositiveIntegerField(default=0, verbose_name='개발자'),
        ),
        migrations.AddField(
            model_name='team',
            name='planner',
            field=models.PositiveIntegerField(default=0, verbose_name='기획자'),
        ),
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.FileField(default='default_team.jpg', storage=config.storage_backends.PublicMediaStorage(), upload_to=config.utils.s3_test_image_upload_to, verbose_name='이미지'),
        ),
    ]
