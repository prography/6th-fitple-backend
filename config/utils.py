import os
from uuid import uuid4

from django.utils import timezone


def s3_test_image_upload_to(instance, filename):  # utils.py
    ymd_path = timezone.now().strftime('%Y/%m/%d/%H/%M')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([
        ymd_path,
        uuid_name + extension,
    ])


def check_email_subscription(user):
    return user.profile.email_subscribe, user.email
