# Generated by Django 3.0.6 on 2020-05-27 13:39

import config.storage_backends
import config.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0002_auto_20200525_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.FileField(default='https://cdn.pixabay.com/photo/2017/05/12/08/46/team-2306528_960_720.jpg', storage=config.storage_backends.PublicMediaStorage, upload_to=config.utils.s3_test_image_upload_to, verbose_name='이미지'),
        ),
    ]
