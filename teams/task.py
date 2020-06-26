from __future__ import absolute_import, unicode_literals
from celery import shared_task
from config.email import send_aplct_guide


@shared_task
def def_email(email):
    print(email)
    send_aplct_guide(email)
    return True
